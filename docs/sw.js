const CACHE_NAME = 'bonodori-cache-v31';
const urlsToCache = [
  './',
  './index.html',
  './robots.txt',
  './sitemap.xml',
  './manifest.json',
  './events.json',
  './submission-config.js',
  './icon-192.png',
  './icon-512.png'
];

self.addEventListener('install', event => {
  event.waitUntil(
    Promise.all(
      urlsToCache.map(url =>
        fetch(url, { cache: 'reload' })
          .then(response => {
            if (!response.ok) {
              throw new Error(`Failed to cache ${url}: ${response.status}`);
            }
            return caches.open(CACHE_NAME).then(cache => cache.put(url, response));
          })
      )
    )
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', event => {
  const requestUrl = new URL(event.request.url);
  const dynamicPaths = [
    '/submission-config.js',
    '/index.html',
    '/events.json',
    '/sitemap.xml'
  ];
  const isDynamic = dynamicPaths.some(p => requestUrl.pathname.endsWith(p));

  if (isDynamic) {
    event.respondWith(
      fetch(event.request, { cache: 'no-store' })
        .then(response => {
          const responseClone = response.clone();
          event.waitUntil(
            caches.open(CACHE_NAME).then(cache => cache.put(event.request, responseClone))
          );
          return response;
        })
        .catch(() => caches.match(event.request))
    );
    return;
  }

  event.respondWith(
    caches.match(event.request)
      .then(response => {
        return response || fetch(event.request);
      })
  );
});
