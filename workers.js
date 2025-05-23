export default {
  async fetch(request, env, ctx) {
    const { searchParams } = new URL(request.url);
    const targetUrl = searchParams.get('url');

    if (!targetUrl) {
      return new Response('Missing `url` query parameter.', { status: 400 });
    }

    try {
      const response = await fetch(targetUrl, {
        headers: {
          // Forward original headers if needed
        }
      });

      const contentType = response.headers.get('content-type') || '';
      const fileExt = targetUrl.split('.').pop().toLowerCase();

      // Define types you want to serve
      const supportedTypes = ['m3u8', 'ts', 'mp4', 'mp3'];

      // Create a new response with CORS headers
      const modifiedResponse = new Response(response.body, {
        status: response.status,
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET,HEAD,OPTIONS',
          'Access-Control-Allow-Headers': '*',
          'Content-Type': contentType,
        },
      });

      // If it's one of the supported extensions, just return it
      if (supportedTypes.includes(fileExt)) {
        return modifiedResponse;
      }

      // Optionally block other content types
      return new Response('Unsupported file type.', { status: 403 });

    } catch (error) {
      return new Response('Error fetching URL: ' + error.toString(), { status: 500 });
    }
  }
}
