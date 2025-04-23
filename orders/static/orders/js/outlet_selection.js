import { IosPwaInstallService } from './services/iosPwaInstallService.js';
let locationId = null; 
document.addEventListener("DOMContentLoaded", function () {
    IosPwaInstallService.init();
    // Handle Agree Button
    const agreeBtn = document.getElementById("ios-a2hs-agree");
    if (agreeBtn) {
        agreeBtn.addEventListener("click", () => {
            localStorage.setItem("iosA2HS", "true");
            IosPwaInstallService.dismiss();
        });
    }

    // Handle Deny Button
    const denyBtn = document.getElementById("ios-a2hs-deny");
    if (denyBtn) {
        denyBtn.addEventListener("click", () => {
            localStorage.setItem("iosA2HS", "false");
            IosPwaInstallService.dismiss();
        });
    }

    const urlParams = new URLSearchParams(window.location.search);
    locationId = urlParams.get("location_id");

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

    if (window.location.pathname === "/" && !window.location.search.includes("location_id")) {
        if (locationId) {
            console.log("Redirecting to location_id from localStorage...");
            window.location.href = `/?location_id=${locationId}`;
        }
    }

    fetch(`/api/outlets/?location_id=${locationId}`)
        .then(response => response.json())
        .then(data => {
            const outletList = document.getElementById("outlet-list");
            outletList.innerHTML = "";

            if (data.length === 0) {
                outletList.innerHTML = "<p class='text-center'>No outlets found</p>";
                return;
            }

            data.forEach(outlet => {
                const tile = document.createElement("div");
                tile.className = "outlet-tile";
                // Add attributes for later access
                tile.dataset.vendorId = outlet.vendor_id;
                tile.dataset.name = outlet.name;
                tile.dataset.location = outlet.location || '';
            
                tile.innerHTML = `
                    <img src="${outlet.logo || '/static/default-logo.png'}" alt="${outlet.name}">
                    <p class="outlet-name">${outlet.name}</p>
                    <p class="outlet-location">${outlet.location || ''}</p>
                `;
                
                tile.addEventListener("click", function () {
                    tile.classList.toggle("selected");
                });
            
                outletList.appendChild(tile);
            });
            
        })
        .catch(error => console.error("Error fetching outlets:", error));
});

// Continue Button Click Event
document.getElementById("continue-btn").addEventListener("click", function () {
    const selectedOutlets = document.querySelectorAll(".outlet-tile.selected");

    if (selectedOutlets.length === 0) {
        alert("Please select at least one outlet.");
        return;
    }

    // Extract all necessary data
    const selectedData = [...selectedOutlets].map(tile => ({
        vendor_id: tile.dataset.vendorId,
        name: tile.dataset.name,
        location: tile.dataset.location, 
    }));

    console.log("Selected Outlet Data:", selectedData);

    // Redirect with vendor IDs (can modify as per your logic)
    const vendorIds = selectedData.map(outlet => outlet.vendor_id).join(",");
    window.location.href = `/home/?location_id=${locationId}&vendor_id=${vendorIds}`;
});

