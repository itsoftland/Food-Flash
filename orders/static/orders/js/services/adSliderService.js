// static/js/services/adSliderService.js
let slideshowInterval;
let currentSlideIndex = 0;

export const AdSliderService = {
    fetchAds: async function (vendorIds) {
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
    },

    interleaveAds: function (vendorAdsArray) {
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
    },
    renderAds: function (ads, containerId = "ad-slider") {
        const adContainer = document.getElementById(containerId);
        if (!adContainer) return;
    
        adContainer.innerHTML = "";
    
        // To create infinite loop effect, clone the ads
        const allAds = ads.concat(ads);  // Doubled list
    
        allAds.forEach(adUrl => {
            const img = document.createElement("img");
            img.src = adUrl;
            img.alt = "Advertisement";
            img.classList.add("ad-slide");
    
            img.addEventListener("click", () => {
                AdSliderService.openAdModal(adUrl);
            });
    
            adContainer.appendChild(img);
        });
    },

    openAdModal: function (src) {
        const adModal = document.getElementById("ad-modal");
        const modalImg = document.getElementById("ad-modal-img");

        if (adModal && modalImg) {
            adModal.style.display = "block";
            modalImg.src = src;
        }
    },

    initModalListeners: function () {
        const modalClose = document.querySelector(".ad-modal-close");
        const adModal = document.getElementById("ad-modal");

        if (modalClose && adModal) {
            modalClose.onclick = () => {
                adModal.style.display = "none";
            };

            window.onclick = event => {
                if (event.target === adModal) {
                    adModal.style.display = "none";
                }
            };
        }
    },
   
    
};
