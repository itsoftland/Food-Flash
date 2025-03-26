document.addEventListener('DOMContentLoaded', async function() {
    const permissionModal = new bootstrap.Modal(document.getElementById('permissionModal'));
    const notificationModal = new bootstrap.Modal(document.getElementById('notificationModal'));
    const chatContainer = document.getElementById('chat-container');
    const chatInput = document.getElementById('chat-input');
    const sendButton = document.getElementById('send-button');
    const menuButton = document.getElementById('menu-button');

    let notificationsEnabled = true;
    const isAndroid = /Android/i.test(navigator.userAgent);
    console.log("Android device detected:", isAndroid);
    if (isAndroid) {
        // Add a bit of extra bottom padding to .branding or .container-wrapper
        document.querySelector('.container-wrapper')
                .style.paddingBottom = '8px';
    }

    // Adjust viewport for mobile devices
    function setVh() {
        // 1% of the window's *innerHeight*
        let vh = window.innerHeight * 0.01;
        // Set the value in a CSS variable
        document.documentElement.style.setProperty('--vh', `${vh}px`);
      }
      
    // Call the function once to set the initial value
    setVh();
    
    // Recompute on resize/orientation changes
    window.addEventListener('resize', setVh);
    window.addEventListener('orientationchange', setVh);
      
    // 1) Try the official Brave check
    let braveDetected = false;
    if (navigator.brave && typeof navigator.brave.isBrave === 'function') {
        braveDetected = await navigator.brave.isBrave();
    }

    // 2) If that fails, try user agent or UA-CH fallback
    if (!braveDetected) {
        if (navigator.userAgent.includes("Brave")) {
        braveDetected = true;
        } else if (navigator.userAgentData && navigator.userAgentData.getHighEntropyValues) {
        const data = await navigator.userAgentData.getHighEntropyValues(["brands"]);
        if (data.brands.some(b => b.brand.includes("Brave"))) {
            braveDetected = true;
        }
        }
    }

    // 3) If Brave is detected, show instructions
    if (braveDetected) {
        alert("It looks like you’re using Brave. Please ensure:\n\n1. Brave Settings > Privacy and Security > Site and Shields Settings > Notifications > 'Sites can ask to send notifications' is ON.\n2. Enable 'Use Google Services for Push Messaging' if shown.\n\nOtherwise, push notifications may fail.");
    }
    
    // Show permission modal
    permissionModal.show();

    // Grant permission button
    document.getElementById('grant-permission').addEventListener('click', ()=> {
        permissionModal.hide();
        requestPermissions();
        playWelcomeMessage();
    });

    // Deny permission button
    document.getElementById('deny-permission').addEventListener('click', function() {
        permissionModal.hide();
        alert('Permissions denied. Service may not function properly.');
    });

    // Additional function to request other permissions or do setup
    function requestPermissions() {
        Notification.requestPermission().then(permission => {
            console.log("permission:",permission);
            if (permission === "granted") {
                console.log("Notifications allowed!");
            } else {
                console.log("Notifications denied!");
            }
        });
    }

    // Welcome message
    function playWelcomeMessage() {
        const welcomeMessage = new SpeechSynthesisUtterance('Hi, Welcome, Good Day. Please enter the Bill Number and send to track your order.');
        speechSynthesis.speak(welcomeMessage);
    }

    // Buttons for notification modal
    document.getElementById('ok-notification').addEventListener('click', function() {
        notificationModal.hide();
    });
    document.getElementById('disable-notifications').addEventListener('click', function() {
        notificationModal.hide();
        notificationsEnabled = false;
    });
    // 1. Register the Service Worker at the root scope
    if ("serviceWorker" in navigator) {
        navigator.serviceWorker.register("/service-worker.js", { scope: '/' })
        .then((registration) => {
            console.log("Service Worker Registered:", registration);
        })
        .catch((error) => {
            console.error("Service Worker Registration Failed:", error);
        });
    }

    // 2. If there's no controller, optionally reload once to let the SW take control
    if (!navigator.serviceWorker.controller) {
        console.log("No active service worker controller. Reloading...");
        // You can uncomment this if you want an automatic reload:
        // window.location.reload();
    }



    // Helper to convert your public key
    function urlBase64ToUint8Array(base64String) {
        const padding = '='.repeat((4 - (base64String.length % 4)) % 4);
        const base64 = (base64String + padding)
            .replace(/\-/g, '+')
            .replace(/_/g, '/');
        const rawData = window.atob(base64);
        const outputArray = new Uint8Array(rawData.length);
        
        for (let i = 0; i < rawData.length; ++i) {
            outputArray[i] = rawData.charCodeAt(i);
        }
        return outputArray;
    }

    // Function to get or generate a unique browser ID stored in localStorage
    function getBrowserId() {
        let browserId = localStorage.getItem('browser_id');
        if (!browserId) {
            browserId = crypto.randomUUID();
            localStorage.setItem('browser_id', browserId);
        }
        return browserId;
    }

    // Subscribe to push notifications (called after user enters a token)
    async function subscribeToPushNotifications(token) {
        try {
            if (!token) {
                console.error("Token not provided. Cannot subscribe.");
                return;
            }
            
            if (Notification.permission !== "granted") {
                console.error("Notification permission is not granted.");
                return;
            }
            
            // Wait for the service worker registration.
            let registration = await navigator.serviceWorker.getRegistration();
            if (!registration) {
                console.error("No service worker found. Registering...");
                registration = await navigator.serviceWorker.register('/service-worker.js', { scope: '/' });
            }
            console.log(navigator.serviceWorker.ready)

            // Check if the page is controlled by the service worker.
            if (!navigator.serviceWorker.controller) {
                console.warn("No active service worker controller. The page may need a reload.");
                // Optionally reload to let SW take control:
                window.location.reload();
            }

            // Try to retrieve an existing push subscription.
            let subscription = await registration.pushManager.getSubscription();
            if (subscription) {
                console.log("Existing subscription found:", subscription);
                // Unsubscribe the existing subscription if you suspect corruption
                try {
                    await subscription.unsubscribe();
                    console.log("Unsubscribed from existing subscription.");
                    subscription = null;
                } catch (unsubError) {
                    console.error("Error unsubscribing:", unsubError);
                }
            }

            // Create a new push subscription
            if (!subscription) {
                const vapidKey = "BAv_HFvgMBKxx3Jnse3fLMjzUEn3n3zS76GwEGQ_oOPR_40U1e7O4AiezuOReRTK4ULx2EaGC9kGAz-lzV791Tw".trim();
                subscription = await registration.pushManager.subscribe({
                    userVisibleOnly: true,
                    applicationServerKey: urlBase64ToUint8Array(vapidKey)
                });
                console.log("New subscription created:", subscription);
                console.log("Subscription JSON string:", JSON.stringify(subscription));

            }
            
            // Save subscription to server if changed.
            const newSubscriptionJSON = JSON.stringify(subscription);
            const storedSubscription = localStorage.getItem("pushSubscription");
            if (storedSubscription !== newSubscriptionJSON) {
                // Convert the subscription to JSON to ensure we have plain objects.
                const sub = subscription.toJSON();

                const payload = {
                    endpoint: sub.endpoint,       // e.g., "https://fcm.googleapis.com/fcm/send/..."
                    keys: sub.keys,               // Contains "p256dh" and "auth"
                    browser_id: getBrowserId(),   // Your generated browser ID
                    token_number: token           // The token provided by the user
                };
                                
                const response = await fetch('/vendors/api/save-subscription/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                
                if (response.ok) {
                    localStorage.setItem("pushSubscription", newSubscriptionJSON);
                    console.log("Push subscription updated successfully.");
                } else {
                    console.error("Failed to update push subscription on the server.");
                }
            } else {
                console.log("Subscription unchanged. No need to update.");
            }
        } catch (error) {
            console.error("Error in subscribeToPushNotifications:", error);
        }
    }

    console.log("Notification API supported:", "Notification" in window);

    if (navigator.serviceWorker) {
        // Update the service worker with the current page URL on load.
        // Listen for messages from the service worker
        navigator.serviceWorker.addEventListener("message", (event) => {
            if (event.data && event.data.type === "OPEN_CHAT") {
            console.log("Received OPEN_CHAT message:", event.data.payload);
            // Call a function to display or refresh the chat view
            showChatWindow(event.data.payload);   
            }
        });
        
        // Optionally, update the service worker with the current page URL if needed
        navigator.serviceWorker.ready.then((registration) => {
            if (registration.active) {
            registration.active.postMessage({
                type: "UPDATE_LAST_PAGE",
                url: window.location.href,
            });
            }
        });

        // Optionally, you can listen for navigation events (if using a SPA or similar)
        window.addEventListener("popstate", () => {
            navigator.serviceWorker.ready.then((registration) => {
            if (registration.active) {
                registration.active.postMessage({
                type: "UPDATE_LAST_PAGE",
                url: window.location.href,
                });
            }
            });
        });
        navigator.serviceWorker.addEventListener('message', (event) => {
            if (event.data && event.data.type === 'PUSH_STATUS_UPDATE') {
                const pushData = event.data.payload;
                console.log('Received push update via postMessage:', pushData);
                
                // Customize the chat message as needed. Here we assume pushData contains token_number and status.
                const messageHTML = `
                    <strong>Order Status:</strong> ${pushData.status || "Unknown"}<br>
                    <strong>Counter No:</strong> ${pushData.counter_no || ""}<br>
                    <strong>Token No:</strong> ${pushData.token_no || ""}
                    
                `;
                appendMessage(messageHTML, 'server');
                if (pushData.status === "ready") {
                    playNotificationSound();
                    const orderReadyMessage = new SpeechSynthesisUtterance(`Your Order ${pushData.token_no} is Ready at Counter ${pushData.counter_no}`);
                    speechSynthesis.speak(orderReadyMessage);
                    notificationModal.show();
                    if (navigator.vibrate) {
                        navigator.vibrate([500, 200, 500, 200, 500, 200, 500]);
                    }
                }
                const modalHeader = document.querySelector('#notificationModal .modal-body h5');
                modalHeader.innerHTML = `Order <strong>${pushData.token_no}</strong> is <strong>${pushData.status}</strong> at Counter <strong>${pushData.counter_no}</strong>!`;
                
            }
        });
    }
    // Menu button logic
    if (menuButton) {
        menuButton.addEventListener('click', function() {
            let menuImageModal = new bootstrap.Modal(document.getElementById('menuImageModal'));
            menuImageModal.show();
        });
    }
    
    function playNotificationSound() {
        if (notificationsEnabled) {
            const notificationAudio = new Audio('/static/orders/audio/0112.mp3');
            notificationAudio.play().catch(err => console.error('Error playing notification sound:', err));
            } else {
                console.log('Audio not unlocked. Please tap anywhere to enable audio.');
            }
    }

    // Chat messaging
    function appendMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message-bubble', sender);
    
        // Get current time in HH:MM AM/PM format
        const now = new Date();
        const timeStamp = now.toLocaleTimeString([], { 
          hour: '2-digit', 
          minute: '2-digit', 
          hour12: true 
        });
    
        // Create message content with flex layout
        messageDiv.innerHTML = `
          <div class="message-row">
            <div class="message-content">${text}</div>
            <div class="message-timestamp">
              ${timeStamp}
              <span class="message-check">&#10003;</span>
            </div>
          </div>
        `;
    
        chatContainer.appendChild(messageDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight; // Auto-scroll to bottom
    }
    

    // Send button logic
    sendButton.addEventListener('click', function () {
        const message = chatInput.value.trim();
        if (message !== '') {
            appendMessage(message, 'user');
            chatInput.value = '';
            fetchOrderStatusOnce(message);
        }
    });

    // Single check to confirm the order status
    function fetchOrderStatusOnce(token) {
        fetch(`/check-status/?token_no=${token}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                const messageHTML = `
                    <strong>Order Status:</strong> ${data.status || "Unknown"}<br>
                    <strong>Counter No:</strong> ${data.counter_no || "N/A"}<br>
                    <strong>Token No:</strong> ${token}
                `;
                appendMessage(messageHTML, 'server');

                // If status is ready, notify user
                if (data.status === "ready") {
                    playNotificationSound();
                    const orderReadyMessage = new SpeechSynthesisUtterance(`Your Order ${token} is ${data.status} at the counter ${data.counter_no}.`);
                    speechSynthesis.speak(orderReadyMessage);
                    notificationModal.show();
                    const modalHeader = document.querySelector('#notificationModal .modal-body h5');
                    modalHeader.innerHTML = `Order <strong>${data.token_no}</strong> is <strong>${data.status}</strong> at Counter <strong>${data.counter_no}</strong>!`;
                    
                    if (navigator.vibrate) {
                        navigator.vibrate([500, 200, 500, 200, 500, 200, 500]);
                    }
                }

                // Finally, subscribe for push notifications with the token
                subscribeToPushNotifications(token);
            })
            .catch(error => {
                console.error("Error fetching order status:", error);
                appendMessage("Error fetching order status. Please try again.", 'server');
            });
    }

    function showChatWindow(data) {
        // Make sure the chat container is visible.
        // (If you’re hiding it by default using CSS, e.g., display: none,
        //  then set it to block or flex as required.)
        window.onload = function () {
            document.querySelector('.chat-container').style.display = "none";
            setTimeout(() => {
                document.querySelector('.chat-container').style.display = "block";
            }, 100);
        };
        setTimeout(() => {
            chatContainer.scrollTop = chatContainer.scrollHeight;
          }, 50);
        // Optionally, if the payload contains a token number,
        // pre-populate the chat input or perform any additional logic.
        if (data && data.token_no) {

            chatInput.value = data.token_no;
            chatInput.value = '';
            // If you want to refresh the chat messages based on token,
            // you could call your fetch function here, e.g.:
            // fetchOrderStatusOnce(data.token_no);
        }
        
        // Optionally, you could scroll to the chat container if needed.
        chatContainer.scrollIntoView({ behavior: "smooth" });
    
        console.log("Chat window is now open or refreshed.", data);
    }
    
});
