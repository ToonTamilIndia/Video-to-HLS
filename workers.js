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

      const modifiedResponse = new Response(response.body, {
        status: response.status,
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET,HEAD,OPTIONS',
          'Access-Control-Allow-Headers': '*',
          'Content-Type': contentType,
        },
      });
      
      return modifiedResponse;
      
    } catch (error) {
      return new Response('Error fetching URL: ' + error.toString(), { status: 500 });
    }
  }
}
