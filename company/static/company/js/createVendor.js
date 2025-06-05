import createLoaderService from './services/loaderService.js';

document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('create-outlet-form');
    const loader = createLoaderService(form);
  
    form.addEventListener('submit', async function (e) {
      loader.showLoader("Creating outlet...");
      e.preventDefault();
      const locationSelect = document.getElementById('location');
      const selectedOption = locationSelect.options[locationSelect.selectedIndex];
      
      const locationValue = selectedOption.value;  // This is loc.value
      const locationKey = selectedOption.dataset.locationName;  // This is loc.key
      
      const formData = new FormData();
      formData.append('name', document.getElementById('name').value);
      formData.append('location', locationKey);     // Sending readable name
      formData.append('location_id', locationValue); // Sending internal value
      formData.append('place_id', document.getElementById('place_id').value || '');

      // You can replace this with dynamic customer_id if needed
      const customer_id = localStorage.getItem('customerId');
      formData.append('customer_id', customer_id);
  
      // File fields
      const logoInput = document.getElementById('logo');
      if (logoInput.files.length > 0) {
        formData.append('logo', logoInput.files[0]);
      }
  
      const menuFilesInput = document.getElementById('menu_files');
      for (let i = 0; i < menuFilesInput.files.length; i++) {
        formData.append('menu_files', menuFilesInput.files[i]);
      }
  
      // Device Mapping checkboxes
      document.querySelectorAll('input[name="device_mapping"]:checked').forEach(cb => {
        formData.append('device_mapping', cb.value);
      });
  
      // Android TV Mapping checkboxes
      document.querySelectorAll('input[name="tv_mapping"]:checked').forEach(cb => {
        formData.append('tv_mapping', cb.value);
      });
  
      try {
        const response = await fetch('/company/api/create_vendor/', {
          method: 'POST',
          headers: {
            'X-CSRFToken': AppUtils.getCSRFToken()  // ✅ CSRF token only,
          },
          body: formData,
        });
  
        const result = await response.json();
  
        if (result.success) {
          updateLoaderStatus("Registration complete 🎉");
          setTimeout(() => {
              hideLoader();
              form.reset();
              window.location.href = "/login/";
          }, 1500);
          form.reset();
        } else {
          alert('Error: ' + result.error);
        }
      } catch (err) {
        console.error('Fetch error:', err);
        alert('An unexpected error occurred.');
      }
    });
  });
  