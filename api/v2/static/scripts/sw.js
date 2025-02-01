self.addEventListener("push", event => {
  if (!event.data) {
    console.warn("Push event received with no data.");
    return;
  }

  const data = event.data.json(); // Get the message from the server
  console.log("Push Notification Received!", data);

  const options = {
    body: data.message,
    icon: "/static/img/text-message-icon.png",
    data: { url: data.url } // Allow clicking to open a chat
  };

  event.waitUntil(
    self.registration.showNotification(data.title, options)
  );
});

self.addEventListener("notificationclick", event => {
  event.notification.close(); // Close the notification
  const url = event.notification.data.url;

  event.waitUntil(
    clients.matchAll({ type: "window", includeUncontrolled: true })
      .then(clientList => {
        for (const client of clientList) {
          if (client.url === url && "focus" in client) {
            return client.focus();
          }
        }
        if (clients.openWindow) {
          return clients.openWindow(url);
        }
      })
  );
});

self.addEventListener('install', event => {
  console.log('Service Worker installing...');
  self.skipWaiting(); // Ensures immediate activation
});

self.addEventListener('activate', event => {
  console.log('Service Worker activated');
  event.waitUntil(clients.claim());
});
