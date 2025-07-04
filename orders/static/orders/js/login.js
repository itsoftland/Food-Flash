
document.addEventListener('DOMContentLoaded', function () {
    const loginForm = document.getElementById('loginForm');

    loginForm.addEventListener('submit', async function (e) {
        e.preventDefault();

        const username = document.getElementById('username').value.trim();
        const password = document.getElementById('password').value.trim();

        const payload = { username, password };

        try {
            const response = await fetch('/api/login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload)
            });

            const data = await response.json();

            if (!response.ok) {
                alert(data.error || 'Login failed');
                return;
            }

            // Store data in localStorage
            localStorage.setItem('access_token', data.access);
            localStorage.setItem('refresh_token', data.refresh);
            AppUtils.setCustomerName(data.user.username);
            localStorage.setItem('role', data.user.role);
            AppUtils.setCustomerId(data.user.customer_id || '');

            // Redirect based on role
            const role = data.user.role;
            if (role === 'Company Admin') {
                window.location.href = '/companyadmin/dashboard/';
            } else if (role === 'Company') {
                window.location.href = '/company/dashboard/';
            } else if (role === 'Outlet') {
                window.location.href = '/vendor/dashboard/';
            } else {
                alert('Unknown user role');
            }
        } catch (err) {
            console.error('Login error:', err);
            alert('An unexpected error occurred.');
        }
    });
});
