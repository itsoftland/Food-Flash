window.AppUtils = {
    // ─────────────────────────────────────
    // CSRF Token
    // ─────────────────────────────────────
    getCSRFToken: function () {
        const meta = document.querySelector('meta[name="csrf-token"]');
        return meta ? meta.getAttribute("content") : "";
    },

    // ─────────────────────────────────────
    // Cookies
    // ─────────────────────────────────────
    setCookie: function (name, value, days = 365) {
        const expires = new Date(Date.now() + days * 864e5).toUTCString();
        document.cookie = `${name}=${encodeURIComponent(value)}; path=/; expires=${expires}; SameSite=Lax`;
    },

    getCookie: function (name) {
        const cookieStr = `; ${document.cookie}`;
        const parts = cookieStr.split(`; ${name}=`);
        if (parts.length >= 2) {
            return decodeURIComponent(parts.pop().split(';')[0]);
        }
        return null;
    },

    // ─────────────────────────────────────
    // Location ID
    // ─────────────────────────────────────
    setCurrentLocation: function (locationId) {
        if (locationId) {
            console.log("Setting location:", locationId);
            localStorage.setItem('activeLocation', locationId);
            this.setCookie('activeLocation', locationId);
        }
    },

    getCurrentLocation: function () {
        let locationId = localStorage.getItem('activeLocation');
        console.log("LocalStorage location:", locationId);

        if (!locationId) {
            locationId = this.getCookie('activeLocation');
            console.log("Fallback Cookie location:", locationId);

            if (locationId) {
                localStorage.setItem('activeLocation', locationId); // Rehydrate
            }
        }

        return locationId || null;
    },

    // ─────────────────────────────────────
    // Vendor Helpers
    // ─────────────────────────────────────
    getStoredVendors: function () {
        const storedVendors = localStorage.getItem('selectedVendors');
        return storedVendors ? JSON.parse(storedVendors) : [];
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
    setViewportHeightVar: function () {
        const vh = window.innerHeight * 0.01;
        document.documentElement.style.setProperty('--vh', `${vh}px`);
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
    }
      
};

// Initialize viewport handlers
window.addEventListener('resize', AppUtils.setViewportHeightVar);
window.addEventListener('orientationchange', AppUtils.setViewportHeightVar);
document.addEventListener('DOMContentLoaded', AppUtils.setViewportHeightVar);
window.addEventListener('load', AppUtils.setViewportHeightVar);
window.addEventListener('focusin', AppUtils.setViewportHeightVar);
window.addEventListener('focusout', AppUtils.setViewportHeightVar);

if (window.visualViewport) {
    window.visualViewport.addEventListener('resize', () => {
        const isKeyboardOpen = window.visualViewport.height < window.innerHeight;
        document.body.classList.toggle('keyboard-open', isKeyboardOpen);
    });
}
