import { get as idbGet, set as idbSet } from "https://cdnjs.cloudflare.com/ajax/libs/idb-keyval/6.2.1/index.min.js";
if (window.navigator.standalone) {
    console.log('Running in standalone mode');
}
window.AppUtils = {
    // ─────────────────────────────────────
    // CSRF Token
    // ─────────────────────────────────────
    getCSRFToken: function () {
        const meta = document.querySelector('meta[name="csrf-token"]');
        return meta ? meta.getAttribute("content") : "";
    },
    key: 'activeLocation',
    async get() {
        // 1️⃣ Try localStorage
        let locationId = localStorage.getItem(this.key);
        if (locationId) {
          console.log("[LocationStore] Loaded from localStorage:", locationId);
          return locationId;
        }
    
        // 2️⃣ Try IndexedDB
        try {
          locationId = await idbGet(this.key);
          if (locationId) {
            console.log("[LocationStore] Loaded from IndexedDB:", locationId);
            localStorage.setItem(this.key, locationId); // Rehydrate
            return locationId;
          }
        } catch (e) {
          console.warn("[LocationStore] IndexedDB read failed:", e);
        }
    
        // 3️⃣ Try Cookie (after slight delay for PWA cold boot)
        await new Promise(resolve => setTimeout(resolve, 200));
        locationId = this.getCookie(this.key);
        if (locationId) {
          console.log("[LocationStore] Loaded from Cookie:", locationId);
          localStorage.setItem(this.key, locationId); // Rehydrate
          try { await idbSet(this.key, locationId); } catch {}
          return locationId;
        }
    
        console.warn("[LocationStore] No activeLocation found in any storage.");
        return null;
      },
    async set(locationId) {
    if (!locationId) return;
    console.log("[LocationStore] Setting location:", locationId);

    // 1️⃣ Set in localStorage
    localStorage.setItem(this.key, locationId);

    // 2️⃣ Set in IndexedDB
    try {
        await idbSet(this.key, locationId);
    } catch (e) {
        console.warn("[LocationStore] IndexedDB write failed:", e);
    }

    // 3️⃣ Set in cookie
    this.setCookie(this.key, locationId);
    },

    setCookie(name, value, days = 365) {
    const expires = new Date(Date.now() + days * 864e5).toUTCString();
    document.cookie = `${name}=${encodeURIComponent(value)}; path=/; expires=${expires}; SameSite=Lax`;
    },

    getCookie(name) {
    const cookieStr = `; ${document.cookie}`;
    const parts = cookieStr.split(`; ${name}=`);
    if (parts.length >= 2) {
        return decodeURIComponent(parts.pop().split(';')[0]);
    }
    return null;
    },

    // ─────────────────────────────────────
    // Vendor Helpers
    // ─────────────────────────────────────
    getStoredVendors: function () {
        const storedVendors = localStorage.getItem('selectedVendors');
        return storedVendors ? JSON.parse(storedVendors) : [];
    },
    setSelectedOutletName: function (name) {
        localStorage.setItem('selectedOutletName', name);
    },

    getSelectedOutletName: function () {
        const outletName = localStorage.getItem('selectedOutletName');
        return outletName ? outletName : null;
    },

    setCurrentVendors: function (vendorInput) {
        let newVendors = [];

        if (typeof vendorInput === 'string') {
            newVendors = vendorInput.split(',').map(v => parseInt(v.trim(), 10));
        } else if (Array.isArray(vendorInput)) {
            newVendors = vendorInput.map(v => parseInt(v, 10));
        }

        const updatedList = Array.from(new Set(newVendors));
        localStorage.setItem('selectedVendors', JSON.stringify(updatedList));

        if (updatedList.length > 0) {
            localStorage.setItem('activeVendor', updatedList[updatedList.length - 1]);
        }
    },
    appendVendorIfNotExists: function (vendorId) {
        // Append the vendorId to the list
        let selectedVendors = JSON.parse(localStorage.getItem('selectedVendors')) || [];
        selectedVendors.push(vendorId);

        // Update localStorage with the new list (ensure uniqueness)
        const updatedList = Array.from(new Set(selectedVendors));
        localStorage.setItem('selectedVendors', JSON.stringify(updatedList));

        // Optionally update activeVendor to the new vendorId
        localStorage.setItem('activeVendor', updatedList[updatedList.length - 1]);
    },    
    getActiveVendor: function () {
        return localStorage.getItem('activeVendor') ? parseInt(localStorage.getItem('activeVendor'), 10) : null;
    },

    // ─────────────────────────────────────
    // Notification Sound
    // ─────────────────────────────────────
    playNotificationSound: function (volume = 1.0) {
        const notificationAudio = new Audio('/static/orders/audio/0112.mp3');
        notificationAudio.volume = Math.max(0, Math.min(volume, 1));
        notificationAudio.play().catch(err =>
            console.error('Error playing notification sound:', err)
        );
    },
    // ─────────────────────────────────────
    // Viewport Utility
    // ─────────────────────────────────────
    adjustChatResponsePadding: function () {
        const chatResponse = document.querySelector('.chat-response');
        const chatFooter = document.querySelector('.chat-footer');
        const premiumFooter = document.querySelector('.premium-footer');
    
        if (!chatResponse) return;
    
        const chatFooterHeight = chatFooter?.offsetHeight || 0;
        const premiumFooterHeight = premiumFooter?.offsetHeight || 0;
    
        const viewportHeight = window.visualViewport?.height || window.innerHeight;
        const keyboardOffset = window.innerHeight - viewportHeight;
    
        const totalBottomOffset = chatFooterHeight + premiumFooterHeight + keyboardOffset;
    
        chatResponse.style.paddingBottom = `${totalBottomOffset}px`; // Add safe spacing
    
        // Optional: Dynamically limit height if needed
        const topOffset = 120; // Same as your padding-top
        const calculatedHeight = viewportHeight - chatFooterHeight - premiumFooterHeight - 20;
        chatResponse.style.maxHeight = `${calculatedHeight}px`;
    },
    initPaddingAdjustmentListeners: function () {
        const self = this;
        const adjust = () => self.adjustChatResponsePadding();
    
        window.addEventListener('load', adjust);
        window.addEventListener('resize', adjust);
        window.visualViewport?.addEventListener('resize', adjust);
        window.addEventListener('focusin', adjust);
        window.addEventListener('focusout', adjust);
    },

    showToast: function(message) {
        const toast = document.getElementById('customToast');
        toast.textContent = message;
        toast.classList.add('show');
        setTimeout(() => {
          toast.classList.remove('show');
        }, 3000); // 3 seconds
    },
    // ─────────────────────────────────────
    // Notification State (Persistent)
    // ─────────────────────────────────────
    notificationStorageKey: "notification_order_states",

    saveOrderStates: function (orderStates) {
        try {
            localStorage.setItem(this.notificationStorageKey, JSON.stringify(orderStates));
        } catch (e) {
            console.error("Failed to save orderStates to storage", e);
        }
    },

    loadOrderStates: function () {
        try {
            const stored = localStorage.getItem(this.notificationStorageKey);
            return stored ? JSON.parse(stored) : {};
        } catch (e) {
            console.error("Failed to load orderStates from storage", e);
            return {};
        }
    },
    // ─────────────────────────────────────
    // Order Ready Notification (Persistent)
    // ─────────────────────────────────────
    notifyOrderReady: function(pushData) {
        try {
            // Speech synthesis
            const orderReadyMessage = new SpeechSynthesisUtterance(`Your Order ${pushData.token_no} is Ready at Counter ${pushData.counter_no}`);
            speechSynthesis.speak(orderReadyMessage);

            // Vibration if supported
            if (navigator.vibrate) {
                navigator.vibrate([500, 200, 500, 200, 500, 200, 500]);
            }
        } catch (e) {
            console.error("Failed to notify order readiness", e);
        }
    },
    /**
         * Convert a base64 VAPID public key to a Uint8Array
         * for use with the PushManager.subscribe() method.
         */
    urlBase64ToUint8Array: function (base64String) {
        const padding = '='.repeat((4 - (base64String.length % 4)) % 4);
        const base64 = (base64String + padding)
            .replace(/-/g, '+')
            .replace(/_/g, '/');
        const rawData = window.atob(base64);
        const outputArray = new Uint8Array(rawData.length);
        for (let i = 0; i < rawData.length; ++i) {
            outputArray[i] = rawData.charCodeAt(i);
        }
        return outputArray;
    },

    /**
     * Get or generate a unique browser identifier.
     * Stores and retrieves it from localStorage.
     */
    getBrowserId: function () {
        let browserId = localStorage.getItem('browser_id');
        if (!browserId) {
            browserId = crypto.randomUUID();
            localStorage.setItem('browser_id', browserId);
        }
        return browserId;
    }   
};

