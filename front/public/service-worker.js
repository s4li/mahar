const staticAssets = [
  '../src/assets/fonts/IRANSansWeb_100.woff',
  '../src/assets/fonts/IRANSansWeb_200.woff',
  '../src/assets/fonts/IRANSansWeb_400.woff',
  '../src/assets/fonts/IRANSansWeb_600.woff',
  '../src/assets/fonts/IRANSansWeb_800.woff',
  '../src/assets/fonts/fa-duotone-900.woff',
  '../src/assets/fonts/fa-brands-400.woff',
  '../src/assets/fonts/fa-light-300.woff',
  '../src/assets/fonts/fa-regular-400.woff',
];

const cacheName = 'first';

self.addEventListener('install', async e => {
  const cache = await caches.open(cacheName);
  await cache.addAll(staticAssets);
  return self.skipWaiting();
});

self.addEventListener('activate', e => {
  self.clients.claim();
});

self.addEventListener('fetch', async e => {
  const req = e.request;
  const url = new URL(req.url);
  if (url.origin === location.origin) {
    e.respondWith(cacheFirst(req));
  } else {
    e.respondWith(networkAndCache(req));
  }
});

async function cacheFirst(req) {
  const cache = await caches.open(cacheName);
  const cached = await cache.match(req);
  return cached || fetch(req);
}

async function networkAndCache(req) {
  const cache = await caches.open(cacheName);
  try {
    const fresh = await fetch(req);
    await cache.put(req, fresh.clone());
    return fresh;
  } catch (e) {
    const cached = await cache.match(req);
    return cached;
  }
}