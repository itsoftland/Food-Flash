export const AdSliderService = (() => {
    const fetchAds = async (vendorIds) => {
        try {
            const response = await fetch("/api/get_vendor_ads/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken(),
                },
                credentials: "same-origin",
                body: JSON.stringify({ vendor_ids: vendorIds }),
            });

            if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error("Error fetching ads:", error);
            return [];
        }
    };

    const interleaveAds = (vendorAdsArray) => {
        const result = [];
        let i = 0;
        let hasMore = true;

        while (hasMore) {
            hasMore = false;
            for (const ads of vendorAdsArray) {
                if (i < ads.length) {
                    result.push(ads[i]);
                    hasMore = true;
                }
            }
            i++;
        }

        return result;
    };

    const renderAds = (ads, containerId = "ad-slider") => {
        const adContainer = document.getElementById(containerId);
        if (!adContainer) return;

        adContainer.innerHTML = "";

        const baseAds = [...ads];
        const allAds = baseAds.concat(baseAds); // Duplicate for infinite scroll

        allAds.forEach(adUrl => {
            const img = document.createElement("img");
            img.src = adUrl;
            img.alt = "Advertisement";
            img.classList.add("ad-slide");
             // ✅ iOS rendering fixes
            img.style.willChange = "transform";
            img.style.backfaceVisibility = "hidden";
            img.style.WebkitTransform = "translateZ(0)"; // iOS GPU trigger
            img.loading = "eager"; // force load early
            img.width = 180;
            img.height = 100;

            img.addEventListener("click", () => {
                openAdModal(adUrl);
            });

            adContainer.appendChild(img);
        });
        // 👇 Wait for layout paint before triggering animation
        requestAnimationFrame(() => {
            requestAnimationFrame(() => {
                adContainer.classList.add("start-scroll");
            });
        });
    };

    const openAdModal = (src) => {
        const modalElement = document.getElementById("ad-modal");
        const modalImg = document.getElementById("ad-modal-img");
    
        if (modalElement && modalImg) {
            modalImg.src = src;
            const bsModal = new bootstrap.Modal(modalElement, {
                backdrop: 'static',
                keyboard: false
            });
            bsModal.show();
        }
    };
    
    const initModalListeners = () => {
        const modalElement = document.getElementById("ad-modal");
        if (!modalElement) return;
    
        modalElement.addEventListener("hidden.bs.modal", () => {
            const modalImg = document.getElementById("ad-modal-img");
            if (modalImg) modalImg.src = ""; // clear when closed
        });
    };
    
    const init = () => {
        initModalListeners();
    };

    return {
        init,
        fetchAds,
        interleaveAds,
        renderAds
    };
})();
