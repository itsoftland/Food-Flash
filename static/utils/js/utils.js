// Global utility object to store reusable helper functions
window.AppUtils = {

    // ─────────────────────────────────────
    // CSRF Token Utilities
    // ─────────────────────────────────────

    // Retrieves the CSRF token from a meta tag in the HTML document
    // Useful for making secure POST/PUT/DELETE requests in Django
    getCSRFToken: function () {
        const meta = document.querySelector('meta[name="csrf-token"]');
        return meta ? meta.getAttribute("content") : "";
    },

    // ─────────────────────────────────────
    // Customer ID Helpers (Local Storage)
    // ─────────────────────────────────────

    // Stores the customer ID in localStorage under the key 'customer_id'
    // Useful for tracking/logging user activity across pages
    setCustomerId: function (name) {
        localStorage.setItem('customer_id', name);
    },

    // Retrieves the customer ID from localStorage, or returns null if not set
    // Can be used to fetch customer-specific data or personalize UI
    getCustomerId: function () {
        const customerId = localStorage.getItem('customer_id');
        return customerId ? customerId : null;
    }
};
