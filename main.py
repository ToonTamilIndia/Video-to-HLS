import os
import subprocess
import json
import sys
import shutil
import argparse
import logging
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional

# --- Configuration Loading ---
CONFIG_FILE = Path("config.json")
DEFAULT_CONFIG = {
    "ffmpeg_path": "ffmpeg",
    "ffprobe_path": "ffprobe",
    "video_variants": {
        "144p": {"resolution": "256x144", "bitrate": "300k", "order": 10},
        "240p": {"resolution": "426x240", "bitrate": "500k", "order": 20},
        "360p": {"resolution": "640x360", "bitrate": "800k", "order": 30},
        "480p": {"resolution": "854x480", "bitrate": "1200k", "order": 40},
        "720p": {"resolution": "1280x720", "bitrate": "2500k", "order": 50},
        "1080p": {"resolution": "1920x1080", "bitrate": "4500k", "order": 60},
    },
    "default_audio_bitrate": "128k",
    "default_ffmpeg_preset": "medium",
    "default_segment_duration": 6,
    "github_deployment": {
        "enabled": False,
        "default_branch": "main",
        "temp_deploy_dir": "_deploy_tmp"
    },
    "archive_deployment": {
        "enabled": False,
        "max_workers": 5,
        "worker_url": "",
        "base_archive_url": "https://archive.org/download/{identifier}"
    }
}


def load_config() -> Dict[str, Any]:
    """Loads configuration from JSON file, falling back to defaults."""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
            # Basic validation or merging with defaults could be added here
            return {**DEFAULT_CONFIG, **config}
        except json.JSONDecodeError:
            logging.error(f"Error decoding {CONFIG_FILE}. Using default configuration.")
            return DEFAULT_CONFIG
        except Exception as e:
            logging.error(f"Error loading {CONFIG_FILE}: {e}. Using default configuration.")
            return DEFAULT_CONFIG
    return DEFAULT_CONFIG

APP_CONFIG = load_config()
VIDEO_VARIANTS = APP_CONFIG["video_variants"]

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

