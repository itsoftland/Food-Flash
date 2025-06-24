import { fetchWithAutoRefresh } from '/static/utils/js/services/authFetchService.js';
import { ImageLibraryService } from './services/imageLibraryService.js';
import { ConfirmModalService } from './services/confirmModalService.js';

document.addEventListener('DOMContentLoaded', async () => {
  setupOutletGreeting();
  await fetchAdProfiles();
  ImageLibraryService.init();
  setupFormSubmitHandler();
  await initAssignProfileForm();
  $(function () {
  $('[data-toggle="tooltip"]').tooltip();
  });
});

// =================== INIT HELPERS ===================

function setupOutletGreeting() {
  const outletInfoContainer = document.getElementById('outlet-info');
  const outletName = localStorage.getItem('username') || 'Admin';
  outletInfoContainer.innerHTML = `<h3 class="card-title mb-0">Welcome, ${outletName}</h3>`;
}

// =================== FETCH PROFILES ===================

async function fetchAdProfiles() {
  try {
    const res = await fetchWithAutoRefresh('/company/api/get_ad_profiles/');
    const data = await res.json();
    const profiles = data.profiles || data.banners || data.ad_profiles || [];
    renderAdProfiles(profiles);
  } catch (err) {
    console.error('Error fetching advertisement profiles:', err);
  }
}

function renderAdProfiles(profiles) {
  const tbody = document.getElementById("ad-profile-table-body");
  tbody.innerHTML = "";

  profiles.forEach(profile => {
    const row = document.createElement("tr");
    const days = (profile.days_active || []).map(day =>
      `<span class="badge badge-secondary mr-1">${day}</span>`
    ).join("");

    row.innerHTML = `
      <td><strong>${profile.name}</strong></td>
      <td>${profile.date_start} → ${profile.date_end}</td>
      <td>${days}</td>
      <td class="text-center"><span class="badge-priority">${profile.priority}</span></td>
      <td>
        <button class="icon-btn icon-view" title="View Images" data-images='${JSON.stringify(profile.images)}'>
          <i class="fas fa-image"></i>
        </button>

        <button class="icon-btn icon-edit" title="Edit Profile" data-id="${profile.id}">
          <i class="fas fa-edit"></i>
        </button>

        <button class="icon-btn icon-delete" title="Delete Profile" data-id="${profile.id}">
          <i class="fas fa-trash"></i>
        </button>
      </td>

    `;

    tbody.appendChild(row);
  });

  attachActionListeners();
}

// =================== IMAGE MODAL ===================

function attachActionListeners() {
  document.querySelectorAll('.icon-view').forEach(btn => {
    btn.addEventListener('click', () => {
      const images = JSON.parse(btn.dataset.images || '[]');
      const container = document.getElementById('modal-image-container');
      console.log(container)
      container.innerHTML = '';

      images.forEach(img => {
        const imgBox = document.createElement('div');
        imgBox.className = 'm-2';
        imgBox.innerHTML = `<img src="${img.image_url}" class="preview-image">`;
        container.appendChild(imgBox);
      });

      $('#imageModal').modal('show');
    });
  });

  document.querySelectorAll('.icon-edit').forEach(btn => {
    btn.addEventListener('click', () => {
      const profileId = btn.dataset.id;
      console.log('Edit profile:', profileId);
      // TODO: Open modal and load data for editing
    });
  });

  document.querySelectorAll('.icon-delete').forEach(btn => {
    btn.addEventListener('click', async () => {
      const profileId = btn.dataset.id;
      console.log('Delete profile:', profileId);
      const confirmed = await ConfirmModalService.show("Do you want to discard this Ad Profile?");
      if (!confirmed) return;
      try {
      const res = await fetchWithAutoRefresh(`/company/api/delete_ad_profile/?ad_profile_id=${profileId}`, {
        method: 'DELETE',
      });
      await fetchAdProfiles();
      } 
      catch (err) {
        console.error('Error submitting form:', err);
        alert('Unexpected error while creating profile.');
      }
    });
  });
}

// =================== CREATE PROFILE ===================

document.getElementById('select-all-days').addEventListener('change', function () {
  const isChecked = this.checked;
  document.querySelectorAll('.day-checkbox').forEach(cb => {
    cb.checked = isChecked;
  });
});

function showErrorModal(message) {
  const modalBody = document.getElementById('errorModalBody');
  modalBody.innerText = message || "An unknown error occurred.";
  const errorModal = new bootstrap.Modal(document.getElementById('errorModal'));
  errorModal.show();
}


