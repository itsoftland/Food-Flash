import { AdSliderService } from './services/adSliderService.js';
import { AddOutletService } from "./services/addOutletService.js"; // adjust the path if needed
import { MenuModalService } from './services/menuModalService.js';
import { FeedbackService } from "./services/feedBackService.js";
import { IosPwaInstallService } from './services/iosPwaInstallService.js';
import { PermissionService } from "./services/permissionService.js";
import { initNotificationModal, showNotificationModal } from './services/notificationService.js';

document.addEventListener('DOMContentLoaded', async function() {
    AppUtils.setViewportHeightVar();
    const notificationModal = new bootstrap.Modal(document.getElementById('notificationModal'));
    const chatContainer = document.getElementById('chat-container');
    const chatInput = document.getElementById('chat-input');
    const sendButton = document.getElementById('send-button');
    const menuButton = document.getElementById('menu-button');
    const ratingButton = document.getElementById('rating-button');

    
    const urlParams = new URLSearchParams(window.location.search);
    let locationId = urlParams.get("location_id");

    // 1️⃣ Check URL param first
    if (locationId) {
        AppUtils.setCurrentLocation(locationId); // Store it
    } else {
        // 2️⃣ Fallback to localStorage
        locationId = AppUtils.getCurrentLocation();

        if (!locationId) {
            // 3️⃣ Ask for it / show error / redirect
            alert("No location ID found. Please select a location to proceed.");
            // Optionally redirect to a location selection page
            // window.location.href = "/select-location/";
            throw new Error("Missing location ID");
        }
    }

    const vendorFromQR = urlParams.get('vendor_id');

    if (vendorFromQR) {
        AppUtils.setCurrentVendors(vendorFromQR);

        // Optional: Clean the URL
        const newUrl = window.location.origin + window.location.pathname;
        history.replaceState(null, "", newUrl);
    }
    MenuModalService.init();
    FeedbackService.init();
    IosPwaInstallService.init();
    PermissionService.init();
    PermissionService.showModal();
    // Example usage: Get the last active vendor ID

    const vendorIdsString = localStorage.getItem("selectedVendors");
    if (vendorIdsString) {
        console.log(vendorIdsString, "vendoridsstring");
        const vendorIdsArray = JSON.parse(vendorIdsString);
    
        const vendorIds = vendorIdsArray
            .map(id => parseInt(id))
            .filter(id => Number.isInteger(id) && !isNaN(id));
    
        if (vendorIds.length > 0) {
            try {
                const adsData = await AdSliderService.fetchAds(vendorIds);
                const vendorAdsArray = adsData.map(vendor => vendor.ads);
                const interleavedAds = AdSliderService.interleaveAds(vendorAdsArray);
                AdSliderService.renderAds(interleavedAds);
                AdSliderService.init();
            } catch (err) {
                console.error("Failed to load ads:", err);
            }
    
            fetch("/api/get_vendor_logos/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": AppUtils.getCSRFToken(),
                },
                credentials: "same-origin",
                body: JSON.stringify({ vendor_ids: vendorIds }),
            })
            .then(response => response.json())
            .then(data => {
                const logoContainer = document.getElementById("vendor-logo-bar");
                const activeVendorId = AppUtils.getActiveVendor();
                if (logoContainer) {
                    logoContainer.innerHTML = "";
    
                    data.forEach(vendor => {
                        const wrapper = document.createElement("div");
                        wrapper.classList.add("vendor-logo-wrapper");
                    
                        const logo = document.createElement("img");
                        logo.src = vendor.logo_url;
                        logo.alt = vendor.name;
                        logo.classList.add("vendor-logo");
                        logo.dataset.vendorId = vendor.vendor_id;
                    
                        // Add highlight if active
                        if (vendor.vendor_id === activeVendorId) {
                            wrapper.classList.add("active");
                            localStorage.setItem("selectedOutletName", vendor.name);
                            localStorage.setItem("activeVendorLogo",vendor.logo_url);
                            const outletName = localStorage.getItem("selectedOutletName") || "our outlet";
                            showWelcomeMessage(outletName)
                            // Scroll into view after render
                            setTimeout(() => {
                                wrapper.scrollIntoView({
                                    behavior: "smooth",
                                    inline: "center",
                                    block: "nearest"
                                });
                            }, 100);
                        }
                    
                        logo.addEventListener("click", () => {
                            document.querySelectorAll('.vendor-logo-wrapper').forEach(el => el.classList.remove('active'));
                            // Add active to clicked one
                            wrapper.classList.add("active");
                            localStorage.setItem("selectedOutletName", vendor.name);
                            handleOutletSelection(vendor.vendor_id, vendor.logo_url);
                        });
                    
                        wrapper.appendChild(logo);
                        logoContainer.appendChild(wrapper);
                    });
                    
    
                    // Add spacer and "+" button
                    const spacer = document.createElement("div");
                    spacer.style.flex = "1";
    
                    const addBtnWrapper = document.createElement("div");
                    addBtnWrapper.className = "add-btn-wrapper flex-shrink-0 ms-2";
                    addBtnWrapper.innerHTML = `
                        <button id="add-outlet-btn" class="btn add-outlet-btn">+</button>
                    `;
    
                    logoContainer.appendChild(spacer);
                    logoContainer.appendChild(addBtnWrapper);
    
                    AddOutletService.init();
                }
            })
            .catch(error => {
                console.error("Error fetching vendor logos:", error);
            });
        }
    }
    
    function handleOutletSelection(vendorId, vendor_logo) {
        localStorage.setItem("activeVendor", vendorId);
        localStorage.setItem("activeVendorLogo", vendor_logo);
    
        const chatContainer = document.getElementById("chat-container");
        chatContainer.innerHTML = "";
    
        const outletName = localStorage.getItem("selectedOutletName") || "our outlet";
        showWelcomeMessage(outletName);
    
        // Flag to prevent history messages from being re-saved
        window.isRestoringHistory = true;
    
        const historyKey = `chat_history_${vendorId}`;
        const cachedMessages = JSON.parse(localStorage.getItem(historyKey)) || [];
    
        cachedMessages.forEach(msg => {
            appendMessage(msg.text, msg.sender, msg.timestamp); // Pass the saved timestamp
        });
    
        // Done restoring history
        window.isRestoringHistory = false;
    
        // fetchVendorData(vendorId); // Optional fresh fetch
    }   
    
    function showWelcomeMessage(outletName) {
        const chatContainer = document.getElementById("chat-container");
        if (!chatContainer) return;
    
        const messages = [
            `Hi, Good Day! Welcome to ${outletName}.`,
            "Kindly enter the Bill Number and Send so that we can track your order."
        ];
    
        messages.forEach(msg => {
            const messageRow = document.createElement("div");
            messageRow.classList.add("message-row", "server");
    
            const logoImg = document.createElement("img");
            logoImg.src = localStorage.getItem("activeVendorLogo") || "/static/images/default-logo.png";
            logoImg.alt = "Vendor Logo";
            logoImg.className = "server-logo";
    
            const messageBubble = document.createElement("div");
            messageBubble.classList.add("message-bubble", "server");
            messageBubble.textContent = msg;
    
            messageRow.appendChild(logoImg);
            messageRow.appendChild(messageBubble);
            chatContainer.appendChild(messageRow);
        });
    
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
    
    


    if (ratingButton) {
        ratingButton.addEventListener('click', function () {
            console.log("Rating button clicked");

            // Define the Google Place ID for Softland India Ltd
            const placeId = "ChIJQ94r10S-BTsRDtOmYzIplto"; // Softland India Ltd

            // Construct the Google Review URL
            const googleReviewUrl = `https://search.google.com/local/writereview?placeid=${placeId}`;

            // Open the review page in a new browser tab
            window.open(googleReviewUrl, "_blank");
        });
    } else {
        console.error("Rating button not found.");
    }

    let notificationsEnabled = true;
    const isAndroid = /Android/i.test(navigator.userAgent);
    console.log("Android device:", isAndroid);
    function adjustKeyboardOffset() {
        const isAndroid = /Android/i.test(navigator.userAgent);
        document.documentElement.style.setProperty('--keyboard-offset', isAndroid ? '210px' : '150px');
        console.log("Keyboard offset set for", isAndroid ? "Android" : "Other");
    }
    
    window.addEventListener('load', adjustKeyboardOffset);
    window.addEventListener('resize', adjustKeyboardOffset);
    
    // Adjust viewport for mobile devices
    function setDynamicVH() {
        let vh = window.innerHeight * 0.01;
        document.documentElement.style.setProperty('--vh', `${vh}px`);
    }
    window.addEventListener('resize', setDynamicVH);
    setDynamicVH();
    
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
        alert("It looks like you're using Brave. Please ensure:\n\n1. Brave Settings > Privacy and Security > Site and Shields Settings > Notifications > 'Sites can ask to send notifications' is ON.\n2. Enable 'Use Google Services for Push Messaging' if shown.\n\nOtherwise, push notifications may fail.");
    }
    initNotificationModal(notificationModal);
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
    async function subscribeToPushNotifications(token,vendor_id) {
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
                    endpoint: sub.endpoint,       
                    keys: sub.keys,               
                    browser_id: getBrowserId(),   
                    token_number: token,
                    vendor:vendor_id
                };
                                
                const response = await fetch('/vendors/api/save-subscription/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' ,
                        'X-CSRFToken': AppUtils.getCSRFToken()
                    },
                    credentials: "same-origin",
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
                    <strong>${pushData.name || "Unknown"}</strong><br>
                    <strong>Status:</strong> ${pushData.status || "Unknown"}<br>
                    <strong>Counter No:</strong> ${pushData.counter_no || ""}<br>
                    <strong>Token No:</strong> ${pushData.token_no || ""}
                `;
                appendMessage(messageHTML, 'server');
                if (pushData.status === "ready") {
                    const orderReadyMessage = new SpeechSynthesisUtterance(`Your Order ${pushData.token_no} is Ready at Counter ${pushData.counter_no}`);
                    speechSynthesis.speak(orderReadyMessage);
                    if (navigator.vibrate) {
                        navigator.vibrate([500, 200, 500, 200, 500, 200, 500]);
                    }
                }
                showNotificationModal(pushData);
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

    function appendMessage(text, sender, timestamp = null) {
        const messageRow = document.createElement('div');
        messageRow.classList.add('message-row', sender);
        
        // Use the passed timestamp if available, else generate the current time
        const timeStamp = timestamp || new Date().toLocaleTimeString([], { 
            hour: '2-digit', 
            minute: '2-digit', 
            hour12: true 
        });
    
        const messageBubble = document.createElement('div');
        messageBubble.classList.add('message-bubble', sender);
        messageBubble.innerHTML = `
            <div class="message-row">
                <div class="message-content">${text}</div>
                <div class="message-timestamp">
                    ${timeStamp}
                    <span class="message-check">&#10003;</span>
                </div>
            </div>
        `;
        
        if (sender === 'server') {
            const activeLogo = localStorage.getItem("activeVendorLogo") || '/static/images/default-logo.png';
            const logoImg = document.createElement('img');
            logoImg.src = activeLogo;
            logoImg.alt = 'Vendor Logo';
            logoImg.className = 'server-logo';
            messageRow.appendChild(logoImg);
        }
        
        messageRow.appendChild(messageBubble);
        chatContainer.appendChild(messageRow);
        chatContainer.scrollTop = chatContainer.scrollHeight;
        
        // ✅ Save only if not restoring history
        if (!window.isRestoringHistory) {
            const activeVendorId = localStorage.getItem("activeVendor");
            if (activeVendorId) {
                const historyKey = `chat_history_${activeVendorId}`;
                const existing = JSON.parse(localStorage.getItem(historyKey)) || [];
                existing.push({ text, sender, timestamp: timeStamp }); // Save the timestamp
                localStorage.setItem(historyKey, JSON.stringify(existing));
            }
        }
    }
    // Send button logic
    sendButton.addEventListener('click', async function () {
        const message = chatInput.value.trim();
        if (message !== '') {
            const granted = await PermissionService.requestPermissions();

            if (!granted) {
                console.warn("Notification not enabled. Proceeding without push alerts.");
            }

            if (IosPwaInstallService.shouldRePrompt()) {
                IosPwaInstallService.showModal();
            }

            appendMessage(message, 'user');
            chatInput.value = '';
            fetchOrderStatusOnce(message);
        }
    });


    // Single check to confirm the order status
    function fetchOrderStatusOnce(token) {
        const activeVendor = AppUtils.getActiveVendor();
        console.log("Active Vendor ID in order update:", activeVendor);
    
        fetch(`/check-status/?token_no=${token}&vendor_id=${activeVendor}`)
            .then(async (response) => {
                const responseData = await response.json();
    
                if (!response.ok) {
                    const errorMessage = responseData.error || "An unknown error occurred.";
                    appendMessage(`❌ ${errorMessage}`, 'server');
                    throw new Error(`Server responded with error: ${errorMessage}`);
                }
    
                const data = responseData;
                console.log(data);
                const messageHTML = `
                    <strong>${data.name || "Unknown"}</strong><br>
                    <strong>Status:</strong> ${data.status || "Unknown"}<br>
                    <strong>Counter No:</strong> ${data.counter_no || "N/A"}<br>
                    <strong>Token No:</strong> ${token}
                `;
                appendMessage(messageHTML, 'server');
    
                // If status is ready, notify user
                if (data.status === "ready") {
                    showNotificationModal(data);
                    const orderReadyMessage = new SpeechSynthesisUtterance(
                        `Your Order ${token} is ${data.status} at the counter ${data.counter_no}.`
                    );
                    speechSynthesis.speak(orderReadyMessage);
                    if (navigator.vibrate) {
                        navigator.vibrate([500, 200, 500, 200, 500, 200, 500]);
                    }
                }
    
                // Subscribe for push notifications
                subscribeToPushNotifications(token, data.vendor);
            })
            .catch(error => {
                console.error("Error fetching order status:", error);
                if (!error.handled) {
                    appendMessage("⚠️ Something went wrong. Please try again.", 'server');
                }
            });
    }
    

    function showChatWindow(data) {
        const chatContainer = document.querySelector('.chat-container');
        const chatInput = document.getElementById('chat-input'); 
    
        if (!chatContainer || !chatInput) return;
    
        // Temporarily hide and show chat
        chatContainer.style.display = "none";
        setTimeout(() => {
            chatContainer.style.display = "block";
        }, 100);
    
        // Auto-scroll
        setTimeout(() => {
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }, 50);
    
        // Set token if available
        if (data && data.token_no) {
            chatInput.value = data.token_no;
            chatInput.value = '';  
        }
    
        chatContainer.scrollIntoView({ behavior: "smooth" });
    
        console.log("Chat window is now open or refreshed.", data);
    }    
});
