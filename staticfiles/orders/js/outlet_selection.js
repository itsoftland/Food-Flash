let locationId = null; // <-- define globally
document.addEventListener("DOMContentLoaded", function () {
    const urlParams = new URLSearchParams(window.location.search);
    locationId = urlParams.get("location_id");

    if (!locationId) {
        console.error("No location_id found in URL");
        return;
    }
    fetch(`/api/outlets/?location_id=${locationId}`)
        .then(response => response.json())
        .then(data => {
            const outletList = document.getElementById("outlet-list");
            outletList.innerHTML = ""; // Clear previous content

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
    console.log("vendorids",vendorIds)
    console.log("locationid",locationId)
    window.location.href = `/home/?location_id=${locationId}&vendor_id=${vendorIds}`;
});

