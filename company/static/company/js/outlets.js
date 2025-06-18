import { fetchWithAutoRefresh } from '/static/utils/js/services/authFetchService.js';

document.addEventListener('DOMContentLoaded',  async () => {

  const outletInfoContainer = document.getElementById('outlet-info');
  const vendorListContainer = document.getElementById('vendor-list');

  const outletName = localStorage.getItem('username') || 'Admin';

   // 1️⃣ Inject Admin Outlet Card
  outletInfoContainer.innerHTML = `
    <h3 class="card-title mb-0">Welcome, ${outletName} </h3>
  `;

  // 2️⃣ Fetch Vendors
  try {
    const response = await fetchWithAutoRefresh('/company/api/get_vendors/', {
      method: 'GET'
    });

    if (!response.ok) {
      throw new Error("Failed to load vendors");
    }

    const data = await response.json();
    const vendors = data.vendors || [];
    console.log(vendors)

    if (vendors.length === 0) {
      vendorListContainer.innerHTML = `
        <div class="col-12">
          <div class="alert alert-warning">No vendors have been added yet.</div>
        </div>`;
      return;
    }

    // 3️⃣ Render Each Vendor Card
    vendors.forEach(vendor => {
      const col = document.createElement('div');
      col.className = 'col-lg-3 col-md-4 col-sm-6 col-12 mb-4';
      col.innerHTML = `
        <div class="vendor-tile">
          <div class="inner">
            <h4>${vendor.name}</h4>
            <p>Location: ${vendor.location || 'N/A'}</p>
          </div>
          <div class="icon">
            <i class="fas fa-store"></i>
          </div>
          <a data-vendor-id="${vendor.vendor_id}" class="small-box-footer">
            View Details <i class="fas fa-arrow-circle-right"></i>
          </a>
        </div>
      `;
      vendorListContainer.appendChild(col);
    });

  } catch (error) {
    console.error('Error loading vendor data:', error);
    vendorListContainer.innerHTML = `
      <div class="col-12">
        <div class="alert alert-warning">Something went wrong while loading vendor data.</div>
      </div>`;
  }
  vendorListContainer.addEventListener('click', function (e) {
    const link = e.target.closest('a[data-vendor-id]');
    if (link) {
      e.preventDefault();
      const vendorId = link.dataset.vendorId;
      window.location.href = `/company/update_outlet/?vendor_id=${vendorId}`;
    }
  });

  
});
