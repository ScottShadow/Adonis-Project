
// Utility function to convert the Base64 VAPID key to a UInt8Array
function urlBase64ToUint8Array(base64String) {
  const padding = "=".repeat((4 - base64String.length % 4) % 4);
  const base64 = (base64String + padding)
    .replace(/-/g, "+")
    .replace(/_/g, "/");
  const rawData = window.atob(base64);
  const outputArray = new Uint8Array(rawData.length);
  for (let i = 0; i < rawData.length; ++i) {
    outputArray[i] = rawData.charCodeAt(i);
  }
  return outputArray;
}

// Your VAPID application server key (public key)
const VAPID_PUBLIC_KEY = "{{ VAPID_PUBLIC_KEY }}";
const MY_WEBSITE_URL = "{{ MY_WEBSITE_URL }}";
const applicationServerKey = urlBase64ToUint8Array(VAPID_PUBLIC_KEY);

// Subscribe the user to push notifications
async function subscribeUserToPush(registration) {
  try {
    console.log("[Push Notifications] Attempting to subscribe user to push notifications...");
    const subscription = await registration.pushManager.subscribe({
      userVisibleOnly: true,
      applicationServerKey: applicationServerKey
    });
    console.log("[Push Notifications] New push subscription obtained:", subscription);

    console.log("[Push Notifications] Sending subscription to backend...");
    const response = await fetch("/api/v2/subscribe", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify(subscription)
    });

    if (!response.ok) {
      throw new Error(`Failed to send subscription to backend: ${response.statusText}`);
    }
    console.log("[Push Notifications] Subscription successfully sent to backend!");
  } catch (error) {
    console.error("[Push Notifications] Error during push subscription:", error);
  }
}

// Continue with push subscription after SW is ready and in control
async function proceedWithPushSubscription(registration) {
  console.log("[Push Notifications] Checking for existing push subscription...");
  try {
    const existingSubscription = await registration.pushManager.getSubscription();
    if (existingSubscription) {
      console.log("[Push Notifications] Existing subscription found:", existingSubscription);
    } else {
      console.log("[Push Notifications] No existing subscription found. Subscribing user...");
      await subscribeUserToPush(registration);
    }
  } catch (error) {
    console.error("[Push Notifications] Error checking subscription:", error);
  }
}

// Initialize push notifications: check permissions and register the SW
async function initializePushNotifications() {
  console.log("[Push Notifications] Starting initialization...");

  // Check notification permission first
  if (Notification.permission !== "granted") {
    console.log("[Push Notifications] Permission not granted. Requesting permission...");
    try {
      const permission = await Notification.requestPermission();
      console.log("[Push Notifications] Permission result:", permission);
      if (permission !== "granted") {
        console.warn("[Push Notifications] User denied notification permission.");
        return;
      }
    } catch (error) {
      console.error("[Push Notifications] Error requesting notification permission:", error);
      return;
    }
  } else {
    console.log("[Push Notifications] Notification permission already granted.");
  }

  // Register the service worker
  if ("serviceWorker" in navigator) {
    try {
      console.log("[Push Notifications] Registering service worker...");
      const registration = await navigator.serviceWorker.register("/sw.js", { scope: "/" });
      console.log("[Push Notifications] Service Worker registered:", registration);
      console.log("[Push Notifications] Waiting for service worker to be ready...");

      // Check if the SW is already controlling the page
      if (navigator.serviceWorker.controller) {
        console.log("[Push Notifications] Active Service Worker detected:", navigator.serviceWorker.controller);
        const serviceWorkerRegistration = await navigator.serviceWorker.ready;
        console.log("[Push Notifications] Service Worker is ready:", serviceWorkerRegistration);
        await proceedWithPushSubscription(serviceWorkerRegistration);
      } else {
        console.warn("[Push Notifications] No active Service Worker controlling the page yet.");
        // Listen for controllerchange and proceed once the new SW takes control
        navigator.serviceWorker.addEventListener("controllerchange", async () => {
          console.log("[Push Notifications] New service worker is now controlling this page.");
          const serviceWorkerRegistration = await navigator.serviceWorker.ready;
          console.log("[Push Notifications] Service Worker is ready after controllerchange:", serviceWorkerRegistration);
          await proceedWithPushSubscription(serviceWorkerRegistration);
        });
      }
    } catch (error) {
      console.error("[Push Notifications] Error during service worker registration or push subscription:", error);
    }
  } else {
    console.error("[Push Notifications] Service Workers are not supported in this browser.");
  }
}

// Display a notification on the client
function showNotification() {
  if (Notification.permission === "granted") {
    // Initialize push notifications (which includes SW registration and subscription)
    initializePushNotifications();
    /* new Notification(`New message from ${data.from}`, {
        body: data.message,
        icon: "/static/img/favicon.jpg",
    }); */
  } else {
    Notification.requestPermission().then(permission => {
      if (permission === "granted") {
        initializePushNotifications();
      }
    });
  }
}

// Optionally, call initializePushNotifications() on load or when needed
// initializePushNotifications();
showNotification();
