addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

// Get or refresh the access token from Baidu API
async function getAccessToken(kv, forceUpdate = false) {
  let accessToken = await kv.get('access_token');
  let expiresAt = parseInt(await kv.get('expires_in'), 10);
  let now = Math.floor(Date.now() / 1000);

  if (!forceUpdate && accessToken && now < expiresAt) {
    return {"token":accessToken,"exp":expiresAt.toString()}
  }

  const api_key = await kv.get('api_key');
  const secret_key = await kv.get('secret_key');
  const url = `https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=${api_key}&client_secret=${secret_key}`;
  
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    }
  });
  const odata = await response.json();
  accessToken = odata.access_token;
  expiresAt = now - 30 + odata.expires_in;

  await kv.put('access_token', accessToken);
  await kv.put('expires_in', expiresAt.toString());
  return {"token":accessToken,"exp":expiresAt.toString()}
}

// Process Base64-encoded image
async function processImg(kv, rbody, accessToken) {

  const response = await fetch(`https://aip.baidubce.com/file/2.0/mt/pictrans/v1?access_token=${accessToken}`, {
    method: 'POST',
    headers: {'content-type': 'multipart/form-data'},
    body: rbody
  });

  return response.json();
}

async function handleRequest(request) {
  
  const url = new URL(request.url);
  const kv = baiduAPI; // Replace MY_KV_NAMESPACE with your actual KV namespace binding
  const uuids = await kv.get('uuids');
  const uuid = url.searchParams.get('uuid');

  if (!uuids || !uuids.split(',').includes(uuid)) {
    return modifyHeaders(new Response('{"error":"provided uuid is invalid"}', {status: 401}));
  }
  
  if (request.method !== 'POST') {
    return modifyHeaders(new Response('{"error":"Bad Request"}', {status: 400}));
  }

  const accessTokens = await getAccessToken(kv);
  if (url.pathname === "/token") {
    return modifyHeaders(new Response('{"access_token":"'+accessTokens["token"]+'","expires_in":"'+accessTokens['exp']+'"}', {status: 200}));
  }
  // 以下内容暂未完成 不可用
  let requestBody = request.body;
  
  const result = await processImg(kv, requestBody, accessTokens[0]);
  return modifyHeaders(new Response(JSON.stringify(result)));
}

function modifyHeaders(originalResponse) {
  let newHeaders = new Headers(originalResponse.headers);
  newHeaders.set('Access-Control-Allow-Origin', '*');
  newHeaders.set('Access-Control-Allow-Headers', '*');
  newHeaders.set('Cache-Control', 'no-cache');
  newHeaders.set('Pragma', 'no-cache');
  newHeaders.set('Expires', '-1');
  newHeaders.set('Content-Type','application/json');
  return new Response(originalResponse.body, {
      status: originalResponse.status,
      statusText: originalResponse.statusText,
      headers: newHeaders
  });
}
