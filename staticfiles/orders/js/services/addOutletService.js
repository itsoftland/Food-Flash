export const AddOutletService = (() => {
    let locationId = null;
    let selectedVendorIds = new Set();

    const getExistingVendors = () => {
        const urlParams = new URLSearchParams(window.location.search);
        const vendorIdsParam = urlParams.get("vendor_id");
        if (vendorIdsParam) {
            vendorIdsParam.split(",").forEach(id => selectedVendorIds.add(id));
        }
    };

    const fetchOutlets = async () => {
        try {
            const response = await fetch(`/api/outlets/?location_id=${locationId}`);
            if (!response.ok) {
                console.error("Error fetching outlets");
                return [];
            }
            return await response.json();
        } catch (err) {
            console.error("Fetch error:", err);
            return [];
        }
    };

    const toggleSelection = (tile, vendorId) => {
        tile.classList.toggle("selected");
        if (tile.classList.contains("selected")) {
            selectedVendorIds.add(vendorId);
        } else {
            selectedVendorIds.delete(vendorId);
        }
    };

    const renderOutlets = (outlets) => {
        const outletList = document.getElementById("outlet-list");
        outletList.innerHTML = "";

        if (outlets.length === 0) {
            outletList.innerHTML = "<p class='text-center'>No outlets found</p>";
            return;
        }

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
        console.log("Opening Add Outlet Modal...");
        locationId = getCurrentLocation();
        if (!locationId) {
            console.error("Missing location_id in URL");
            return;
        }

        selectedVendorIds.clear();
        getExistingVendors();
        console.log("existing vendors",getExistingVendors())

        const outlets = await fetchOutlets();
        renderOutlets(outlets);
    };

    const bindEvents = () => {
        const addOutletBtn = document.getElementById("add-outlet-btn");
        const continueBtn = document.getElementById("continue-btn");

        if (addOutletBtn) {
            addOutletBtn.addEventListener("click", openModal);
        }

        if (continueBtn) {
            continueBtn.addEventListener("click", () => {
                if (selectedVendorIds.size === 0) {
                    alert("Please select at least one outlet.");
                    return;
                }

                const finalVendorIds = Array.from(selectedVendorIds).join(",");
                window.location.href = `/home/?location_id=${locationId}&vendor_id=${finalVendorIds}`;
            });
        }
    };

    return {
        init: bindEvents
    };
})();
