// static/sw.js

self.addEventListener('install', (e) => {
    console.log('[Service Worker] Installed');
});

self.addEventListener('fetch', (e) => {
    // PWA ko pass karne ke liye bas ye function hona zaroori hai
});