import { fetchWithAutoRefresh } from '/static/utils/js/services/authFetchService.js';
import { ConfirmModalService } from './services/confirmModalService.js';

document.addEventListener('DOMContentLoaded',  async () => {
  const outletInfoContainer = document.getElementById('outlet-info');
  const outletName = localStorage.getItem('username') || 'Admin';

  // Inject Admin Outlet Card
  outletInfoContainer.innerHTML = `
    <h3 class="card-title mb-0">Welcome, ${outletName} </h3>
  `;
  const uploadForm = document.getElementById('banner-upload-form');
  const bannerContainer = document.getElementById('banner-tiles-container');
  const modalImage = document.getElementById('bannerModalImage');

  // Load all banners on page load
  fetchBanners();

  // Upload form submission
  uploadForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(uploadForm);
    console.log(formData)
    const response = await fetchWithAutoRefresh('/company/api/banner_upload/', {
      method: 'POST',
      body: formData
    });
    if (response.ok) {
      uploadForm.reset();
      fetchBanners();
    } else {
      alert("Banner upload failed.");
    }
  });

  // Fetch and render banners
  async function fetchBanners() {
    // const response = await fetch('/company/api/banner_list/');
    const response = await fetchWithAutoRefresh('/company/api/banner_list/', {
      method: 'GET'
    });
    const banners = await response.json();
    console.log(banners);

    bannerContainer.innerHTML = '';
    banners.banners.forEach(banner => {
      const tile = document.createElement('div');
      tile.className = 'banner-tile';

      tile.innerHTML = `
        <img src="${banner.image_url}" alt="Banner">
        <div class="banner-actions">
          <button onclick="viewBanner('${banner.image_url}')" title="View">
            <i class="fas fa-eye"></i>
          </button>
          <button onclick="deleteBanner(${banner.id})" title="Delete">
            <i class="fas fa-trash-alt"></i>
          </button>
        </div>
      `;
      bannerContainer.appendChild(tile);
    });
  }

  window.viewBanner = (url) => {
    modalImage.src = url;
    $('#bannerModal').modal('show');
  };


  window.deleteBanner = async (id) => {
    const confirmed = await ConfirmModalService.show("Do you want to discard this banner?");
    if (!confirmed) return;

    try {
      const response = await fetchWithAutoRefresh(`/company/api/banner_delete/?banner_id=${id}`, {
        method: 'DELETE'
      });

      if (response.ok) {
        fetchBanners();
      }
    } catch (err) {
      console.error("Banner delete error:", err);
    }
  };

  // window.deleteBanner = async (id) => {
  //   // const confirmed = await loader.awaitConfirmation("Do you want to discard this banner?", false); // ⬅️ no overlay
  //   // if (!confirmed) return;

  //   try {
  //     const response = await fetchWithAutoRefresh(`/company/api/banner_delete/?banner_id=${id}`, {
  //       method: 'DELETE'
  //     });

  //     if (response.ok) {
  //       fetchBanners();
  //     }
  //   } catch (err) {
  //     console.error("Banner delete error:", err);
  //   }
  // };
});
