// document.addEventListener('DOMContentLoaded',() => {
//     setupOutletGreeting();
// });
// // =================== INIT HELPERS ===================
// function setupOutletGreeting() {
//     const welcomeInfoContainer = document.getElementById('welcome-info');
//     const outletName = localStorage.getItem('username') || 'Admin';
//     welcomeInfoContainer.innerHTML = `<h1 class="text-golden">Welcome, ${outletName}</h1>`;
// }
document.addEventListener('DOMContentLoaded', () => {
  const currentPath = window.location.pathname;

  // Show welcome only on dashboard
  if (currentPath.includes('/dashboard') || currentPath.endsWith('/company/')) {
    setupOutletGreeting();
  }
});

function setupOutletGreeting() {
  const welcomeInfoContainer = document.getElementById('welcome-info');
  const outletName = localStorage.getItem('username') || 'Admin';
  welcomeInfoContainer.innerHTML = `<span class="text-golden fw-bold">Welcome, ${outletName}</span>`;
}
