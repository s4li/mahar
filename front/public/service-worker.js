self.__precacheManifest = [].concat(self.__precacheManifest || []);
workbox.precaching.suppressWarnings();
workbox.precaching.precacheAndRoute(self.__precacheManifest, {});

workbox.routing.registerNavigationRoute('/index.html');

// install new service worker when ok, then reload page.
self.addEventListener("message", msg => {
    if (msg.data.action == 'skipWaiting') {
        self.skipWaiting()
    }
})


//importScripts('https://storage.googleapis.com/workbox-cdn/releases/5.1.2/workbox-sw.js');

//if (workbox) {
//  console.log(`Yay! Workbox is loaded 🎉`);
//} else {
//  console.log(`Boo! Workbox didn't load 😬`);
//}
//workbox.core.setCacheNameDetails({ prefix: 'offlinMode' })
//self.__precacheManifest = [].concat(self.__precacheManifest || []);
//workbox.precaching.suppressWarnings();
//workbox.precaching.precacheAndRoute(self.__precacheManifest, {});
//
//// install new service worker when ok, then reload page.
//self.addEventListener("message", msg=>{
//    if (msg.data.action=='skipWaiting'){
//        self.skipWaiting()
//    }
//})

//workbox.routing.registerRoute('https://jsonplaceholder.typicode.com/todos/1', workbox.strategies.cacheFirst({
//    cacheName: 'placeholder-cache',
//}));



//workbox.setConfig({
//  debug: false,
//});
//workbox.routing.registerNavigationRoute('/index.html');
//workbox.skipWaiting()
//workbox.clientsClaim()
//const staticAssets = [
//  '../src/assets/fonts/IRANSansWeb_100.woff',
//  '../src/assets/fonts/IRANSansWeb_200.woff',
//  '../src/assets/fonts/IRANSansWeb_400.woff',
//  '../src/assets/fonts/IRANSansWeb_600.woff',
//  '../src/assets/fonts/IRANSansWeb_800.woff',
//  '../src/assets/fonts/fa-duotone-900.woff',
//  '../src/assets/fonts/fa-brands-400.woff',
//  '../src/assets/fonts/fa-light-300.woff',
//  '../src/assets/fonts/fa-regular-400.woff',
//  '../src/assets/image/guidImage/1.png',
//  '../src/assets/image/guidImage/2.jpg',
//  '../src/assets/image/guidImage/3.jpg',
//  '../src/assets/image/guidImage/4.jpg',
//  '../src/assets/image/guidImage/5.jpg',
//  '../src/assets/image/guidImage/6.jpg',
//  '../src/assets/image/guidImage/7.jpg',
//  '../public/manifest.json',
//];
//const cacheName = 'first';
//
//self.addEventListener('install', async () => {
//  const cache = await caches.open(cacheName);
//  await cache.addAll(staticAssets);
//  return self.skipWaiting();
//});
//
//
//////Change this value every time before you build
//const LATEST_VERSION = 'v1.2'
//self.addEventListener('activate', () => {
//console.log(`%c ${LATEST_VERSION} `, 'background: #ddd; color: #0000ff')
//if (caches) {
//  caches.keys().then((arr) => {
//    arr.forEach((key) => {
//      if (key.indexOf('d4-precache') < -1) {
//        caches.delete(key).then(() => console.log(`%c Cleared ${key}`, 'background: #333; color: #ff0000'))
//      } else {
//        caches.open(key).then((cache) => {
//          cache.match('version').then((res) => {
//            if (!res) {
//              cache.put('version', new Response(LATEST_VERSION, { status: 200, statusText: LATEST_VERSION }))
//            } else if (res.statusText !== LATEST_VERSION) {
//              caches.delete(key).then(() => console.log(`%c Cleared Cache ${LATEST_VERSION}`, 'background: #333; color: #ff0000'))
//            } else console.log(`%c Great you have the latest version ${LATEST_VERSION}`, 'background: #333; color: #00ff00')
//          })
//        })
//      }
//    })
//  })
//}
////self.clients.claim();
//})
//
//self.addEventListener('fetch', async e => {
//  const req = e.request;
//  const url = new URL(req.url);
//  if (url.origin === location.origin) {
//    e.respondWith(cacheFirst(req));
//  } else {
//    e.respondWith(networkAndCache(req));
//  }
//});
//
//async function cacheFirst(req) {
//  const cache = await caches.open(cacheName);
//  const cached = await cache.match(req);
//  return cached || fetch(req);
//}
//
//async function networkAndCache(req) {
//  const cache = await caches.open(cacheName);
//  try {
//    const fresh = await fetch(req);
//    await cache.put(req, fresh.clone());
//    return fresh;
//  } catch (e) {
//    const cached = await cache.match(req);
//    return cached;
//  }
//}