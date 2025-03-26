// Global variable to store last visited page URL
let lastVisitedPage = null;

self.addEventListener("install", (event) => {
  console.log("Service Worker Installed");
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  console.log("Service Worker Activated");
  event.waitUntil(clients.claim());
});

console.log("Service worker loaded");

self.addEventListener("push", (event) => {
  console.log("[Service Worker] Push Received:", event);

  let data = {};
  if (event.data) {
    try {
      data = event.data.json();
      console.log("[Service Worker] Push data:", data);
    } catch (error) {
      console.error("[Service Worker] Error parsing push data:", error);
    }
  } else {
    data = { title: "Order Update", body: "Your order is ready!" };
    console.log("[Service Worker] No data payload, using default:", data);
  }

  const title = data.title || "Order Update";
  const options = {
    body: data.body || "Your order is ready!",
    icon: "https://feline-clever-mutually.ngrok-free.app/static/orders/images/logo.png",
    data: data, // Full payload attached (if needed for future use)
  };

  event.waitUntil(
    self.registration.showNotification(title, options)
      .then(() => {
        console.log("[Service Worker] Notification displayed.");
        return clients.matchAll({ includeUncontrolled: true, type: "window" });
      })
      .then((clients) => {
        console.log("[Service Worker] Found", clients.length, "client(s).");
        clients.forEach((client) => {
          client.postMessage({
            type: "PUSH_STATUS_UPDATE",
            payload: data,
          });
        });
      })
      .catch((err) => {
        console.error("[Service Worker] Error displaying notification:", err);
      })
  );
});

self.addEventListener("message", (event) => {
  if (event.data && event.data.type === "UPDATE_LAST_PAGE") {
    lastVisitedPage = event.data.url;
    console.log("[Service Worker] Last visited page updated:", lastVisitedPage);
  }
});

self.addEventListener("notificationclick", (event) => {
  event.notification.close();

  event.waitUntil(
    (async () => {
      // Check if any client (window/tab) is open
      const clientList = await clients.matchAll({ type: "window", includeUncontrolled: true });
      
      if (clientList.length > 0) {
        // If one or more clients are open, focus the first one
        const client = clientList[0];
        client.focus();

        // Optionally, send a message to the client to display the chat view
        client.postMessage({
          type: "OPEN_CHAT",
          // You can include additional data if needed, e.g., token_no or chat parameters
          payload: event.notification.data || {}
        });
      } else {
        // If no client is open, open a new window/tab to your main URL
        await clients.openWindow("https://feline-clever-mutually.ngrok-free.app");
      }
    })()
  );
});
