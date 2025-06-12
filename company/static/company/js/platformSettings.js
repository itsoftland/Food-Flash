// import { fetchWithAutoRefresh } from '/static/utils/js/services/authFetchService.js';

document.addEventListener('DOMContentLoaded',  async () => {

  const outletInfoContainer = document.getElementById('outlet-info');
  const outletName = localStorage.getItem('username') || 'Admin';

   // 1️⃣ Inject Admin Outlet Card
  outletInfoContainer.innerHTML = `
    <h3 class="card-title mb-0">Welcome, ${outletName} </h3>
  `;
});
