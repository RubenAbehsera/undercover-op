// Le service worker minimal d'une PWA de soirée : la coquille en cache, le
// reste au réseau. Le socket ne passe jamais par ici.
const CACHE = "undercover-op-v1";
const COQUILLE = ["/", "/manifest.webmanifest", "/icone-192.png", "/icone-512.png"];

self.addEventListener("install", (evenement) => {
  evenement.waitUntil(
    caches.open(CACHE).then((cache) => cache.addAll(COQUILLE)).then(() => self.skipWaiting()),
  );
});

self.addEventListener("activate", (evenement) => {
  evenement.waitUntil(
    caches
      .keys()
      .then((cles) => Promise.all(cles.filter((cle) => cle !== CACHE).map((cle) => caches.delete(cle))))
      .then(() => self.clients.claim()),
  );
});

self.addEventListener("fetch", (evenement) => {
  const requete = evenement.request;
  if (requete.method !== "GET" || new URL(requete.url).pathname.startsWith("/socket.io")) {
    return;
  }
  evenement.respondWith(
    fetch(requete)
      .then((reponse) => {
        // Seules les réponses complètes du serveur méritent le cache : une
        // erreur mise de côté serait resservie hors ligne.
        if (reponse.ok && reponse.type === "basic") {
          const copie = reponse.clone();
          caches.open(CACHE).then((cache) => cache.put(requete, copie)).catch(() => {});
        }
        return reponse;
      })
      .catch(() => caches.match(requete).then((cache) => cache || caches.match("/"))),
  );
});
