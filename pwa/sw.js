/* Service Worker for Super Cerebro AI */
const CACHE_VERSION = 'v1.0.0';
const STATIC_CACHE = `cerebro-static-${CACHE_VERSION}`;
const RUNTIME_CACHE = 'cerebro-runtime';
const PRECACHE_URLS = [
  './',
  './index.html',
  './styles.css',
  './app.js',
  './manifest.json',
  './icons/icon-192.png',
  './icons/icon-512.png'
];
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(STATIC_CACHE).then(cache => cache.addAll(PRECACHE_URLS)).then(() => self.skipWaiting())
  );
});
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys => Promise.all(keys.filter(k => ![STATIC_CACHE, RUNTIME_CACHE].includes(k)).map(k => caches.delete(k)))).then(() => self.clients.claim())
  );
});
self.addEventListener('fetch', event => {
  const { request } = event;
  const url = new URL(request.url);
  if (request.method !== 'GET') return;
  if (url.origin === self.location.origin) {
    // Network-first for HTML, cache-first for assets
    if (request.mode === 'navigate' || request.destination === 'document') {
      event.respondWith(networkFirst(request));
      return;
    }
    if (['style','script','image','font'].includes(request.destination)) {
      event.respondWith(cacheFirst(request));
      return;
    }
  }
  event.respondWith(networkFirst(request));
});
async function cacheFirst(request) {
  const cache = await caches.open(STATIC_CACHE);
  const cached = await cache.match(request);
  if (cached) return cached;
  const response = await fetch(request);
  if (response && response.ok) cache.put(request, response.clone());
  return response;
}
async function networkFirst(request) {
  const cache = await caches.open(RUNTIME_CACHE);
  try {
    const response = await fetch(request);
    if (response && response.ok) cache.put(request, response.clone());
    return response;
  } catch (err) {
    const cached = await cache.match(request);
    if (cached) return cached;
    if (request.mode === 'navigate') {
      const fallback = await caches.match('./index.html');
      if (fallback) return fallback;
    }
    throw err;
  }
}
self.addEventListener('push', event => {
  let data = {};
  try { data = event.data ? event.data.json() : {}; } catch (_) {}
  const title = data.title || 'Super Cerebro AI';
  const options = {
    body: data.body || 'You have a new message',
    icon: './icons/icon-192.png',
    badge: './icons/icon-192.png',
    data: data.url || './',
  };
  event.waitUntil(self.registration.showNotification(title, options));
});
self.addEventListener('notificationclick', event => {
  event.notification.close();
  const url = event.notification.data || './';
  event.waitUntil(
    clients.matchAll({ type: 'window', includeUncontrolled: true }).then(list => {
      const client = list.find(c => c.url.includes(url));
      if (client) return client.focus();
      return clients.openWindow(url);
    })
  );
});
