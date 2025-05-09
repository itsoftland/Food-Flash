import { AddOutletService } from "./services/addOutletService.js"; 
import { MenuModalService } from './services/menuModalService.js';
import { FeedbackService } from "./services/feedBackService.js";
import { IosPwaInstallService } from './services/iosPwaInstallService.js';
import { PermissionService } from "./services/permissionService.js";
import { initNotificationModal, showNotificationModal } from './services/notificationService.js';
import { VendorUIService } from "./services/vendorUIService.js";
import { handleOutletSelection,appendMessage } from "./services/chatService.js";
import { PushSubscriptionService } from "./services/pushSubscriptionService.js";

document.addEventListener('DOMContentLoaded', async function() {
    AppUtils.initPaddingAdjustmentListeners();
    const notificationModal = new bootstrap.Modal(document.getElementById('notificationModal'));
    const chatInput = document.getElementById('chat-input');
    const sendButton = document.getElementById('send-button');
    const ratingButton = document.getElementById('rating-button');
    const urlParams = new URLSearchParams(window.location.search);
    let locationId = urlParams.get("location_id");
    const vendorFromQR = urlParams.get('vendor_id');

    // 1️⃣ Check URL param first
    if (locationId) {
        AppUtils.setCurrentLocation(locationId); // Store it
    } else {
        // 2️⃣ Fallback to localStorage
        locationId = AppUtils.getCurrentLocation();

        if (!locationId )  {
            // 3️⃣ Ask for it / show error / redirect
            AppUtils.showToast("No location ID found. Please select a location to proceed");
            // Optionally redirect to a location selection page
            window.location.href = "/";
            throw new Error("Missing location ID");
        }
    }

    if (vendorFromQR) {
        AppUtils.setCurrentVendors(vendorFromQR);
        // Optional: Clean the URL
        const newUrl = window.location.origin + window.location.pathname;
        history.replaceState(null, "", newUrl);
    } else {
        AddOutletService.init();
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
        VendorUIService.init(vendorIds);
    }
    if (ratingButton) {
        ratingButton.addEventListener('click', function () {
            console.log("Rating button clicked");
            let ratingLink = localStorage.getItem("activeVendorRatingLink") || "https://default-rating-link.com";
            // Construct the Google Review URL
            const googleReviewUrl = `https://search.google.com/local/writereview?placeid=${ratingLink}`;

            // Open the review page in a new browser tab
            window.open(googleReviewUrl, "_blank");
        });
    } else {
        console.error("Rating button not found.");
    }

    let notificationsEnabled = true;
    const isAndroid = /Android/i.test(navigator.userAgent);
    console.log("Android device:", isAndroid);    
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
        AppUtils.showToast("It looks like you're using Brave. Please ensure:\n\n1. Brave Settings > Privacy and Security > Site and Shields Settings > Notifications > 'Sites can ask to send notifications' is ON.\n2. Enable 'Use Google Services for Push Messaging' if shown.\n\nOtherwise, push notifications may fail");
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
                let selectedVendors = JSON.parse(localStorage.getItem('selectedVendors')) || [];
                // Check if the vendor is already in the list
                if (!selectedVendors.includes(pushData.vendor_id)) {
                    AppUtils.appendVendorIfNotExists(pushData.vendor_id);
                    const vendorIds = AppUtils.getStoredVendors();
                    VendorUIService.init(vendorIds);
                }
                updateChatOnPush(pushData.vendor_id,pushData.logo_url,pushData.name);
                // Customize the chat message as needed. Here we assume pushData contains token_number and status.
                
                const messageHTML = `
                    <div class="response-title">${pushData.name || "Unknown"}</div>
                    <div class="status">
                        Status: 
                        <span class="${pushData.status?.toLowerCase() === 'ready' ? 'ready-color' : 'preparing-color'}">
                            ${pushData.status || "Unknown"}
                        </span>
                    </div>
                    <div class="info-badges">
                        <div class="badge">Counter No: ${pushData.counter_no || ""}</div>
                        <div class="badge">Token No: ${pushData.token_no || ""}</div>
                    </div>
                `;
                const offerMessageHTML = `
                        <div class="response-title">${pushData.name}</div>
                        <div class="response-title">🔥 ${pushData.title}</div>
                        <div style="color: #333; font-size: 15px;">
                            ${pushData.body || "Delicious deals await. Come grab your favorite combo now!"}
                        </div>
                    
                `;

                if (pushData.type =="offers"){
                    appendMessage(offerMessageHTML, 'server');
                }else{
                if (pushData.status === "ready") {
                    AppUtils.notifyOrderReady(pushData); 
                    AppUtils.playNotificationSound();
                    showNotificationModal(pushData);
                    appendMessage(messageHTML, 'server');
                    }
                    
                }
                
            }
        });
    }
    function updateChatOnPush(vendorId,logo_url,name) {
        document.querySelectorAll(".vendor-logo-wrapper").forEach(wrapper => {
            const logo = wrapper.querySelector("img");
            if (logo.dataset.vendorId == vendorId) {
                // Clear all active states
                document.querySelectorAll(".vendor-logo-wrapper").forEach(w => w.classList.remove("active"));
                // Activate matching one
                wrapper.classList.add("active");
                localStorage.setItem("selectedOutletName", name);
                let ratingLink = localStorage.getItem("activeVendorRatingLink") || "https://default-rating-link.com";
                handleOutletSelection(vendorId,logo_url,ratingLink);
            }
        });
    }
    
    chatInput.addEventListener("keydown", function(event) {
        let inputValue = event.target.value;
        const originalValue = inputValue; // Save original for comparison
        // Remove non-numeric characters
        inputValue = inputValue.replace(/[^0-9]/g, '');
    
        // Restrict to 4 digits
        if (inputValue.length > 4) {
            inputValue = inputValue.substring(0, 4);
        }
    
        // Update the input value
        event.target.value = inputValue;
    
        // If invalid characters were typed
        if (originalValue !== inputValue) {
            appendMessage("Please Enter a valid Order No.", "server"); // or "left" if you use sides
        }
    
        // Handle Enter key
        if (event.key === "Enter") {
            event.preventDefault();
            sendButton.click();
        }
    });
    
    
    // Send button logic
    sendButton.addEventListener('click', async function () {
        const message = chatInput.value.trim();
        if (message !== '') {
            const granted = await PermissionService.requestPermissions();

            if (!granted) {
                AppUtils.showToast("Notification not enabled. Proceeding without push alerts");
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
                    <div class="response-title">${data.name || "Unknown"}</div>
                    <div class="status">
                        Status: 
                        <span class="${data.status?.toLowerCase() === 'ready' ? 'ready-color' : 'preparing-color'}">
                            ${data.status || "Unknown"}
                        </span>
                    </div>
                    <div class="info-badges">
                        <div class="badge">Counter No: ${data.counter_no || ""}</div>
                        <div class="badge">Token No: ${data.token_no || ""}</div>
                    </div>
                `;
                appendMessage(messageHTML, 'server');
    
                // If status is ready, notify user
                if (data.status === "ready") {
                    AppUtils.playNotificationSound();
                    showNotificationModal(data);
                    AppUtils.notifyOrderReady(data);
                }
    
                // Subscribe for push notifications
                PushSubscriptionService.subscribe(token, data.vendor);
                // subscribeToPushNotifications(token, data.vendor);
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
