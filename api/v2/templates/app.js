async function subscribeUserToPush() {
  const registration = await navigator.serviceWorker.ready;
  const subscription = await registration.pushManager.subscribe({
    userVisibleOnly: true,
    applicationServerKey: "YOUR_PUBLIC_VAPID_KEY"
  });

  //console.log("Push Subscription:", subscription);

  // Send this subscription to your backend (so the server can send push messages)
  fetch("/subscribe", {
    method: "POST",
    body: JSON.stringify(subscription),
    headers: { "Content-Type": "application/json" }
  });
}

if (Notification.permission === "granted") {
  subscribeUserToPush();
} else {
  Notification.requestPermission().then(permission => {
    if (permission === "granted") {
      subscribeUserToPush();
    }
  });
}
