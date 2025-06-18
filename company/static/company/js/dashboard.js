document.addEventListener('DOMContentLoaded',() => {
  const outletInfoContainer = document.getElementById('outlet-info');

  const outletName = localStorage.getItem('username') || 'Admin';

  // Inject Admin Outlet Card
  outletInfoContainer.innerHTML = `
    <h3 class="card-title mb-0">Welcome, ${outletName} </h3>
  `;
});
