// utils/js/services/authFetchService.js

export async function fetchWithAutoRefresh(url, options = {}) {
  const accessToken = localStorage.getItem('access_token');
  const refreshToken = localStorage.getItem('refresh_token');

  options.headers = options.headers || {};
  options.headers['Authorization'] = 'Bearer ' + accessToken;
  options.headers['Content-Type'] = 'application/json';

  let response = await fetch(url, options);

  if (response.status === 401) {
    // Attempt to refresh the token
    const refreshResponse = await fetch('/api/token/refresh/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh: refreshToken })
    });

    if (refreshResponse.ok) {
      const refreshData = await refreshResponse.json();
      localStorage.setItem('access_token', refreshData.access);

      // Retry original request with new token
      options.headers['Authorization'] = 'Bearer ' + refreshData.access;
      response = await fetch(url, options);
    } else {
      console.warn('Token refresh failed. Redirecting to login.');
      window.location.href = '/login/';
      return;
    }
  }

  return response;
}
