/**
 * Cloudflare Workers script untuk YouTube Downloader API
 * Deploy ini ke Cloudflare Workers untuk routing dan caching
 */

addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
  const url = new URL(request.url)
  
  // Your backend server URL (ganti dengan URL server Anda)
  const BACKEND_URL = 'https://your-server.com'
  
  // Add CORS headers
  const corsHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    'Access-Control-Max-Age': '86400',
  }
  
  // Handle preflight requests
  if (request.method === 'OPTIONS') {
    return new Response(null, {
      headers: corsHeaders,
    })
  }
  
  try {
    // Forward request to backend
    const backendUrl = `${BACKEND_URL}${url.pathname}${url.search}`
    
    const modifiedRequest = new Request(backendUrl, {
      method: request.method,
      headers: request.headers,
      body: request.body,
    })
    
    const response = await fetch(modifiedRequest)
    
    // Add CORS headers to response
    const modifiedResponse = new Response(response.body, {
      status: response.status,
      statusText: response.statusText,
      headers: {
        ...response.headers,
        ...corsHeaders,
      },
    })
    
    return modifiedResponse
    
  } catch (error) {
    return new Response(JSON.stringify({
      error: 'Backend service unavailable',
      details: error.message
    }), {
      status: 503,
      headers: {
        'Content-Type': 'application/json',
        ...corsHeaders,
      },
    })
  }
}

// Optional: Add caching for video info requests
async function handleCachedRequest(request) {
  const cache = caches.default
  const cacheKey = new Request(request.url, request)
  
  // Check cache first
  let response = await cache.match(cacheKey)
  
  if (!response) {
    // Not in cache, fetch from backend
    response = await handleRequest(request)
    
    // Cache video info requests for 1 hour
    if (request.url.includes('/info')) {
      const cacheResponse = response.clone()
      cacheResponse.headers.set('Cache-Control', 'max-age=3600')
      await cache.put(cacheKey, cacheResponse)
    }
  }
  
  return response
}
