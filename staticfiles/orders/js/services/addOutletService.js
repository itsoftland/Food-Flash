export const AddOutletService = (() => {
    let locationId = null;
    let selectedVendorIds = new Set();

    const fetchOutlets = async () => {
        try {
            const response = await fetch(`/api/outlets/?location_id=${locationId}`);
            return response.ok ? await response.json() : [];
        } catch (err) {
            console.error("Fetch error:", err);
            return [];
        }
    };

    const toggleSelection = (tile, vendorId) => {
        tile.classList.toggle("selected");
        tile.classList.contains("selected")
            ? selectedVendorIds.add(vendorId)
            : selectedVendorIds.delete(vendorId);
    };

    const renderOutlets = (outlets) => {
        const outletList = document.getElementById("outlet-list");
        outletList.innerHTML = outlets.length
            ? ""
            : "<p class='text-center'>No outlets found</p>";

        outlets.forEach(outlet => {
            const tile = document.createElement("div");
            tile.className = "outlet-tile";
            tile.dataset.vendorId = outlet.vendor_id;
            tile.dataset.name = outlet.name;
            tile.dataset.location = outlet.location || "";

            tile.innerHTML = `
                <img src="${outlet.logo || '/static/default-logo.png'}" alt="${outlet.name}">
                <p class="outlet-name">${outlet.name}</p>
                <p class="outlet-location">${outlet.location || ''}</p>
            `;

            if (selectedVendorIds.has(String(outlet.vendor_id))) {
                tile.classList.add("selected");
            }

            tile.addEventListener("click", () => {
                toggleSelection(tile, String(outlet.vendor_id));
            });

            outletList.appendChild(tile);
        });
    };

    const openModal = async () => {
        locationId = getCurrentLocation(); // from utils.js

        if (!locationId) {
            alert("Location ID is missing. Please scan or provide location.");
            return;
        }

        selectedVendorIds.clear();

        // Ensure vendor IDs are stored as strings
        const storedVendorIds = getStoredVendors().map(String);
        storedVendorIds.forEach(id => selectedVendorIds.add(id));

        const outlets = await fetchOutlets();
        renderOutlets(outlets);

        // Show modal
        const modal = document.getElementById("addOutletModal");
        if (modal) {
            modal.classList.add("show");
            modal.style.display = "block";
            document.body.classList.add("modal-open");
        }
    };

    const bindEvents = () => {
        document.getElementById("add-outlet-btn")?.addEventListener("click", openModal);

        document.getElementById("continue-btn")?.addEventListener("click", () => {
            if (selectedVendorIds.size === 0) {
                alert("Please select at least one outlet.");
                return;
            }

            const finalVendorIds = Array.from(selectedVendorIds).join(",");
            window.location.href = `/home/?location_id=${locationId}&vendor_id=${finalVendorIds}`;
        });
    };

    return {
        init: bindEvents
    };
})();
