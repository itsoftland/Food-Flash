export const MenuModalService = (() => {
    const menuContent = document.getElementById("menuContent");

    const renderMenu = (fileList) => {
        if (!fileList || fileList.length === 0) {
            menuContent.innerHTML = `<p class="text-danger">No menu available.</p>`;
            return;
        }

        const imageFiles = fileList.filter(f => /\.(jpg|jpeg|png|webp)$/i.test(f));
        const pdfFiles = fileList.filter(f => /\.pdf$/i.test(f));

        menuContent.innerHTML = ""; // Clear previous content

        if (pdfFiles.length > 0 && imageFiles.length === 0) {
            // Single PDF shown in iframe
            menuContent.innerHTML = `
                <iframe src="${pdfFiles[0]}" width="100%" height="500px" frameborder="0"></iframe>
            `;
            return;
        }

        if (imageFiles.length === 1 && pdfFiles.length === 0) {
            menuContent.innerHTML = `
                <img src="${imageFiles[0]}" alt="Menu" class="img-fluid" onerror="this.src='/static/default-menu.jpg'">
            `;
            return;
        }

        if (imageFiles.length > 1) {
            const carouselId = "menuCarousel";
            menuContent.innerHTML = `
                <div id="${carouselId}" class="carousel slide" data-bs-ride="carousel">
                    <div class="carousel-inner">
                        ${imageFiles.map((file, index) => `
                            <div class="carousel-item ${index === 0 ? "active" : ""}">
                                <img src="${file}" class="d-block w-100" alt="Menu Page ${index + 1}">
                            </div>
                        `).join("")}
                    </div>
                    <button class="carousel-control-prev" type="button" data-bs-target="#${carouselId}" data-bs-slide="prev">
                        <span class="carousel-control-prev-icon"></span>
                    </button>
                    <button class="carousel-control-next" type="button" data-bs-target="#${carouselId}" data-bs-slide="next">
                        <span class="carousel-control-next-icon"></span>
                    </button>
                </div>
            `;
            return;
        }

        // Mixed or unsupported
        menuContent.innerHTML = `<p class="text-warning">Unsupported or mixed format.</p>`;
    };

    const openModalWithFiles = (filePaths) => {
        renderMenu(filePaths);

        const modal = new bootstrap.Modal(document.getElementById("menuImageModal"), {
            backdrop: 'static',
            keyboard: false
        });
        modal.show();
    };

    const bindEvents = () => {
        const menuButton = document.getElementById("menu-button");
        if (menuButton) {
            menuButton.addEventListener("click", async function () {
                const activeVendorId = localStorage.getItem("activeVendor");

                if (!activeVendorId) {
                    alert("No active vendor selected.");
                    return;
                }

                try {
                    const res = await fetch(`/api/menus/`, {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({ vendor_ids: [parseInt(activeVendorId)] })
                    });

                    if (!res.ok) throw new Error("Menu not found");

                    const data = await res.json();

                    if (!Array.isArray(data) || data.length === 0) {
                        throw new Error("No menu data");
                    }

                    const vendorMenu = data[0];  // single vendor expected
                    const menuFiles = vendorMenu.menus || [];

                    openModalWithFiles(menuFiles);
                } catch (err) {
                    console.error("Menu fetch failed:", err);
                    menuContent.innerHTML = `<p class="text-danger">Failed to load menu.</p>`;
                    const modal = new bootstrap.Modal(document.getElementById("menuImageModal"), {
                        backdrop: 'static',
                        keyboard: false
                    });
                    modal.show();
                }
            });
        }
    };

    return {
        init: bindEvents,
        openModalWithFiles
    };
})();