# --- Helper Functions ---
def run_command(cmd: List[str], check: bool = True) -> subprocess.CompletedProcess:
    """Executes a shell command and logs its execution."""
    logging.info(f"Executing: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, check=check, capture_output=True, text=True)
        if result.stdout:
            logging.debug(f"Stdout: {result.stdout.strip()}")
        if result.stderr:
            logging.debug(f"Stderr: {result.stderr.strip()}")
        if check and result.returncode != 0:
            logging.error(f"Command failed with exit code {result.returncode}")
            logging.error(f"Error output: {result.stderr}")
            raise subprocess.CalledProcessError(result.returncode, cmd, output=result.stdout, stderr=result.stderr)
        return result
    except FileNotFoundError:
        logging.error(f"Error: The command '{cmd[0]}' was not found. Ensure FFmpeg/FFprobe is installed and in your PATH, or configure the path in {CONFIG_FILE}.")
        sys.exit(1)
    except Exception as e:
        logging.error(f"An unexpected error occurred while running command {' '.join(cmd)}: {e}")
        raise

def get_video_metadata(input_file: Path) -> Dict[str, Any]:
    """Probes video file for stream information using ffprobe."""
    logging.info(f"Probing video metadata for: {input_file}")
    cmd = [
        APP_CONFIG["ffprobe_path"],
        "-v", "error",
        "-print_format", "json",
        "-show_streams",
        "-show_format",
        str(input_file)
    ]
    result = run_command(cmd)
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as e:
        logging.error(f"Failed to parse ffprobe output: {e}")
        logging.error(f"ffprobe output was: {result.stdout}")
        raise

def bitrate_to_bandwidth(bitrate_str: str) -> int:
    """Converts bitrate string (e.g., '500k') to integer bandwidth (e.g., 500000)."""
    bitrate_str = bitrate_str.lower()
    if "k" in bitrate_str:
        return int(float(bitrate_str.replace("k", "")) * 1000)
    elif "m" in bitrate_str:
        return int(float(bitrate_str.replace("m", "")) * 1000000)
    return int(bitrate_str)

def get_input_video_resolution(streams: List[Dict[str, Any]]) -> Optional[Tuple[int, int]]:
    """Extracts video resolution (width, height) from ffprobe streams."""
    for stream in streams:
        if stream.get("codec_type") == "video":
            width = stream.get("width")
            height = stream.get("height")
            if width and height:
                return int(width), int(height)
    return None

# --- Core HLS Generation Logic ---
def generate_video_renditions(
    input_file: Path,
    output_dir: Path,
    segment_duration: int,
    ffmpeg_preset: str,
    selected_qualities: List[str],
    input_video_height: Optional[int]
) -> List[Tuple[str, Dict[str, str], str]]:
    """Generates different video quality renditions."""
    video_paths = []
    sorted_variants = sorted(VIDEO_VARIANTS.items(), key=lambda item: item[1].get('order', 0))

    for quality_name, settings in sorted_variants:
        if quality_name not in selected_qualities:
            continue

        # Skip upscaling if input video height is known
        rendition_height = int(settings["resolution"].split("x")[1])
        if input_video_height and rendition_height > input_video_height:
            logging.info(f"Skipping {quality_name} ({rendition_height}p) as it's higher than input video height ({input_video_height}p).")
            continue
        
        logging.info(f"Processing video rendition: {quality_name}")
        variant_path = output_dir / f"video_{quality_name}"
        variant_path.mkdir(parents=True, exist_ok=True)

        cmd = [
            APP_CONFIG["ffmpeg_path"], "-y", # -y to overwrite output files without asking
            "-i", str(input_file),
            "-map", "0:v:0",  # Map the first video stream
            "-c:v", "libx264",
            "-b:v", settings["bitrate"],
            "-s", settings["resolution"],
            "-profile:v", "main", # Or high, baseline. Main is widely compatible.
            "-level:v", "4.0", # Adjust based on resolution/bitrate for compatibility
            "-preset", ffmpeg_preset,
            "-force_key_frames", f"expr:gte(t,n_forced*{segment_duration})",
            "-f", "hls",
            "-hls_time", str(segment_duration),
            "-hls_playlist_type", "vod", # Video on Demand
            "-hls_segment_filename", str(variant_path / "segment_%05d.ts"), # %05d for more segments
            str(variant_path / "index.m3u8")
        ]
        run_command(cmd)
        video_paths.append((quality_name, settings, f"video_{quality_name}/index.m3u8"))
    
    if not video_paths:
        logging.warning("No video renditions were generated. Check input video resolution and selected qualities.")
    return video_paths

def generate_audio_renditions(
    input_file: Path,
    output_dir: Path,
    audio_streams: List[Dict[str, Any]],
    segment_duration: int,
    ffmpeg_preset: str
) -> List[Tuple[str, str, str]]:
    """Generates HLS renditions for each audio track."""
    audio_playlists = []
    if not audio_streams:
        logging.warning("No audio streams found in the input file.")
        return []

    for i, stream in enumerate(audio_streams):
        lang_code = stream.get("tags", {}).get("language", f"und{i}") # und for undetermined
        lang_name = stream.get("tags", {}).get("title", f"Audio Track {i+1}")
        
        logging.info(f"Processing audio rendition: {lang_name} ({lang_code})")
        audio_dir = output_dir / f"audio_{lang_code}_{i}"
        audio_dir.mkdir(parents=True, exist_ok=True)

        cmd = [
            APP_CONFIG["ffmpeg_path"], "-y",
            "-i", str(input_file),
            "-map", f"0:a:{i}", # Map specific audio stream
            "-c:a", "aac",
            "-b:a", APP_CONFIG["default_audio_bitrate"],
            "-preset", ffmpeg_preset,
            "-f", "hls",
            "-hls_time", str(segment_duration),
            "-hls_playlist_type", "vod",
            "-hls_segment_filename", str(audio_dir / "segment_%05d.ts"),
            str(audio_dir / "index.m3u8")
        ]
        run_command(cmd)
        audio_playlists.append((lang_code, lang_name, f"audio_{lang_code}_{i}/index.m3u8"))
    return audio_playlists

def generate_subtitle_renditions(
    input_file: Path,
    output_dir: Path,
    subtitle_streams: List[Dict[str, Any]]
) -> List[Tuple[str, str, str]]:
    """Extracts subtitle tracks and converts them to WebVTT format for HLS."""
    subtitle_playlists = []
    if not subtitle_streams:
        logging.info("No subtitle streams found in the input file.")
        return []

    for i, stream in enumerate(subtitle_streams):
        lang_code = stream.get("tags", {}).get("language", f"sub{i}")
        lang_name = stream.get("tags", {}).get("title", f"Subtitle {i+1}")
        
        logging.info(f"Processing subtitle: {lang_name} ({lang_code})")
        subtitle_dir = output_dir / f"sub_{lang_code}_{i}"
        subtitle_dir.mkdir(parents=True, exist_ok=True)
        
        # Output subtitles as WebVTT
        vtt_filename = f"subtitles_{lang_code}_{i}.vtt"
        vtt_file_path = subtitle_dir / vtt_filename
        
        cmd = [
            APP_CONFIG["ffmpeg_path"], "-y",
            "-i", str(input_file),
            "-map", f"0:s:{i}", # Map specific subtitle stream
            "-c:s", "webvtt", # Convert to WebVTT
            str(vtt_file_path)
        ]
        try:
            run_command(cmd)
            # Relative path for the master playlist
            subtitle_playlists.append((lang_code, lang_name, str(Path(f"sub_{lang_code}_{i}") / vtt_filename)))
        except subprocess.CalledProcessError as e:
            logging.warning(f"Could not extract subtitle stream {i} ({lang_name}): {e.stderr}")
        except Exception as e:
            logging.warning(f"An unexpected error occurred while processing subtitle stream {i} ({lang_name}): {e}")

    return subtitle_playlists

def generate_master_playlist(
    output_dir: Path,
    video_paths: List[Tuple[str, Dict[str, str], str]],
    audio_playlists: List[Tuple[str, str, str]],
    subtitle_playlists: List[Tuple[str, str, str]]
):
    """Creates the master M3U8 playlist."""
    master_playlist_path = output_dir / "master.m3u8"
    logging.info(f"Generating master playlist: {master_playlist_path}")

    with open(master_playlist_path, "w") as f:
        f.write("#EXTM3U\n")
        f.write("#EXT-X-VERSION:3\n\n") # Consider version 6 or 7 for more features if needed

        # Audio renditions
        # Create a unique group ID for audio, e.g., "aac"
        # Default audio can be marked with DEFAULT=YES
        is_first_audio = True
        for lang_code, lang_name, path in audio_playlists:
            default_flag = "YES" if is_first_audio else "NO" # Make first audio default
            autoselect_flag = "YES"
            f.write(
                f'#EXT-X-MEDIA:TYPE=AUDIO,GROUP-ID="audio-aac",NAME="{lang_name}",LANGUAGE="{lang_code}",'
                f'DEFAULT={default_flag},AUTOSELECT={autoselect_flag},URI="{path}"\n'
            )
            is_first_audio = False
        f.write("\n")

        # Subtitle renditions
        # Create a unique group ID for subtitles, e.g., "subs"
        is_first_subtitle = True
        for lang_code, lang_name, path in subtitle_playlists:
            default_flag = "NO" # Subtitles usually not default
            autoselect_flag = "YES"
            f.write(
                f'#EXT-X-MEDIA:TYPE=SUBTITLES,GROUP-ID="subs",NAME="{lang_name}",LANGUAGE="{lang_code}",'
                f'DEFAULT={default_flag},AUTOSELECT={autoselect_flag},URI="{path}"\n'
            )
            is_first_subtitle = False
        f.write("\n")
        
        # Video renditions with associated audio and subtitles
        # Ensure CODECS string is accurate for your encodes. avc1.xxxxxx for H.264, mp4a.40.2 for AAC-LC.
        # You might need to probe the actual generated files for precise codec strings if issues arise.
        # Common H.264 profiles: Baseline (avc1.42E0xx), Main (avc1.4D40xx), High (avc1.6400xx)
        # For simplicity, using a common one.
        # Example: CODECS="avc1.4D401F,mp4a.40.2" (H.264 Main Profile Level 3.1, AAC-LC)
        
        # Sort video_paths by bitrate (ascending) for better player adaptation
        video_paths.sort(key=lambda x: bitrate_to_bandwidth(x[1]["bitrate"]))

        for quality_name, settings, path in video_paths:
            bandwidth = bitrate_to_bandwidth(settings["bitrate"])
            # Add audio bitrate to video bandwidth for a more accurate total stream bandwidth
            # Assuming one audio stream for simplicity here. If multiple, this needs adjustment.
            if audio_playlists:
                 # A rough estimate, actual audio bitrate might vary
                bandwidth += bitrate_to_bandwidth(APP_CONFIG["default_audio_bitrate"])

            # Construct codec string. This is a common one. For more accuracy, ffprobe the TS segments.
            # The video codec part (e.g., avc1.4D401F) can vary based on libx264 settings.
            # For simplicity, using a generic one.
            codecs = "avc1.4D401F,mp4a.40.2" # Example: H.264 Main Profile, AAC-LC

            f.write(
                f'#EXT-X-STREAM-INF:BANDWIDTH={bandwidth},RESOLUTION={settings["resolution"]},'
                f'CODECS="{codecs}",AUDIO="audio-aac",SUBTITLES="subs"\n'
            )
            f.write(f"{path}\n")
            
    logging.info("Master playlist generated successfully.")

def generate_thumbnail(input_file: Path, output_dir: Path, thumbnail_time: str = "00:00:05") -> Optional[Path]:
    """Generates a thumbnail from the video."""
    logging.info(f"Generating thumbnail for {input_file}")
    thumbnail_file = output_dir / f"{input_file.stem}_thumbnail.jpg"
    try:
        cmd = [
            APP_CONFIG["ffmpeg_path"], "-y",
            "-ss", thumbnail_time,       # Seek to time
            "-i", str(input_file),
            "-vframes", "1",             # Extract one frame
            "-q:v", "2",                 # Quality (2-5 is good for JPEG)
            str(thumbnail_file)
        ]
        run_command(cmd)
        logging.info(f"Thumbnail generated: {thumbnail_file}")
        return thumbnail_file
    except Exception as e:
        logging.error(f"Failed to generate thumbnail: {e}")
        return None

# --- Deployment (GitHub Pages Example) ---
def deploy_to_github_pages(
    folder_to_upload: Path,
    github_username: Optional[str],
    repo_name: Optional[str],
    github_token: Optional[str],
    branch: Optional[str]
):
    """Deploys the HLS content to GitHub Pages."""
    if not all([github_username, repo_name, github_token, branch]):
        logging.warning("GitHub deployment skipped: Missing username, repo name, token, or branch.")
        logging.info("Set GITHUB_USERNAME, GITHUB_REPO, GITHUB_TOKEN, GITHUB_BRANCH environment variables or CLI options.")
        return

    logging.info(f"Starting deployment to GitHub Pages: {github_username}/{repo_name} on branch {branch}")
    
    tmp_dir_name = APP_CONFIG["github_deployment"]["temp_deploy_dir"]
    # Create a temporary directory in the parent of folder_to_upload to avoid issues if folder_to_upload is already in a git repo
    base_tmp_dir = folder_to_upload.parent / tmp_dir_name 
    
    deploy_content_path = base_tmp_dir / folder_to_upload.name

    if base_tmp_dir.exists():
        logging.info(f"Cleaning up old temporary deployment directory: {base_tmp_dir}")
        shutil.rmtree(base_tmp_dir)
    
    base_tmp_dir.mkdir(parents=True, exist_ok=True)
    
    logging.info(f"Copying HLS content from {folder_to_upload} to {deploy_content_path}")
    shutil.copytree(folder_to_upload, deploy_content_path)

    # Create .nojekyll to avoid GitHub Pages issues with underscore/dot folders
    (deploy_content_path / ".nojekyll").touch()

    # Store current working directory and change to the base_tmp_dir for git operations
    original_cwd = Path.cwd()
    os.chdir(base_tmp_dir)
    logging.info(f"Changed directory to: {Path.cwd()}")

    remote_url = f"https://{github_username}:{github_token}@github.com/{github_username}/{repo_name}.git"

    try:
        run_command(["git", "init"])
        # Check if branch already exists locally, if so, just checkout
        try:
            run_command(["git", "show-branch", branch], check=False) # Check if branch exists
            run_command(["git", "checkout", branch])
        except subprocess.CalledProcessError: # If branch doesn't exist
             run_command(["git", "checkout", "-b", branch])

        # Check if remote 'origin' already exists
        git_remote_result = run_command(["git", "remote", "-v"], check=False)
        if "origin" not in git_remote_result.stdout:
            run_command(["git", "remote", "add", "origin", remote_url])
        else: # Update URL if it changed (e.g. token updated)
            run_command(["git", "remote", "set-url", "origin", remote_url])
            
        run_command(["git", "add", str(folder_to_upload.name)]) # Add only the specific output folder
        
        # Check for changes before committing
        status_result = run_command(["git", "status", "--porcelain"])
        if not status_result.stdout.strip():
            logging.info("No changes to commit. Deployment skipped.")
            return

        run_command(["git", "commit", "-m", f"Auto deploy HLS files: {folder_to_upload.name}"])
        logging.info(f"Pushing to origin/{branch}...")
        run_command(["git", "push", "--force", "origin", branch]) # Use --force with caution
        
        logging.info("✅ Deployment to GitHub Pages successful!")
        # The URL structure depends on whether it's a user/org page or project page
        # Assuming project page:
        hls_url_path = f"{repo_name}/{folder_to_upload.name}/master.m3u8"
        if f"{github_username}.github.io" == repo_name.lower(): # User/Org page
             hls_url_path = f"{folder_to_upload.name}/master.m3u8"
        
        logging.info(f"🌐 HLS URL: https://{github_username.lower()}.github.io/{hls_url_path}")

    except subprocess.CalledProcessError as e:
        logging.error(f"GitHub deployment failed: {e}")
        logging.error(f"Git command output: {e.stderr}")
    except Exception as e:
        logging.error(f"An unexpected error occurred during GitHub deployment: {e}")
    finally:
        os.chdir(original_cwd) # Always change back to original directory
        logging.info(f"Changed directory back to: {original_cwd}")
        # Optionally, clean up the temp directory after deployment
        # logging.info(f"Cleaning up temporary deployment directory: {base_tmp_dir}")
        # shutil.rmtree(base_tmp_dir)

def deploy_to_internet_archive(
    folder_to_upload: Path,
    access_key: Optional[str],
    secret_key: Optional[str],
    max_workers: int,
    worker_url: str
):
    import time
    from concurrent.futures import ThreadPoolExecutor, as_completed
    import internetarchive
    import re
    from rich.console import Console
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn

    IDENTIFIER = folder_to_upload.name.replace(" ", "_") + "-ToonTamilIndia"
    BASE_ARCHIVE_URL = APP_CONFIG["archive_deployment"]["base_archive_url"].format(identifier=IDENTIFIER)
    console = Console()

    def rewrite_m3u8_file(file_path, relative_path):
        with open(file_path, 'r') as f:
            lines = f.readlines()

        updated_lines = []
        for line in lines:
            # Replace URI="..." if it exists in the line
            if 'URI="' in line:
                def replace_uri(match):
                    original_uri = match.group(1)
                    updated_uri = f'{worker_url}{BASE_ARCHIVE_URL}/{os.path.dirname(relative_path)}/{original_uri}'.replace('\\', '/')
                    return f'URI="{updated_uri}"'

                line = re.sub(r'URI="([^"]+)"', replace_uri, line)
            elif line.strip() and not line.strip().startswith('#'):
                # plain segment line (e.g., index0.ts, not a tag)
                archive_url = f'{worker_url}{BASE_ARCHIVE_URL}/{os.path.dirname(relative_path)}/{line.strip()}'.replace('\\', '/')
                line = f'{archive_url}\n'

            updated_lines.append(line)

        with open(file_path, 'w') as f:
            f.writelines(updated_lines)

    def rewrite_all_m3u8_files():
        console.print("[bold yellow]Rewriting .m3u8 files with worker URLs...[/bold yellow]")
        for root, _, files in os.walk(folder_to_upload):
            for file in files:
                if file.endswith('.m3u8'):
                    full_path = os.path.join(root, file)
                    relative_path = os.path.relpath(full_path, folder_to_upload).replace("\\", "/")
                    rewrite_m3u8_file(full_path, relative_path)
                    console.print(f"[green]✔ Rewritten:[/green] {relative_path}")

    def collect_files(folder):
        uploads = []
        for root, _, files in os.walk(folder):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, folder).replace("\\", "/")
                uploads.append((full_path, rel_path))
        return uploads

    def upload_file(local_path, remote_path):
        try:
            result = internetarchive.upload(
                IDENTIFIER,
                {remote_path: local_path},
                access_key=access_key,
                secret_key=secret_key,
                retries=100,
                verbose=False,
            )
            status = "success" if result[0].status_code == 200 else f"failed ({result[0].status_code})"
        except Exception as e:
            status = f"error: {str(e)}"
        return remote_path, status

    def upload_all(files):
        console.print("\n[bold yellow]Uploading files to Internet Archive...[/bold yellow]")
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.fields[filename]}", justify="right"),
            BarColumn(),
            TextColumn("{task.fields[status]}", justify="left"),
            TimeElapsedColumn(),
            transient=True,
        ) as progress:
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = {
                    executor.submit(upload_file, lp, rp): (lp, rp)
                    for lp, rp in files
                }

                for future in as_completed(futures):
                    lp, rp = futures[future]
                    try:
                        rel, result = future.result()
                        color = "green" if "success" in result else "red"
                        progress.add_task("upload", filename=rel, status=f"[{color}]{result}[/{color}]")
                    except Exception as e:
                        progress.add_task("upload", filename=rp, status=f"[red]exception: {e}[/red]")

    # Start the deployment process
    rewrite_all_m3u8_files()
    console.print(f"\n[bold yellow]Collecting files in:[/] {folder_to_upload}")
    file_list = collect_files(folder_to_upload)
    console.print(f"[bold cyan]Found {len(file_list)} files to upload[/bold cyan]\n")
    upload_all(file_list)
    console.print(f"\n[bold green]✅ Upload complete Check : {worker_url}{BASE_ARCHIVE_URL}/master.m3u8.[/bold green]")
