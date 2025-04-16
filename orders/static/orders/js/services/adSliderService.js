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
        const container = document.getElementById(containerId);
        if (!container) return;

        container.innerHTML = "";

        const track = document.createElement("div");
        track.classList.add("ad-slider-track");

        const duplicatedAds = [...ads, ...ads]; // Infinite loop

        duplicatedAds.forEach(adUrl => {
            const img = document.createElement("img");
            img.src = adUrl;
            img.alt = "Advertisement";
            img.classList.add("ad-slide");

            // ✅ iOS-specific rendering fixes
            img.style.willChange = "transform";
            img.style.backfaceVisibility = "hidden";
            img.style.WebkitTransform = "translateZ(0)";
            img.loading = "eager";
            img.width = 180;
            img.height = 100;

            img.addEventListener("click", () => {
                openAdModal(adUrl);
            });

            track.appendChild(img);
        });

        container.appendChild(track);

        // Start scrolling using JavaScript transform loop
        startScroll(track);
    };

    const startScroll = (track) => {
        let offset = 0;
        const speed = 0.5; // px per frame

        const scroll = () => {
            offset -= speed;
            const resetThreshold = track.scrollWidth / 2;

            if (Math.abs(offset) >= resetThreshold) {
                offset = 0;
            }

            track.style.transform = `translateX(${offset}px)`;
            requestAnimationFrame(scroll);
        };

        scroll();
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
            if (modalImg) modalImg.src = "";
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
