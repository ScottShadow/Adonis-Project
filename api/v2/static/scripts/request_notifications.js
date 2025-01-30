if (Notification.permission === "default") {
  Notification.requestPermission().then((permission) => {
    if (permission === "granted") {
      console.log("Notifications enabled!");
    } else {
      console.log("Notifications denied.");
    }
  });
}
