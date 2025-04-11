// --- CSRF Token Utility ---
window.getCSRFToken = function () {
    const meta = document.querySelector('meta[name="csrf-token"]');
    return meta ? meta.getAttribute("content") : "";
};

// --- Cookie Helpers ---
function setCookie(name, value, days = 365) {
    const expires = new Date(Date.now() + days * 864e5).toUTCString();
    document.cookie = `${name}=${encodeURIComponent(value)}; path=/; expires=${expires}; SameSite=Lax`;
}

function getCookie(name) {
    const cookieStr = `; ${document.cookie}`;
    const parts = cookieStr.split(`; ${name}=`);
    if (parts.length >= 2) {
        return decodeURIComponent(parts.pop().split(';')[0]);
    }
    return null;
}

// --- Location ID Utils (with fallback) ---
function setCurrentLocation(locationId) {
    if (locationId) {
        console.log("Setting location:", locationId);
        localStorage.setItem('activeLocation', locationId);
        setCookie('activeLocation', locationId);
    }
}


function getCurrentLocation() {
    let locationId = localStorage.getItem('activeLocation');
    console.log("LocalStorage location:", locationId);

    if (!locationId) {
        locationId = getCookie('activeLocation');
        console.log("Fallback Cookie location:", locationId);

        if (locationId) {
            localStorage.setItem('activeLocation', locationId); // Rehydrate
        }
    }

    return locationId || null;
}

// --- Vendor Helpers ---
function getStoredVendors() {
    const storedVendors = localStorage.getItem('selectedVendors');
    return storedVendors ? JSON.parse(storedVendors) : [];
}

function setCurrentVendors(vendorInput) {
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
}

function getActiveVendor() {
    return localStorage.getItem('activeVendor') ? parseInt(localStorage.getItem('activeVendor'), 10) : null;
}