# --- Main HLS Generation Function ---
def create_hls_package(
    input_file: Path,
    output_dir: Path,
    segment_duration: int,
    ffmpeg_preset: str,
    video_qualities_str: Optional[str] = None,
    generate_thumb: bool = True,
    thumbnail_time: str = "00:00:05",
    deploy_gh: bool = False,
    github_username: Optional[str] = None,
    github_repo: Optional[str] = None,
    github_token: Optional[str] = None,
    github_branch: Optional[str] = None
):
    """Main function to orchestrate HLS package creation."""
    if not input_file.exists():
        logging.error(f"Input file not found: {input_file}")
        return

    output_dir.mkdir(parents=True, exist_ok=True)
    logging.info(f"Starting HLS packaging for {input_file} into {output_dir}")

    try:
        metadata = get_video_metadata(input_file)
    except Exception as e:
        logging.error(f"Could not get video metadata. Aborting. Error: {e}")
        return
        
    all_streams = metadata.get("streams", [])
    input_video_height = get_input_video_resolution(all_streams)
    if input_video_height:
        logging.info(f"Detected input video resolution: {input_video_height[0]}x{input_video_height[1]}")
    else:
        logging.warning("Could not determine input video resolution. Quality selection might not be optimal.")

    audio_streams = [s for s in all_streams if s["codec_type"] == "audio"]
    subtitle_streams = [s for s in all_streams if s["codec_type"] == "subtitle"]

    # Determine which video qualities to process
    available_qualities = list(VIDEO_VARIANTS.keys())
    if video_qualities_str:
        selected_qualities = [q.strip() for q in video_qualities_str.split(",")]
        # Validate selected qualities
        valid_selected_qualities = [q for q in selected_qualities if q in available_qualities]
        invalid_qualities = set(selected_qualities) - set(valid_selected_qualities)
        if invalid_qualities:
            logging.warning(f"Ignoring invalid video qualities: {', '.join(invalid_qualities)}. Available: {', '.join(available_qualities)}")
        selected_qualities = valid_selected_qualities
        if not selected_qualities:
            logging.warning("No valid video qualities selected. Defaulting to all suitable qualities.")
            selected_qualities = available_qualities # Fallback or choose a default set
    else: # If no qualities specified, use all available that are not upscales
        selected_qualities = available_qualities

    logging.info(f"Target video qualities: {', '.join(selected_qualities)}")

    video_paths = generate_video_renditions(
        input_file, output_dir, segment_duration, ffmpeg_preset, selected_qualities, input_video_height[1] if input_video_height else None
    )
    if not video_paths:
        logging.error("Failed to generate any video renditions. Aborting.")
        return

    audio_playlists = generate_audio_renditions(
        input_file, output_dir, audio_streams, segment_duration, ffmpeg_preset
    )
    subtitle_playlists = generate_subtitle_renditions(
        input_file, output_dir, subtitle_streams
    )

    generate_master_playlist(output_dir, video_paths, audio_playlists, subtitle_playlists)

    if generate_thumb:
        generate_thumbnail(input_file, output_dir, thumbnail_time)

    logging.info(f"✅ HLS packaging complete. Master playlist: {output_dir / 'master.m3u8'}")

    if deploy_gh and APP_CONFIG["github_deployment"]["enabled"]:
        deploy_to_github_pages(
            output_dir,
            github_username or os.getenv("GITHUB_USERNAME"),
            github_repo or os.getenv("GITHUB_REPO"),
            github_token or os.getenv("GITHUB_TOKEN"),
            github_branch or os.getenv("GITHUB_BRANCH") or APP_CONFIG["github_deployment"]["default_branch"]
        )
    elif deploy_gh:
        logging.warning("GitHub deployment was requested but is disabled in config.json or missing credentials.")


