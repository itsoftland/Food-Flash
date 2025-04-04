// document.addEventListener("DOMContentLoaded", function () {
//     const locationId = 2001; // Change dynamically as needed
//     fetch(`/api/outlets/?location_id=${locationId}`)
//         .then(response => response.json())
//         .then(data => {
//             const outletList = document.getElementById("outlet-list");
//             outletList.innerHTML = ""; // Clear previous content

//             if (data.length === 0) {
//                 outletList.innerHTML = "<p class='text-center'>No outlets found</p>";
//                 return;
//             }

//             data.forEach(outlet => {
//                 const col = document.createElement("div");
//                 col.className = "col-md-3 col-sm-6";  // Responsive tiles
                
//                 col.innerHTML = `
//                     <div class="outlet-tile" onclick="toggleSelect(this)">
//                         <img src="${outlet.logo || '/static/default-logo.png'}" alt="${outlet.name}">
//                         <p>${outlet.name}</p>
//                     </div>
//                 `;
//                 outletList.appendChild(col);
//             });
//         })
//         .catch(error => console.error("Error fetching outlets:", error));
// });

// function toggleSelect(element) {
//     element.classList.toggle("selected");
// }

document.addEventListener("DOMContentLoaded", function () {
    const locationId = 2001; // Change dynamically as needed
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
        location: tile.dataset.location
    }));

    console.log("Selected Outlet Data:", selectedData);

    // Redirect with vendor IDs (can modify as per your logic)
    const vendorIds = selectedData.map(outlet => outlet.vendor_id).join(",");
    console.log("vendorids",vendorIds)
    window.location.href = `/?vendor_id=${vendorIds}`;
});

