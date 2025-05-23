
# 🎬 Video-to-HLS Converter (V2HLS) 🎞️ 🚀

[![GitHub Repo stars](https://img.shields.io/github/stars/ToonTamilIndia/Video-to-HLS?style=social)](https://github.com/ToonTamilIndia/Video-to-HLS/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/ToonTamilIndia/Video-to-HLS?style=social)](https://github.com/ToonTamilIndia/Video-to-HLS/network/members)
[![GitHub issues](https://img.shields.io/github/issues/ToonTamilIndia/Video-to-HLS)](https://github.com/ToonTamilIndia/Video-to-HLS/issues)
[![License](https://img.shields.io/github/license/ToonTamilIndia/Video-to-HLS)](https://github.com/ToonTamilIndia/Video-to-HLS/blob/main/LICENSE)

**Transform your video files into HTTP Live Streaming (HLS) format with unparalleled ease and control!** 🌐

`Video-to-HLS` (V2HLS) is a powerful and flexible Python-based tool that leverages the might of FFmpeg to convert your standard video files into adaptive bitrate HLS streams. This script is designed for content creators, web developers, streaming enthusiasts, and anyone looking to deliver high-quality, resilient video experiences across various devices and network conditions. It supports multiple audio tracks, subtitles, automatic thumbnail generation, and even offers an optional deployment feature to GitHub Pages. 🌟

## ✨ Core Features

* **🎞️ Adaptive Bitrate Streaming (ABS):** Automatically generates multiple video quality renditions (e.g., 1080p, 720p, 480p) from your source video. This allows players to dynamically switch between quality levels, ensuring the best possible viewing experience for users based on their current internet speed and device capabilities.
* **🎧 Multi-Audio Track Support:** Intelligently detects and processes all embedded audio tracks from your source video. Each track is converted into its own HLS audio rendition, allowing users to select their preferred language or audio commentary.
* **📜 Subtitle Integration:** Extracts embedded subtitle tracks (e.g., SRT, ASS) from the source video and converts them into the WebVTT (`.vtt`) format, which is standard for HLS. This makes your content accessible to a wider audience.
* **🖼️ Automatic Thumbnail Generation:** Creates a high-quality thumbnail image from a specified point in your video, perfect for use as a poster image or preview in video players and listings.
* **⚙️ Highly Configurable via `config.json`:**
    * **Custom Video Variants:** Define your own set of target resolutions and bitrates.
    * **FFmpeg Paths:** Specify custom paths for `ffmpeg` and `ffprobe` if they are not in your system's PATH.
    * **Audio Bitrate:** Set a default bitrate for all transcoded audio tracks.
    * **FFmpeg Preset:** Choose an encoding preset (e.g., `ultrafast`, `medium`, `slow`) to balance encoding speed with output quality/size.
    * **Segment Duration:** Control the length of individual HLS segments.
    * **Smart Upscaling Prevention:** The script automatically skips generating video renditions that would require upscaling the source video, saving processing time and ensuring quality.
* **🚀 Optional GitHub Pages, Archive Deployment:** A convenient feature to automatically deploy your generated HLS content (playlists and segments) to a specified GitHub Pages repository and branch or Archive, making it instantly available for web playback.
* **🖥️ Intuitive Command-Line Interface (CLI):** A clear and easy-to-use CLI allows for straightforward operation and seamless integration into automated scripts or workflows.
* **📝 Comprehensive Logging:** Provides detailed, real-time logging of the entire conversion process, including FFmpeg commands executed. Verbose mode (`-v`) offers even more insight for debugging.
* **🐍 Python-Powered & Cross-Platform:** Written in Python, making it compatible with Windows, macOS, and Linux systems where Python and FFmpeg are available.
* **📦 Organized Output Structure:** Generates a clean, well-organized directory structure for all HLS files, including the master playlist, individual variant playlists, video/audio segments, and subtitle files.

## 📋 Table of Contents

1.  [🌟 Why V2HLS? The Advantages](#-why-v2hls-the-advantages)
2.  [🚀 Getting Started](#-getting-started)
    * [Prerequisites: The Essentials](#prerequisites-the-essentials-️)
        * [Python 3.7+](#1-python-37-)
        * [FFmpeg & FFprobe](#2-ffmpeg--ffprobe-%EF%B8%8F)
        * [Git (for Deployment)](#3-git-for-deployment--optional)
    * [Installation & Setup](#installation--setup-%EF%B8%8F)
3.  [🔧 Configuration Deep Dive (`config.json`)](#-configuration-deep-dive-configjson)
    * [Locating `config.json`](#locating-configjson)
    * [Detailed Parameter Breakdown](#detailed-parameter-breakdown)
        * [`ffmpeg_path`](#ffmpeg_path-string)
        * [`ffprobe_path`](#ffprobe_path-string)
        * [`video_variants`](#video_variants-object)
        * [`default_audio_bitrate`](#default_audio_bitrate-string)
        * [`default_ffmpeg_preset`](#default_ffmpeg_preset-string)
        * [`default_segment_duration`](#default_segment_duration-integer)
        * [`github_deployment`](#github_deployment-object)
    * [Environment Variables for GitHub Deployment](#environment-variables-for-github-deployment-)
4.  [⚙️ How to Use V2HLS (CLI Usage)](#%EF%B8%8F-how-to-use-v2hls-cli-usage)
    * [Basic Command Structure](#basic-command-structure)
    * [Positional Arguments](#positional-arguments)
    * [Optional Arguments (Flags)](#optional-arguments-flags)
        * [Video Quality Selection (`-vq`, `--video-qualities`)](#video-quality-selection--vq---video-qualities)
        * [Segment Duration (`-sd`, `--segment-duration`)](#segment-duration--sd---segment-duration)
        * [FFmpeg Preset (`-p`, `--preset`)](#ffmpeg-preset--p---preset)
        * [Thumbnail Control (`--no-thumbnail`, `--thumbnail-time`)](#thumbnail-control---no-thumbnail---thumbnail-time)
        * [GitHub Pages Deployment (`--deploy` & `--gh-*` flags)](#github-pages-deployment---deploy----gh--flags)
        * [Verbose Logging (`-v`, `--verbose`)](#verbose-logging--v---verbose)
        * [Getting Help (`-h`, `--help`)](#getting-help--h---help)
    * [Practical Usage Examples](#practical-usage-examples)
5.  [🔄 The V2HLS Workflow: Under the Hood](#-the-v2hls-workflow-under-the-hood)
6.  [🗂️ Understanding the Output](#%EF%B8%8F-understanding-the-output)
    * [Directory Structure Example](#directory-structure-example)
    * [Key Files Explained](#key-files-explained)
7.  [▶️ Playing Your HLS Streams](#%EF%B8%8F-playing-your-hls-streams)
    * [Web-Based Players](#web-based-players)
    * [Desktop/Mobile Players](#desktopmobile-players)
    * [Basic HTML Example with HLS.js](#basic-html-example-with-hlsjs)
8.  [🛠️ Advanced Customization & Tips](#%EF%B8%8F-advanced-customization--tips)
    * [Optimizing Video Variants](#optimizing-video-variants-video_variants-in-configjson)
    * [Choosing the Right FFmpeg Preset](#choosing-the-right-ffmpeg-preset-default_ffmpeg_preset)
    * [Segment Duration Considerations](#segment-duration-considerations-default_segment_duration)
9.  [🤔 Troubleshooting Common Issues](#-troubleshooting-common-issues)
10. [📜 Script Internals: A Glimpse for Developers](#-script-internals-a-glimpse-for-developers)
11. [🤝 Contributing to V2HLS](#-contributing-to-v2hls)
12. [⚖️ License](#%EF%B8%8F-license)
13. [🙏 Acknowledgements](#-acknowledgements)

---

## 🌟 Why V2HLS? The Advantages

* **Simplicity:** Converts complex FFmpeg operations into simple CLI commands.
* **Automation:** Handles multi-rendition, multi-audio, and subtitle processing automatically.
* **Quality & Efficiency:** Leverages FFmpeg's robust encoding capabilities.
* **Accessibility:** By supporting subtitles and multiple audio tracks, your content reaches a broader audience.
* **Flexibility:** Highly configurable to suit diverse needs and content types.
* **Open Source:** Free to use, modify, and distribute.

---

## 🚀 Getting Started

Follow these steps to get V2HLS up and running on your system.

### Prerequisites: The Essentials 🛠️

Before you begin, ensure you have the following software installed and correctly configured on your system:

#### 1. Python 3.7+ 🐍

V2HLS is a Python script and requires Python 3.7 or a newer version.

* **Check your Python version:**
    Open your terminal or command prompt and type:
    ```bash
    python --version
    # or, if you have multiple Python versions installed:
    python3 --version
    ```
* **Install Python:** If you don't have Python or need a newer version, download it from the [official Python website](https://www.python.org/downloads/).
    * During installation on Windows, ensure you check the box that says **"Add Python to PATH"**.

#### 2. FFmpeg & FFprobe 🎞️🔊

FFmpeg is the core engine V2HLS uses for all video and audio processing tasks. FFprobe (which comes bundled with FFmpeg) is used to analyze media files.

* **Download FFmpeg:** Get the latest static builds for your operating system from [ffmpeg.org](https://ffmpeg.org/download.html).
* **Installation & PATH Setup:**
    * **Windows:**
        1.  Download the FFmpeg ZIP file.
        2.  Extract it to a directory (e.g., `C:\ffmpeg`).
        3.  Add the `bin` subdirectory (e.g., `C:\ffmpeg\bin`) to your system's PATH environment variable.
            * Search for "environment variables" in the Windows search bar.
            * Click "Edit the system environment variables".
            * In the System Properties window, click the "Environment Variables..." button.
            * Under "System variables", find the variable named `Path` and select it. Click "Edit...".
            * Click "New" and add the path to your FFmpeg `bin` directory.
            * Click OK on all open dialogs.
    * **macOS (using Homebrew - recommended):**
        ```bash
        brew install ffmpeg
        ```
        Homebrew will handle the installation and PATH configuration.
    * **Linux (using package managers):**
        * Debian/Ubuntu:
            ```bash
            sudo apt update
            sudo apt install ffmpeg
            ```
        * Fedora:
            ```bash
            sudo dnf install ffmpeg
            ```
        * Arch Linux:
            ```bash
            sudo pacman -S ffmpeg
            ```
* **Verify FFmpeg/FFprobe Installation:**
    Open a *new* terminal/command prompt window (important after PATH changes) and type:
    ```bash
    ffmpeg -version
    ffprobe -version
    ```
    If these commands display version information, FFmpeg and FFprobe are correctly installed and accessible. If not, double-check your PATH configuration or specify the direct paths in `config.json` (see [Configuration Deep Dive (`config.json`)](#configuration-deep-dive-configjson-)).

#### 3. Git (for Deployment) 🌿 (Optional)

If you intend to use the GitHub Pages deployment feature (`--deploy`), you must have Git installed.

* **Download Git:** Get it from [git-scm.com](https://git-scm.com/downloads).
* **Verify Git Installation:**
    ```bash
    git --version
    ```

### Installation & Setup ⚙️

1.  **Clone the Repository:**
    Open your terminal or command prompt, navigate to the directory where you want to store the project, and clone the V2HLS repository from GitHub:
    ```bash
    git clone https://github.com/ToonTamilIndia/Video-to-HLS.git
    ```
    This will create a `Video-to-HLS` directory containing the script and configuration file.

2.  **Navigate to the Project Directory:**
    ```bash
    cd Video-to-HLS
    ```

3.  **Review Configuration (Highly Recommended):**
    Before your first run, open the `config.json` file (located in the `Video-to-HLS` directory) in a text editor.
    * Verify the `ffmpeg_path` and `ffprobe_path`. If FFmpeg/FFprobe are in your system PATH, the defaults (`"ffmpeg"` and `"ffprobe"`) should work. Otherwise, update these with the full paths to the executables.
    * Familiarize yourself with other settings. See the [Configuration Deep Dive (`config.json`)](#configuration-deep-dive-configjson-) section for details.

4.  **Set up a Virtual Environment (Recommended Best Practice):**
    Using a Python virtual environment helps manage dependencies and avoid conflicts with other Python projects or system-wide packages.
    ```bash
    # Create a virtual environment (e.g., named .venv)
    python3 -m venv .venv

    # Activate the virtual environment
    # On Windows (Git Bash or PowerShell):
    source .venv/Scripts/activate
    # On macOS/Linux:
    source .venv/bin/activate
    ```
    You'll need to activate the virtual environment each time you open a new terminal session to work on this project.

5.  **Install Dependencies (If Any):**
    Currently, `main.py` primarily uses Python's standard library. If future versions introduce external Python packages, they would be listed in a `requirements.txt` file. You would install them using pip:
    ```bash
    # Example: if requirements.txt exists
    # pip install -r requirements.txt
    ```


6. **Deploy and Edit `workers.js` on Cloudflare (for Archive Deployment)**

To deploy and update the `workers.js` file on Cloudflare using Cloudflare Workers:

#### Initial Deployment

1. **Install Wrangler CLI** (Cloudflare’s developer tool):

   ```bash
   npm install -g wrangler
   ```

2. **Initialize a Cloudflare Workers project**:

   ```bash
   wrangler init my-worker
   cd my-worker
   ```

3. **Replace the default script** with your `workers.js` file:

   * Overwrite `./src/index.js` (or `index.ts` if using TypeScript) with your custom `workers.js` content.

4. **Configure `wrangler.toml`**:

   ```toml
   name = "your-worker-name"
   type = "javascript"

   account_id = "your-cloudflare-account-id"
   workers_dev = true
   compatibility_date = "2025-05-23"
   ```

5. **Publish the Worker**:

   ```bash
   wrangler publish
   ```

#### Editing and Redeploying

To make changes to your deployment:

1. **Edit your `workers.js`**:

   * Update the code in your local `src/index.js` (or wherever you placed the script).

2. **Test Locally (Optional)**:

   ```bash
   wrangler dev
   ```

3. **Redeploy**:

   ```bash
   wrangler publish
   ```
Cloudflare will automatically update the deployed Worker with the latest version of your script.
If you prefer to **deploy and edit `workers.js` via the Cloudflare website** (without using Wrangler CLI), here’s a clear step-by-step guide:

---

🚀 **Deploy and Edit `workers.js` on Cloudflare via Website**

#### ✅ Initial Deployment

1. **Log in to Cloudflare**
   Go to: [https://dash.cloudflare.com](https://dash.cloudflare.com)

2. **Navigate to Workers & Pages**

   * Click on **“Workers & Pages”** in the sidebar.
   * Click **“Create Application”** > **“Create Worker”**.

3. **Set Up Your Worker**

   * Name your Worker (e.g., `archive-deployer`).
   * You’ll see a code editor in the browser.

4. **Replace the default code**

   * Delete the default code in the editor.
   * Paste the contents of your `workers.js` file.

5. **Test Your Worker**

   * Use the **"Quick Edit"** tab to run test requests.
   * Make sure your Worker behaves as expected.

6. **Save and Deploy**

   * Click **“Save and Deploy”** to publish your Worker live.

---

#### 🔄 Edit and Redeploy Later

1. **Go back to your Worker**

   * From the Cloudflare dashboard, go to **Workers & Pages**.
   * Click on your Worker (e.g., `archive-deployer`).

2. **Edit Code**

   * Click **“Quick Edit”**.
   * Modify the code directly in the browser editor.

3. **Save and Redeploy**

   * After making changes, click **“Save and Deploy”** again.
   * Your changes go live immediately.

---

You are now fully set up and ready to use V2HLS! 🎉

---

## 🔧 Configuration Deep Dive (`config.json`)

V2HLS's behavior is extensively controlled by the `config.json` file. This JSON file allows you to customize default settings for FFmpeg paths, video quality renditions, audio processing, segment duration, and GitHub deployment options without modifying the script itself.

### Locating `config.json`

The `config.json` file is located in the root directory of the cloned `Video-to-HLS` repository. The script expects to find it here. If the file is missing or contains invalid JSON, V2HLS will fall back to a set of internal default values (defined as `DEFAULT_CONFIG` in `main.py`).

Here's an example of the `config.json` structure provided with the repository:
```json
{
  "ffmpeg_path": "ffmpeg",
  "ffprobe_path": "ffprobe",
  "video_variants": {
    "144p": {"resolution": "256x144", "bitrate": "300k", "order": 10},
    "240p": {"resolution": "426x240", "bitrate": "500k", "order": 20},
    "360p": {"resolution": "640x360", "bitrate": "800k", "order": 30},
    "480p": {"resolution": "854x480", "bitrate": "1200k", "order": 40},
    "720p": {"resolution": "1280x720", "bitrate": "2500k", "order": 50},
    "1080p": {"resolution": "1920x1080", "bitrate": "4500k", "order": 60},
    "1440p": {"resolution": "2560x1440", "bitrate": "8000k", "order": 70},
    "2160p": {"resolution": "3840x2160", "bitrate": "12000k", "order": 80},
    "4k": {"resolution": "3840x2160", "bitrate": "12000k", "order": 80},
    "4320p": {"resolution": "7680x4320", "bitrate": "25000k", "order": 90},
    "8k": {"resolution": "7680x4320", "bitrate": "40000k", "order": 90}
  },
  "default_audio_bitrate": "128k",
  "default_ffmpeg_preset": "medium",
  "default_segment_duration": 6,
  "github_deployment": {
    "enabled": true,
    "default_branch": "main",
    "temp_deploy_dir": "_deploy_tmp"
  },
  "archive_deployment": {
        "enabled": true,
        "max_workers": 5,
        "worker_url": "",
        "base_archive_url": "https://archive.org/download/{identifier}"
    }
}
}
````

### Detailed Parameter Breakdown

#### `ffmpeg_path` (string)

**Description:** Specifies the command or full path to the `ffmpeg` executable.
**Default:** `"ffmpeg"`
**Usage:** If `ffmpeg` is in your system's PATH, the default value is sufficient. If FFmpeg is installed in a custom location, provide the absolute path.
**Examples:**

  * Linux/macOS: `"/usr/local/bin/ffmpeg"` or `"/opt/ffmpeg/ffmpeg"`
  * Windows: `"C:\\ffmpeg\\bin\\ffmpeg.exe"` (note the double backslashes for JSON compatibility, or use single forward slashes: `"C:/ffmpeg/bin/ffmpeg.exe"`)

#### `ffprobe_path` (string)

**Description:** Specifies the command or full path to the `ffprobe` executable.
**Default:** `"ffprobe"`
**Usage:** Similar to `ffmpeg_path`. `ffprobe` is usually located in the same directory as `ffmpeg`.
**Examples:**

  * Linux/macOS: `"/usr/local/bin/ffprobe"`
  * Windows: `"C:\\ffmpeg\\bin\\ffprobe.exe"`

#### `video_variants` (object)

**Description:** This is the heart of your adaptive bitrate setup. It's an object where each key is a human-readable name for a video quality variant (e.g., `"1080p"`, `"720p_high_fps"`), and the value is another object defining its properties.
**Properties for each variant:**

  * `resolution` (string): The target video resolution in `widthxheight` format (e.g., `"1920x1080"`). Ensure this maintains the desired aspect ratio (commonly 16:9).
  * `bitrate` (string): The target video bitrate for this variant. Use `k` for kilobits per second (e.g., `"4500k"`) or `M` for megabits per second (e.g., `"4.5M"`). Higher bitrates generally mean better quality but larger file sizes.
  * `order` (integer): A numeric value used by the script internally, potentially for sorting or prioritizing variants. Lower numbers might be processed first or appear earlier in logs. The master playlist typically sorts renditions by bandwidth for player adaptation.
    **Important Notes:**
  * **No Upscaling:** V2HLS will not create a variant if its specified resolution (height) is greater than the source video's height. This prevents quality degradation from upscaling.
  * **Bitrate Selection:** Choosing appropriate bitrates for each resolution is crucial. Too low, and quality suffers; too high, and bandwidth is wasted. Research recommended bitrates for H.264 encoding at various resolutions.
  * **Common Resolutions (16:9):**
      * `256x144` (144p)
      * `426x240` (240p)
      * `640x360` (360p)
      * `854x480` (480p)
      * `1280x720` (720p HD)
      * `1920x1080` (1080p Full HD)
      * `2560x1440` (1440p QHD/2K)
      * `3840x2160` (2160p UHD/4K)
  * **Adding/Removing Variants:** Simply add or remove entries in the `video_variants` object to customize your rendition ladder.

#### `default_audio_bitrate` (string)

**Description:** The default target bitrate for all transcoded audio tracks.
**Default:** `"128k"`
**Usage:** AAC (the typical HLS audio codec) at 128 kbps is generally good for stereo audio. For speech-only content, you might use `"96k"` or even `"64k"`. For high-fidelity music, consider `"192k"` or `"256k"`.
**Format:** Use `k` for kilobits per second (e.g., `"128k"`).

#### `default_ffmpeg_preset` (string)

**Description:** The FFmpeg encoding preset to use for video transcoding. This setting significantly impacts the balance between encoding speed, output file size, and visual quality.
**Default:** `"medium"`
**Values (from fastest to slowest, generally trading speed for compression efficiency):**

  * `ultrafast`
  * `superfast`
  * `veryfast`
  * `faster`
  * `fast`
  * `medium` (good balance)
  * `slow`
  * `slower`
  * `veryslow` (best compression, but very time-consuming)
    **Recommendation:** Start with `medium`. If encoding takes too long, try `fast` or `veryfast`. If quality at a given bitrate is paramount and you have time, try `slow`.

#### `default_segment_duration` (integer)

**Description:** The target duration (in seconds) for individual HLS media segments (`.ts` files).
**Default:** `6`
**Usage:** Common values range from 2 to 10 seconds.

  * **Shorter segments (e.g., 2-4s):** Can lead to lower latency in live streams (not the primary focus of this VOD script but relevant to HLS in general), faster startup times for VOD, and quicker seeking, as the player only needs to download a small segment to start. However, they result in more HTTP requests and slightly higher overhead due to more frequent playlist updates and segment headers.
  * **Longer segments (e.g., 6-10s):** Reduce the number of files and HTTP requests, potentially improving CDN efficiency. They might lead to slightly slower startup and seeking.
    **Recommendation:** `6` seconds is a common and good default. Adjust based on your specific delivery needs and audience network characteristics.

#### `github_deployment` (object)

**Description:** Contains settings related to the optional GitHub Pages deployment feature.
**Properties:**

  * `enabled` (boolean):
      * **Default:** `true` (in the provided `config.json`, was `false` in the script's internal `DEFAULT_CONFIG`).
      * **Usage:** Set to `true` to enable the `--deploy` CLI flag functionality. If `false`, the script will ignore the `--deploy` flag and any related `--gh-*` arguments, and a warning will be logged if deployment is attempted.
  * `default_branch` (string):
      * **Default:** `"main"`
      * **Usage:** The default Git branch to which the HLS content will be pushed if not specified via the `--gh-branch` CLI argument or the `GITHUB_BRANCH` environment variable. Common choices include `"main"`, `"master"`, or a dedicated branch like `"gh-pages"`.
      * **Note on GitHub Pages Source:** Ensure your GitHub repository settings are configured to serve GitHub Pages from this branch (and often from the `/ (root)` or `/docs` folder within that branch).
  * `temp_deploy_dir` (string):
      * **Default:** `"_deploy_tmp"`
      * **Usage:** The name of a temporary directory that V2HLS will create (typically alongside your output directory) to stage files for Git deployment. This directory is usually removed after successful deployment, but might remain if an error occurs.

### Environment Variables for GitHub Deployment 🔑

For the GitHub Pages deployment feature, V2HLS can use environment variables for authentication and repository details. These are particularly useful for CI/CD pipelines or to avoid repeatedly typing credentials. CLI arguments will override these if both are provided.

  * `GITHUB_USERNAME`: Your GitHub username (e.g., `ToonTamilIndia`).
  * `GITHUB_REPO`: The name of the GitHub repository where you want to deploy the HLS content (e.g., `Video-to-HLS-Output`).
  * `GITHUB_TOKEN`: A GitHub Personal Access Token (PAT).
      * **Crucial:** This token needs the `repo` scope (or `public_repo` for public repositories) to allow pushing changes.
      * **Security:** Treat your PAT like a password. Do NOT hardcode it into scripts or `config.json`. Environment variables are a safer way to handle it.
      * Generate a PAT from your GitHub account: Settings \> Developer settings \> Personal access tokens.
  * `GITHUB_BRANCH`: The target branch in your GitHub repository for deployment (e.g., `gh-pages`, `main`).

**Setting Environment Variables (Examples):**

  * Linux/macOS (in your `.bashrc`, `.zshrc`, or current session):
    ```bash
    export GITHUB_USERNAME="YourGitHubUser"
    export GITHUB_REPO="YourTargetRepoName"
    export GITHUB_TOKEN="your_github_pat_here"
    export GITHUB_BRANCH="gh-pages"
    ```
  * Windows (PowerShell):
    ```powershell
    $Env:GITHUB_USERNAME = "YourGitHubUser"
    $Env:GITHUB_REPO = "YourTargetRepoName"
    $Env:GITHUB_TOKEN = "your_github_pat_here"
    $Env:GITHUB_BRANCH = "gh-pages"
    # To make them persistent across sessions, use System Properties > Environment Variables.
    ```


### ✅ `archive_deployment` (object)

**Description:** Contains settings for the optional Internet Archive deployment feature.
**Properties:**

* `enabled` (boolean):

  * **Default:** `true`
  * **Usage:** Enables the `--archive` CLI flag. If `false`, any archive deployment commands will be ignored, and a warning will be shown if attempted.

* `max_workers` (integer):

  * **Default:** `5`
  * **Usage:** Number of parallel threads to use for uploading files to Internet Archive.

* `worker_url` (string):

  * **Usage:** Proxy/worker URL prepended to file paths in `.m3u8` playlists to optimize delivery through Cloudflare Workers.

---

### 🔐 Environment Variables for Internet Archive Deployment

To avoid hardcoding sensitive credentials, you can use environment variables:

* `ARCHIVE_ACCESS_KEY`: Your Internet Archive access key.
* `ARCHIVE_SECRET_KEY`: Your Internet Archive secret key.

**Setting Examples:**

* Linux/macOS:

  ```bash
  export ARCHIVE_ACCESS_KEY="your_access_key"
  export ARCHIVE_SECRET_KEY="your_secret_key"
  ```

* Windows (PowerShell):

  ```powershell
  $Env:ARCHIVE_ACCESS_KEY = "your_access_key"
  $Env:ARCHIVE_SECRET_KEY = "your_secret_key"
  ```

---


-----

## ⚙️ How to Use V2HLS (CLI Usage)

V2HLS is operated via its command-line interface. Open your terminal or command prompt, navigate to the `Video-to-HLS` directory (and activate your virtual environment if you're using one).

### Basic Command Structure

The fundamental way to run the script is:

```bash
python main.py <input_video_file> <output_directory> [OPTIONS]
```

Or, if you've made `main.py` executable (e.g., `chmod +x main.py` on Linux/macOS):

```bash
./main.py <input_video_file> <output_directory> [OPTIONS]
```

### Positional Arguments

These are required for every run:

  * `input` (string):
    The full path to the source video file you want to convert.
    Example: `my_videos/holiday_footage.mp4`, `../input/lecture.mkv`, `C:\Users\Me\Videos\project_video.mov`
    If the path contains spaces, enclose it in quotes: `"path/to/my video.mp4"`
  * `output` (string):
    The full path to the directory where V2HLS will save all the generated HLS files (master playlist, variant playlists, segments, thumbnail).
    If the directory doesn't exist, V2HLS will attempt to create it.
    Example: `hls_output/holiday_stream`, `public_html/streams/lecture1`, `"D:\Streaming Content\My Movie HLS"`

### Optional Arguments (Flags)

These flags allow you to customize the conversion process for a specific run, often overriding defaults set in `config.json`.

#### Video Quality Selection (`-vq`, `--video-qualities`)

  * **Format:** `STRING` (comma-separated list of quality names)
  * **Default:** None (If not specified, V2HLS processes all variants from `config.json` that are not upscales of the input video).
  * **Description:** Allows you to specify exactly which video quality renditions to generate. The names must match the keys defined in the `video_variants` section of your `config.json` (e.g., `1080p`, `720p`, `480p`).
  * **Example:**
    ```bash
    python main.py video.mp4 output_folder -vq "1080p,480p,240p"
    ```
    This will only generate 1080p, 480p, and 240p renditions (if they are valid for the input video and defined in `config.json`). Invalid names or names leading to upscaling will be skipped with a warning.

#### Segment Duration (`-sd`, `--segment-duration`)

  * **Format:** `INTEGER` (seconds)
  * **Default:** Value from `config.json` (`default_segment_duration`, typically `6`).
  * **Description:** Overrides the default HLS segment duration for this specific run.
  * **Example:**
    ```bash
    python main.py video.mp4 output_folder -sd 4
    ```
    This will generate HLS segments that are approximately 4 seconds long.

#### FFmpeg Preset (`-p`, `--preset`)

  * **Format:** `STRING` (FFmpeg preset name)
  * **Default:** Value from `config.json` (`default_ffmpeg_preset`, typically `medium`).
  * **Description:** Overrides the default FFmpeg encoding preset for this run. Choose from `ultrafast`, `superfast`, `veryfast`, `faster`, `fast`, `medium`, `slow`, `slower`, `veryslow`.
  * **Example:**
    ```bash
    python main.py video.mp4 output_folder -p "fast"
    ```
    This uses the `fast` preset for quicker encoding, potentially at the cost of some compression efficiency.

#### Thumbnail Control (`--no-thumbnail`, `--thumbnail-time`)

  * `--no-thumbnail`:
      * **Action:** Disables thumbnail generation for this run.
      * **Default:** Thumbnails are generated by default.
      * **Example:**
        ```bash
        python main.py video.mp4 output_folder --no-thumbnail
        ```
  * `--thumbnail-time` (string):
      * **Default:** `"00:00:05"` (5 seconds into the video).
      * **Description:** Specifies the timestamp in the video from which to extract the thumbnail.
      * **Format:**
          * `HH:MM:SS` (e.g., `"00:01:23"` for 1 minute 23 seconds)
          * `S` (e.g., `"83"` for 83 seconds)
      * **Example:**
        ```bash
        python main.py video.mp4 output_folder --thumbnail-time "00:00:15.500"
        ```

#### GitHub Pages Deployment (`--deploy` & `--gh-*` flags)

  * `--deploy`:
      * **Action:** Activates the deployment of the generated HLS output folder to GitHub Pages.
      * **Prerequisites:**
          * `github_deployment.enabled` must be `true` in `config.json`.
          * Git must be installed.
          * GitHub credentials/repository details must be provided via environment variables or the `--gh-*` CLI arguments below.
      * **Example:**
        ```bash
        python main.py video.mp4 output_folder --deploy
        ```
  * `--gh-user GITHUB_USER` (string):
    Your GitHub username. Overrides `GITHUB_USERNAME` environment variable.
  * `--gh-repo GITHUB_REPO` (string):
    The name of your GitHub repository for deployment. Overrides `GITHUB_REPO` environment variable.
  * `--gh-token GITHUB_TOKEN` (string):
    Your GitHub Personal Access Token (PAT) with `repo` scope. Overrides `GITHUB_TOKEN` environment variable.
    ⚠️ **Security Warning:** Providing a PAT directly on the command line can be a security risk as it might be stored in your shell's history. Using environment variables is generally safer for tokens.
  * `--gh-branch GITHUB_BRANCH` (string):
    The GitHub branch to deploy to. Overrides `GITHUB_BRANCH` environment variable and `default_branch` in `config.json`.
  * **Example (full deployment command):**
    ```bash
    python main.py video.mp4 deploy_output --deploy \
        --gh-user "MyGitHubUser" \
        --gh-repo "MyHLSContentHost" \
        --gh-token "mypersonalaccesstokenvalue" \
        --gh-branch "hls-streams"
    ```

#### Verbose Logging (`-v`, `--verbose`)

  * **Action:** Enables detailed debug logging to the console. This is extremely helpful for troubleshooting, as it shows the exact FFmpeg/FFprobe commands being executed and their full output.
  * **Example:**
    ```bash
    python main.py video.mp4 output_folder -v
    ```

#### Getting Help (`-h`, `--help`)

  * **Action:** Displays a comprehensive help message listing all available command-line arguments, their descriptions, and default values.
  * **Example:**
    ```bash
    python main.py -h
    ```

### Practical Usage Examples

  * **Basic Conversion (Defaults):**
    Convert `input.mp4` to HLS in `output_hls`, using all settings from `config.json`.
    ```bash
    python main.py "path/to/input.mp4" "path/to/output_hls"
    ```
  * **Specific Qualities & Faster Preset:**
    Convert `promo_video.mov`, generate only `720p` and `360p` renditions, use the `faster` preset, and store in `web_streams/promo`.
    ```bash
    python main.py "videos/promo_video.mov" "web_streams/promo" -vq "720p,360p" -p "faster"
    ```
  * **Custom Segment Duration & Thumbnail Time:**
    Convert `lecture_series_ep1.mkv`, use 2-second segments for potentially faster seeking, grab thumbnail from 10s mark.
    ```bash
    python main.py "lectures/lecture_series_ep1.mkv" "hls_content/ep1" -sd 2 --thumbnail-time "10"
    ```
  * **Full Process with Deployment (using environment variables for credentials):**
    Convert `final_cut.mp4`, generate all suitable qualities, deploy to GitHub Pages (assuming `GITHUB_USERNAME`, `GITHUB_REPO`, `GITHUB_TOKEN`, `GITHUB_BRANCH` are set as environment variables).
    ```bash
    python main.py "project_files/final_cut.mp4" "deploy_candidate_hls" --deploy -v
    ```
    The `-v` will show detailed logs, including Git commands during deployment.

-----

## 🔄 The V2HLS Workflow: Under the Hood

Understanding the sequence of operations V2HLS performs can be helpful for troubleshooting and appreciating its capabilities:

1.  **🎬 Initialization & Configuration:**

      * The script starts, parses all command-line arguments provided by the user.
      * It loads the `config.json` file. If not found, it uses internal defaults. CLI arguments override `config.json` settings for the current run.
      * Logging is configured (INFO level by default, DEBUG if `-v` is used).

2.  **🔍 Input Video Analysis (Metadata Probing):**

      * The script executes `ffprobe` on the specified input video file.
      * `ffprobe` analyzes the video and outputs its metadata in JSON format. This metadata includes:
          * Video stream details: resolution (width, height), codec, frame rate, duration.
          * Audio stream details: codec, channels, language tags (if present), titles.
          * Subtitle stream details: codec, language tags (if present), titles.
      * This information is crucial for subsequent steps, especially for determining the input video's resolution (to avoid upscaling) and identifying all available audio and subtitle tracks.

3.  **🎞️ Video Rendition Generation Loop:**

      * The script determines which video variants to generate based on:
          * The `video_variants` defined in `config.json`.
          * The qualities specified via the `-vq` CLI argument (if used).
          * The input video's actual resolution (to skip any variants that would require upscaling).
      * For each selected video variant:
          * A dedicated subdirectory is created within the main output folder (e.g., `output_dir/video_1080p/`).
          * An `ffmpeg` command is constructed and executed. This command typically includes:
              * `-i <input_file>`: Specifies the input video.
              * `-map 0:v:0`: Selects the first video stream from the input.
              * `-c:v libx264`: Sets the video codec to H.264 (widely compatible).
              * `-b:v <bitrate>`: Sets the target video bitrate for this variant.
              * `-s <resolution>`: Sets the target video resolution.
              * `-profile:v main -level:v 4.0`: Sets H.264 profile and level for compatibility.
              * `-preset <ffmpeg_preset>`: Applies the chosen encoding speed/quality preset.
              * `-force_key_frames "expr:gte(t,n_forced*<segment_duration>)"`: Ensures keyframes are placed at regular intervals aligned with segment boundaries. This is critical for smooth adaptive bitrate switching.
              * `-f hls`: Specifies the output format as HLS.
              * `-hls_time <segment_duration>`: Sets the target duration for HLS segments.
              * `-hls_playlist_type vod`: Indicates a Video-On-Demand playlist.
              * `-hls_segment_filename <path_to_segments>`: Defines the naming pattern for the `.ts` media segment files (e.g., `segment_%05d.ts`).
              * `<path_to_variant_playlist>`: The output path for this variant's M3U8 playlist (e.g., `video_1080p/index.m3u8`).
          * FFmpeg generates the individual M3U8 playlist and all `.ts` video segments for this specific quality level.

4.  **🎧 Audio Rendition Generation Loop:**

      * The script iterates through each audio stream detected by `ffprobe` in the input video.
      * For each audio stream:
          * Language code (e.g., `"eng"`, `"spa"`) and track title are extracted from metadata if available. Defaults are used if not.
          * A dedicated subdirectory is created (e.g., `output_dir/audio_eng_0/`).
          * An `ffmpeg` command is constructed and executed to process this audio stream:
              * `-map 0:a:<stream_index>`: Selects the specific audio stream.
              * `-c:a aac`: Sets the audio codec to AAC (standard for HLS).
              * `-b:a <default_audio_bitrate>`: Sets the target audio bitrate.
              * HLS specific flags (`-f hls`, `-hls_time`, etc.) similar to video are used.
          * FFmpeg generates an audio-only HLS stream (M3U8 playlist and `.ts` audio segments) for this track.

5.  **📜 Subtitle Rendition Generation Loop:**

      * The script iterates through each subtitle stream detected by `ffprobe`.
      * For each subtitle stream:
          * Language code and title are extracted.
          * A dedicated subdirectory is created (e.g., `output_dir/sub_eng_0/`).
          * An `ffmpeg` command is executed to extract the subtitle stream and convert it directly into WebVTT (`.vtt`) format.
              * `-map 0:s:<stream_index>`: Selects the specific subtitle stream.
              * `-c:s webvtt`: Specifies the output codec as WebVTT.
          * The output is a single `.vtt` file for this subtitle track (e.g., `sub_eng_0/subtitles_eng_0.vtt`). HLS typically references entire VTT files rather than segmented ones.

6.  **M3U8 Master Playlist Creation:**

      * Once all individual video, audio, and subtitle renditions are processed, V2HLS generates the crucial master M3U8 playlist (e.g., `output_dir/master.m3u8`). This is the primary file that HLS players will load.
      * The master playlist is a text file containing directives that describe all available streams:
          * `#EXTM3U`: Indicates it's an M3U playlist.
          * `#EXT-X-VERSION:3` (or higher): Specifies the HLS protocol version.
          * **Audio Renditions (`#EXT-X-MEDIA:TYPE=AUDIO`):** For each processed audio track, an entry is added defining its language, name, group ID (e.g., `"audio-aac"`), whether it's the default track, and the URI to its individual M3U8 playlist.
          * **Subtitle Renditions (`#EXT-X-MEDIA:TYPE=SUBTITLES`):** For each processed subtitle track, an entry defines its language, name, group ID (e.g., `"subs"`), and the URI to its `.vtt` file.
          * **Video Renditions (`#EXT-X-STREAM-INF`):** For each generated video quality variant, an entry specifies:
              * `BANDWIDTH`: The peak bitrate for this stream (calculated from video bitrate + default audio bitrate).
              * `RESOLUTION`: The resolution of this video variant.
              * `CODECS`: A string indicating the video and audio codecs used (e.g., `"avc1.4D401F,mp4a.40.2"` for H.264 Main Profile & AAC-LC).
              * `AUDIO`: Links to the audio group ID (e.g., `"audio-aac"`).
              * `SUBTITLES`: Links to the subtitles group ID (e.g., `"subs"`).
          * This is followed by the relative URI to the video variant's individual M3U8 playlist.
      * Video streams are typically sorted by bandwidth in the master playlist to assist players in making an optimal initial stream selection.

7.  **🖼️ Thumbnail Generation (Optional):**

      * If thumbnail generation is enabled (default, or not disabled by `--no-thumbnail`), an `ffmpeg` command is executed:
          * `-ss <thumbnail_time>`: Seeks to the specified timestamp in the input video.
          * `-i <input_file>`: Specifies the input video.
          * `-vframes 1`: Extracts only one frame.
          * `-q:v 2`: Sets the quality for the JPEG output (2 is high quality).
      * The output is a single JPEG image (e.g., `output_dir/input_filename_thumbnail.jpg`).

8.  **🚀 GitHub Pages Deployment (Optional):**

      * If the `--deploy` flag is used and deployment is enabled and configured:
          * The script creates a temporary directory (e.g., `_deploy_tmp` next to the output directory).
          * The entire contents of the HLS output directory are copied into this temporary location.
          * A `.nojekyll` file is created at the root of the content being deployed. This tells GitHub Pages to serve files from directories starting with underscores (which HLS segment folders might, though this script uses names like `video_1080p`). It's a good practice for static site generators.
          * A series of `git` commands are executed (via `run_command`):
              * `git init`: Initializes a new Git repository in the temporary base directory.
              * `git checkout -b <branch>`: Creates or switches to the target deployment branch.
              * `git remote add origin <remote_url>`: Adds the GitHub repository as a remote, using the provided username and token for authentication in the URL.
              * `git add .`: Stages all the HLS content.
              * `git commit -m "Auto deploy HLS files..."`: Commits the changes.
              * `git push --force origin <branch>`: Force-pushes the content to the specified branch on GitHub. The `--force` is used to overwrite the branch content, typical for deployment branches.
          * A success message is logged, including the likely public URL for the `master.m3u8` file on GitHub Pages.

9.  **🏁 Completion & Logging:**

      * Throughout the process, V2HLS logs informative messages about its progress, commands executed, and any warnings or errors.
      * A final success message indicates that HLS packaging is complete and points to the location of the master playlist file.

This detailed workflow ensures that all necessary components for a robust adaptive HLS streaming experience are generated and correctly interlinked.

-----

## 🗂️ Understanding the Output

After V2HLS successfully processes your video, it will create a well-organized directory structure containing all the necessary files for HLS streaming.

### Directory Structure Example

Let's say you ran the command:

```bash
python main.py "my_movie.mp4" "hls_output/my_movie_stream"
```

And `my_movie.mp4` has one 1080p video stream, two audio tracks (English and Spanish), and one English subtitle track. The `video_variants` in your `config.json` include `1080p`, `720p`, and `480p`.

The `hls_output/my_movie_stream` directory might look like this:

```
hls_output/my_movie_stream/
├── master.m3u8                     # The main playlist file players will load
├── my_movie_thumbnail.jpg          # Generated thumbnail image
│
├── video_1080p/                    # Directory for 1080p video rendition
│   ├── index.m3u8                  # Playlist for 1080p video segments
│   ├── segment_00000.ts            # First 1080p video segment
│   ├── segment_00001.ts            # Second 1080p video segment
│   └── ...                         # More 1080p segments
│
├── video_720p/                     # Directory for 720p video rendition
│   ├── index.m3u8                  # Playlist for 720p video segments
│   ├── segment_00000.ts
│   └── ...
│
├── video_480p/                     # Directory for 480p video rendition
│   ├── index.m3u8                  # Playlist for 480p video segments
│   ├── segment_00000.ts
│   └── ...
│
├── audio_eng_0/                    # Directory for the first audio track (English)
│   ├── index.m3u8                  # Playlist for English audio segments
│   ├── segment_00000.ts            # First English audio segment
│   └── ...                         # More English audio segments
│
├── audio_spa_1/                    # Directory for the second audio track (Spanish)
│   ├── index.m3u8                  # Playlist for Spanish audio segments
│   ├── segment_00000.ts
│   └── ...
│
└── sub_eng_0/                      # Directory for the first subtitle track (English)
    └── subtitles_eng_0.vtt         # WebVTT subtitle file for English
```

### Key Files Explained

  * **`master.m3u8` (Master Playlist):**
    This is the most important file. It's the entry point for HLS players.
    It doesn't contain any media itself but lists all available video renditions (with their bandwidth and resolution), audio renditions (languages), and subtitle tracks.
    Players use this file to decide which quality level to start with and to switch between streams adaptively.
  * **`video_<quality>/index.m3u8` (Variant Playlists):**
    Each video quality rendition (e.g., `video_1080p`, `video_720p`) has its own `index.m3u8` playlist.
    These playlists list the actual media segments (`.ts` files) for that specific quality level in chronological order.
    They also contain metadata about the segments, like their duration.
  * **`video_<quality>/segment_XXXXX.ts` (Video Segments):**
    These are the actual chunks of video data, typically a few seconds long (as defined by `segment_duration`).
    They are encoded at the specific resolution and bitrate of their parent variant.
  * **`audio_<lang>_<index>/index.m3u8` (Audio Playlists):**
    Similar to video variant playlists, but for audio-only streams.
    Each audio track (e.g., different languages) gets its own playlist listing its audio segments.
  * **`audio_<lang>_<index>/segment_XXXXX.ts` (Audio Segments):**
    Chunks of audio data for a specific audio track.
  * **`sub_<lang>_<index>/subtitles_<lang>_<index>.vtt` (Subtitle Files):**
    These are WebVTT (Video Text Tracks) files containing the subtitle information (text, timings).
    Unlike video and audio, subtitles in HLS are often referenced as single, complete `.vtt` files per language.
  * **`*_thumbnail.jpg` (Thumbnail Image):**
    A JPEG image extracted from the video, used for previews.

To serve this HLS stream, you would typically upload the entire output directory (e.g., `my_movie_stream` and all its contents) to a web server or CDN. The URL you provide to HLS players would then point to the `master.m3u8` file.

-----

## ▶️ Playing Your HLS Streams

Once you've generated your HLS package with V2HLS, you'll need an HLS-compatible player to watch it.

### Web-Based Players

These are JavaScript libraries that enable HLS playback in web browsers that don't natively support it (most browsers except Safari).

  * **[HLS.js](https://github.com/video-dev/hls.js/):**
    A popular and robust library specifically for HLS playback.
    Relatively lightweight and highly configurable.
  * **[Video.js](https://videojs.com):**
    A comprehensive HTML5 video player framework that supports HLS (often via an HLS plugin or by leveraging native browser support).
    Offers a skinnable UI and a rich plugin ecosystem.
  * **[Shaka Player](https://github.com/shaka-project/shaka-player):**
    Google's open-source player that supports HLS and DASH, with a focus on adaptive streaming and offline playback.
  * **JW Player, TheoPlayer, Bitmovin Player:** Commercial players with advanced features and analytics, also supporting HLS.

### Desktop/Mobile Players

Many modern media players on desktop and mobile devices have native HLS support.

  * **[VLC Media Player](https://www.videolan.org/vlc/):**
    Cross-platform (Windows, macOS, Linux, Android, iOS).
    Excellent HLS support. Simply open the URL to your `master.m3u8` file.
  * **QuickTime Player (macOS):**
    Native HLS support on macOS.
  * **[mpv](https://mpv.io):**
    A free, open-source, and cross-platform media player, highly capable with HLS.
  * **Mobile Apps:** Many video player apps on Android and iOS support HLS streaming.

### Basic HTML Example with HLS.js

Here's a very basic example of how you might embed an HLS stream generated by V2HLS into an HTML page using HLS.js:

1.  **Upload HLS Content:** Ensure your entire HLS output directory (e.g., `my_stream_folder` containing `master.m3u8` and all segment subdirectories) is accessible via a web server (e.g., `https://yourdomain.com/path/to/my_stream_folder/master.m3u8`).
2.  **Create an HTML file:**

<!-- end list -->

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HLS Player Example</title>
    <script src="[https://cdn.jsdelivr.net/npm/hls.js@latest](https://cdn.jsdelivr.net/npm/hls.js@latest)"></script>
    <style>
        #videoPlayer {
            width: 80%;
            max-width: 800px;
            border: 1px solid #ccc;
        }
    </style>
</head>
<body>

    <h1>My HLS Video Stream</h1>
    <video id="videoPlayer" controls></video>

    <script>
        document.addEventListener('DOMContentLoaded', function () {
            var video = document.getElementById('videoPlayer');
            // Replace with the actual URL to YOUR master.m3u8 file
            var videoSrc = '[https://yourdomain.com/path/to/my_stream_folder/master.m3u8](https://yourdomain.com/path/to/my_stream_folder/master.m3u8)'; 

            if (Hls.isSupported()) {
                var hls = new Hls();
                hls.loadSource(videoSrc);
                hls.attachMedia(video);
                hls.on(Hls.Events.MANIFEST_PARSED, function() {
                    // You can uncomment the line below to autoplay if desired
                    // video.play(); 
                });
                hls.on(Hls.Events.ERROR, function (event, data) {
                    if (data.fatal) {
                        switch(data.type) {
                            case Hls.ErrorTypes.NETWORK_ERROR:
                                console.error("Fatal network error encountered: ", data);
                                // try to recover network error
                                hls.startLoad();
                                break;
                            case Hls.ErrorTypes.MEDIA_ERROR:
                                console.error("Fatal media error encountered: ", data);
                                hls.recoverMediaError();
                                break;
                            default:
                                // cannot recover
                                hls.destroy();
                                break;
                        }
                    }
                });
            } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
                // For Safari and other browsers with native HLS support
                video.src = videoSrc;
                video.addEventListener('loadedmetadata', function() {
                    // video.play();
                });
            } else {
                alert('Your browser does not support HLS playback.');
            }
        });
    </script>

</body>
</html>
```

**Key points in the example:**

  * It includes HLS.js from a CDN.
  * It checks if HLS.js is needed or if the browser supports HLS natively (like Safari).
  * **Replace `videoSrc` with the actual URL to your `master.m3u8` file.**
  * Basic error handling for HLS.js is included.

-----

## 🛠️ Advanced Customization & Tips

Beyond the CLI flags and basic `config.json` settings, consider these points for fine-tuning your HLS output:

### Optimizing Video Variants (`video_variants` in `config.json`)

  * **Bitrate Ladder:** The set of resolutions and their corresponding bitrates is often called a "bitrate ladder." A good ladder provides noticeable quality steps without excessive overlap or gaps.
      * Start with your highest desired quality (e.g., 1080p at 4500k).
      * For the next step down (e.g., 720p), aim for a bitrate that offers a good 720p experience (e.g., 2500k-3000k) and is significantly lower than the 1080p bitrate.
      * Continue this for lower resolutions. The lowest tier should be very low bitrate for users on very poor connections (e.g., 240p at 300-500k).
  * **Content Type Matters:**
      * **High-motion content (sports, action):** May require higher bitrates at each resolution to avoid blockiness.
      * **Low-motion content (presentations, talking heads):** Can often achieve good quality at lower bitrates.
  * **Test Your Ladder:** Always test your HLS streams on various devices and network conditions to ensure the adaptive switching works well and quality is acceptable at each level.
  * **FFmpeg CRF (Constant Rate Factor):** While this script uses 2-pass ABR (Average Bitrate) by specifying `-b:v`, for very high-quality archival or less predictable content, FFmpeg's CRF mode is excellent for quality-based encoding (though it makes predicting file size harder). This script is not currently set up for CRF but it's an advanced FFmpeg topic to be aware of.

### Choosing the Right FFmpeg Preset (`default_ffmpeg_preset`)

  * `medium`: The default, offers a good compromise between encoding time and compression efficiency.
  * **Faster presets (`fast`, `veryfast`, `superfast`, `ultrafast`):**
      * Significantly reduce encoding time.
      * Result in larger file sizes for the same visual quality, or slightly lower quality for the same bitrate.
      * Useful for quick previews, testing, or when encoding time is critical.
  * **Slower presets (`slow`, `slower`, `veryslow`):**
      * Dramatically increase encoding time.
      * Achieve better compression, meaning smaller file sizes for the same visual quality, or better quality for the same bitrate.
      * Use when output quality and file size are paramount and you have ample processing time.

### Segment Duration Considerations (`default_segment_duration`)

  * **Apple's Recommendation:** Apple, the creator of HLS, historically recommended 6-second segments. This is a good general-purpose value.
  * **Low Latency HLS (LL-HLS):** For near real-time streaming (more relevant to live events), LL-HLS uses much shorter segments (e.g., \<2 seconds) and partial segment delivery. This script is primarily for VOD, where standard segment durations are fine.
  * **CDN Caching:** Longer segments can sometimes be more CDN-friendly as there are fewer files to cache, but this is usually a minor factor for VOD.
  * **Player Behavior:** Some players might have optimal performance with certain segment lengths.

-----

## 🤔 Troubleshooting Common Issues

If you encounter problems, these tips might help. Always run with `-v` or `--verbose` first to get detailed logs\!

  * **"FFmpeg/FFprobe not found"**

      * **Cause:** The script can't locate the `ffmpeg` or `ffprobe` executables.
      * **Solution:**
          * Ensure FFmpeg is installed correctly.
          * Verify that the directory containing `ffmpeg.exe` (Windows) or `ffmpeg` (macOS/Linux) is in your system's PATH environment variable. Restart your terminal after modifying PATH.
          * Alternatively, provide the full, absolute path to `ffmpeg` and `ffprobe` in your `config.json` file (e.g., `"ffmpeg_path": "C:/ffmpeg/bin/ffmpeg.exe"`).

  * **"Command failed with exit code X" / FFmpeg errors in log**

      * **Cause:** FFmpeg itself encountered an error during processing.
      * **Solution:**
          * Examine the FFmpeg error message in the verbose log output. This is the most crucial piece of information.
          * **Input File:** The input video might be corrupted, use an unsupported codec that your FFmpeg build can't handle, or the path might be incorrect. Try with a known-good, simple `.mp4` file.
          * **Permissions:** Ensure the script has read permission for the input file and read/write/execute permissions for the output directory and any temporary directories.
          * **Disk Space:** Transcoding, especially multiple renditions, can require significant temporary disk space. Ensure you have enough free space on the drive where the output and temp files are being written.
          * **FFmpeg Parameters:** While V2HLS constructs commands, an unusual input file characteristic might lead to an FFmpeg parameter conflict. The verbose log will show the exact command.
          * **Outdated FFmpeg:** An old FFmpeg version might lack features or have bugs. Try updating to a recent stable build.

  * **"No video renditions were generated" or "Skipping {quality\_name}..."**

      * **Cause:** All defined or requested video variants were of a higher resolution than your input video, and the script correctly skipped them to avoid upscaling.
      * **Solution:**
          * Check the actual resolution of your input video.
          * Ensure your `config.json`'s `video_variants` include resolutions appropriate for (i.e., less than or equal to) your input video's resolution.
          * If using `-vq`, select qualities that are not upscales.

  * **GitHub Deployment Fails**

      * **"Deployment skipped: Missing username, repo name, token, or branch":** Provide all necessary `--gh-*` arguments or set the corresponding environment variables.
      * **"Deployment disabled in config.json":** Set `github_deployment.enabled` to `true` in `config.json`.
      * **Git errors (authentication failed, repository not found, etc.):**
          * Verify your `GITHUB_TOKEN` is correct, has `repo` scope, and hasn't expired.
          * Double-check your `--gh-user` and `--gh-repo` names.
          * Ensure the target `--gh-branch` exists or can be created. If it's a protected branch, you might not have permission to force-push.
          * Make sure Git is installed and in your system's PATH.
      * **`.git` directory conflict:** The script creates a temporary git repo. If the output directory or its parent is already a git repo, or if `_deploy_tmp` has issues, it might conflict. The script tries to manage this, but manual cleanup of `_deploy_tmp` might be needed if errors persist.

  * **Audio/Subtitle Issues**

      * **No audio/subs in output:** Verify your input video actually contains the audio/subtitle tracks you expect. Use `ffprobe <input_file>` manually to list streams.
      * **Incorrect language tags:** The script relies on metadata in the source file. If language tags are missing or wrong, the output will reflect that. Some tools can edit this metadata.

  * **Slow Performance**

      * **Cause:** Video transcoding is CPU-intensive.
      * **Solution:**
          * Use a faster FFmpeg preset (`-p fast` or `-p veryfast`), understanding this may reduce quality/compression.
          * Reduce the number of video variants generated (`-vq`).
          * Ensure your computer is not thermal throttling (overheating).
          * Close other CPU-heavy applications.

-----

## 📜 Script Internals: A Glimpse for Developers

For those interested in the Python script (`main.py`) itself:

  * **Modularity:** The script is organized into functions for specific tasks: configuration loading, command execution, metadata probing, video/audio/subtitle rendition generation, master playlist creation, thumbnailing, and deployment.
  * **`argparse`:** Used for parsing command-line arguments.
  * **`subprocess`:** Used to run external commands like `ffmpeg`, `ffprobe`, and `git`. The `run_command` helper function is a central wrapper for this.
  * **`pathlib`:** Used for modern, object-oriented path manipulation, making file system operations cleaner.
  * **`json`:** For loading and parsing `config.json` and `ffprobe` output.
  * **`logging`:** Provides informative output during execution.
  * **Error Handling:** `try-except` blocks are used to catch common errors, especially around subprocess execution and file operations.
  * **Key functions to look at if you're exploring the code:**
      * `create_hls_package()`: The main orchestrating function.
      * `generate_video_renditions()`, `generate_audio_renditions()`, `generate_subtitle_renditions()`: Core transcoding logic.
      * `generate_master_playlist()`: Assembles the final HLS structure.
      * `run_command()`: How external tools are invoked.
      * `load_config()`: Configuration management.

-----

## 🤝 Contributing to V2HLS

Contributions, bug reports, and feature requests are welcome\! Please feel free to:

  * **Open an Issue:** If you find a bug or have a suggestion, please check if an issue already exists. If not, create a new one on the GitHub Issues page. Provide as much detail as possible.
  * **Fork the Repository:** If you'd like to contribute code.
  * **Create a New Branch:** For your feature or bugfix (e.g., `git checkout -b feature/new-cool-thing` or `bugfix/fix-that-error`).
  * **Make Your Changes:** Write clean, well-commented code.
  * **Test Thoroughly:** Ensure your changes work as expected and don't break existing functionality.
  * **Commit Your Changes:** Follow conventional commit message styles if possible.
  * **Push to Your Branch:** `git push origin feature/new-cool-thing`.
  * **Open a Pull Request (PR):** Against the `main` branch of the `ToonTamilIndia/Video-to-HLS` repository. Clearly describe your changes in the PR.

-----

## ⚖️ License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/ToonTamilIndia/Video-to-HLS/blob/main/LICENSE) file in the repository for the full license text.

-----

## 🙏 Acknowledgements

  * The incredible FFmpeg team and community for providing the powerful multimedia toolkit that V2HLS relies on.
  * The Python Software Foundation and the Python community for the versatile and developer-friendly programming language.
  * All contributors and users.