function setupFormSubmitHandler() {
  document.getElementById('create-profile-form').addEventListener('submit', async function (e) {
    e.preventDefault();
    const fieldLabelMap = {
      name: "Profile Name",
      date_start: "Start Date",
      date_end: "End Date",
      days_active: "Days Active",
      priority: "Priority",
      image_ids: "Token Number",
    };
    const payload = {
      name: document.getElementById('profile-name').value,
      date_start: document.getElementById('date-start').value || null,
      date_end: document.getElementById('date-end').value || null,
      days_active: Array.from(document.querySelectorAll('.day-checkbox:checked')).map(cb => cb.value),
      priority: parseInt(document.getElementById('priority').value),
      image_ids: ImageLibraryService.getSelectedImageIds() // Use the modal selection
    };

    console.log('Submitting:', payload); 

    try {
    const res = await fetchWithAutoRefresh('/company/api/create_ad_profile/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const result = await res.json();

    if (res.ok) {
      await fetchAdProfiles();
      this.reset();
      document.getElementById('selected-images-preview').innerHTML = '';
      document.querySelector('#profileTab a[href="#view-profiles"]').click();
    } else {
      // Extract and show error message
      let msg = "Something went wrong.";

      if (result?.details) {
        const errorDetails = result.details;

        if (Array.isArray(errorDetails.non_field_errors)) {
          msg = errorDetails.non_field_errors.join('\n');
        } else {
          msg = Object.entries(errorDetails).map(
            ([key, value]) => `${key}: ${Array.isArray(value) ? value.join(', ') : value}`
          ).join('\n');
        }

      } else if (result?.error) {
        msg = result.error;
      } else if (result?.message) {
        msg = result.message;
      }

      showErrorModal(msg);
    }
  } catch (err) {
    console.error('Error submitting form:', err);
    showErrorModal("Unexpected error while creating profile.");
  }
  });
}
document.getElementById('open-image-library-btn')?.addEventListener('click', () => {
  ImageLibraryService.open();
});

async function initAssignProfileForm() {
  try {
    // Fetch Ad Profiles
    const profilesRes = await fetchWithAutoRefresh('/company/api/get_ad_profiles/');
    const profilesData = await profilesRes.json();
    const profiles = profilesData.profiles || [];
    

    const profileSelect = document.getElementById('ad-profile-select');
    profileSelect.innerHTML = profiles.map(p => `<option value="${p.id}">${p.name}</option>`).join('');

    // Fetch Outlets
    const outletsRes = await fetchWithAutoRefresh('/company/api/get_vendors/');
    const outletsData = await outletsRes.json();
    const outlets = outletsData.vendors || [];
    console.log(outlets)
    const outletSelect = document.getElementById('outlet-select');
    outletSelect.innerHTML = outlets.map(o => `<option value="${o.vendor_id}">${o.name}</option>`).join('');

    // Initialize Choices
    const profileChoices = new Choices(profileSelect, {
      removeItemButton: true,
      placeholderValue: 'Select profiles',
      classNames: {
        containerInner: 'choices-inner-foodflash',
        item: 'choices-item-foodflash',
      },

    });

    const outletChoices = new Choices(outletSelect, {
      removeItemButton: true,
      placeholderValue: 'Select outlets',
      classNames: {
        containerInner: 'choices-inner-foodflash',
        item: 'choices-item-foodflash',
      },
      searchEnabled: true,
    });

    // Submit Handler
    document.getElementById('assign-profile-form')?.addEventListener('submit', async function (e) {
      e.preventDefault();

      const profileIds = profileChoices.getValue(true); // Array
      const outletIds = outletChoices.getValue(true);   // Array
      console.log(profileIds,outletIds)

      if (!profileIds.length || !outletIds.length) {
        showErrorModal("Please select at least one profile and one outlet.");
        return;
      }

      try {
        const res = await fetchWithAutoRefresh('/company/api/assign_ad_profile/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ 
            profile_ids: profileIds, 
            vendor_ids: outletIds 
          })
        });

        const result = await res.json();

        if (res.ok) {
          
          profileChoices.clearStore();
          outletChoices.clearStore();
        } else {
          showErrorModal(result.message || "Assignment failed.");
        }
      } catch (err) {
        console.error('Assignment error:', err);
        showErrorModal("Unexpected error occurred during assignment.");
      }
    });

  } catch (err) {
    console.error('Error loading assign form data:', err);
    showErrorModal("Failed to load data for assigning profiles.");
  }
}