# --- CLI Argument Parsing ---
def main():
    parser = argparse.ArgumentParser(
        description="Advanced Video to HLS Converter with multi-audio/subs, adaptive bitrate, and GitHub Pages deployment.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("input", type=Path, help="Input video file path.")
    parser.add_argument("output", type=Path, help="Output directory for HLS files.")
    
    parser.add_argument(
        "-vq", "--video-qualities", type=str, default=None,
        help=f"Comma-separated video qualities to generate (e.g., 1080p,720p,480p). Available: {', '.join(VIDEO_VARIANTS.keys())}. If not specified, suitable qualities based on input resolution will be chosen."
    )
    parser.add_argument(
        "-sd", "--segment-duration", type=int, default=APP_CONFIG["default_segment_duration"],
        help="Segment duration in seconds for HLS."
    )
    parser.add_argument(
        "-p", "--preset", type=str, default=APP_CONFIG["default_ffmpeg_preset"],
        help="FFmpeg preset for encoding (e.g., ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow)."
    )
    parser.add_argument(
        "--no-thumbnail", action="store_false", dest="generate_thumbnail",
        help="Disable thumbnail generation."
    )
    parser.add_argument(
        "--thumbnail-time", type=str, default="00:00:05",
        help="Timestamp for thumbnail generation (e.g., 00:00:05 or 5 for 5 seconds)."
    )
    
    # Deployment arguments
    deploy_group = parser.add_argument_group('GitHub Deployment Options')
    archive_group = parser.add_argument_group('Internet Archive Deployment Options')
    archive_group.add_argument(
        "--archive", action="store_true",
        help="Upload the output HLS folder to Internet Archive. Requires Internet Archive credentials."
    )
    archive_group.add_argument("--access-key", type=str, default=os.getenv("ARCHIVE_ACCESS_KEY"), help="Internet Archive access key (or set ARCHIVE_ACCESS_KEY env var).")
    archive_group.add_argument("--secret-key", type=str, default=os.getenv("ARCHIVE_SECRET_KEY"), help="Internet Archive secret key (or set ARCHIVE_SECRET_KEY env var).")
    archive_group.add_argument("--max-workers", type=int, default=APP_CONFIG["archive_deployment"]["max_workers"], help="Max workers for Internet Archive upload.")
    archive_group.add_argument("--worker-url", type=str, default=APP_CONFIG["archive_deployment"]["worker_url"], help="Worker URL for Internet Archive upload.")
    deploy_group.add_argument(
        "--deploy", action="store_true",
        help="Deploy the output HLS folder to GitHub Pages. Requires GitHub credentials."
    )
    deploy_group.add_argument("--gh-user", type=str, default=os.getenv("GITHUB_USERNAME"), help="GitHub username (or set GITHUB_USERNAME env var).")
    deploy_group.add_argument("--gh-repo", type=str, default=os.getenv("GITHUB_REPO"), help="GitHub repository name (or set GITHUB_REPO env var).")
    deploy_group.add_argument("--gh-token", type=str, default=os.getenv("GITHUB_TOKEN"), help="GitHub Personal Access Token with repo scope (or set GITHUB_TOKEN env var).")
    deploy_group.add_argument("--gh-branch", type=str, default=os.getenv("GITHUB_BRANCH", APP_CONFIG["github_deployment"]["default_branch"]), help="GitHub branch to deploy to (or set GITHUB_BRANCH env var).")

    parser.add_argument(
        "-v", "--verbose", action="store_true",
        help="Enable verbose debug logging."
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    create_hls_package(
        input_file=args.input,
        output_dir=args.output,
        segment_duration=args.segment_duration,
        ffmpeg_preset=args.preset,
        video_qualities_str=args.video_qualities,
        generate_thumb=args.generate_thumbnail,
        thumbnail_time=args.thumbnail_time,
        deploy_gh=args.deploy,
        github_username=args.gh_user,
        github_repo=args.gh_repo,
        github_token=args.gh_token,
        github_branch=args.gh_branch
    )
    if args.archive or APP_CONFIG["archive_deployment"]["enabled"]:
        deploy_to_internet_archive(
            folder_to_upload=args.output,
            access_key=args.access_key,
            secret_key=args.secret_key,
            max_workers=args.max_workers,
            worker_url=args.worker_url
        )

if __name__ == "__main__":
    main()
