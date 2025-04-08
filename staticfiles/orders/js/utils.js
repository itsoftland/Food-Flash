window.getCSRFToken = function () {
    const meta = document.querySelector('meta[name="csrf-token"]');
    return meta ? meta.getAttribute("content") : "";
};

// Location ID Utils
function setCurrentLocation(locationId) {
    if (locationId) {
        localStorage.setItem('activeLocation', locationId);
    }
}

function getCurrentLocation() {
    return localStorage.getItem('activeLocation') || null;
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

    // ✅ Replace instead of merge
    const updatedList = Array.from(new Set(newVendors));

    localStorage.setItem('selectedVendors', JSON.stringify(updatedList));

    if (updatedList.length > 0) {
        localStorage.setItem('activeVendor', updatedList[updatedList.length - 1]);
    }
}


function getActiveVendor() {
    return localStorage.getItem('activeVendor') ? parseInt(localStorage.getItem('activeVendor'), 10) : null;
}
