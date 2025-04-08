window.getCSRFToken = function () {
    const meta = document.querySelector('meta[name="csrf-token"]');
    return meta ? meta.getAttribute("content") : "";
};

// utils.js

// Location ID Utils
function setCurrentLocation(locationId) {
    if (locationId) {
        localStorage.setItem('activeLocation', locationId);
    }
}

function getCurrentLocation() {
    return localStorage.getItem('activeLocation') || null;
}

