// bypass CORS
addEventListener("fetch", event => {
  event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
  try {
    const url = new URL(request.url)
    const uid = url.searchParams.get("uid")
    const index = url.searchParams.get("index") || 1
    const size = url.searchParams.get("size") || 9999
    const server = url.searchParams.get("server") || "en_US"
    const SERVER_MAP = {
      'en_US': 'https://account.yo-star.com',
      'ja_JP': 'https://account.yostar.co.jp',
      'ko_KR': 'https://account.yostar.kr',
    }
    if (!uid) {
      return new Response(JSON.stringify({ error: "Missing uid parameter" }), {
        status: 400,
        headers: { "Content-Type": "application/json" },
      })
    }
    const server_base = SERVER_MAP[server] || SERVER_MAP['en_US']
    const targetUrl = `${server_base}/api/game/gachas?key=ark&index=${index}&size=${size}&uid=${uid}`

    const response = await fetch(targetUrl)
    const data = await response.json()

    return new Response(JSON.stringify(data), {
      status: response.status,
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET",
      },
    })
  } catch (err) {
    return new Response(JSON.stringify({ error: err.message }), {
      status: 500,
      headers: { "Content-Type": "application/json" },
    })
  }
}
