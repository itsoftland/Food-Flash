import { fetchWithAutoRefresh } from '/static/utils/js/services/authFetchService.js';
import { ImageLibraryService } from './services/imageLibraryService.js';
import { ConfirmModalService } from './services/confirmModalService.js';

document.addEventListener('DOMContentLoaded', async () => {
  setupOutletGreeting();
  await fetchAdProfiles();
  ImageLibraryService.init();
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

// function renderAdProfiles(profiles) {
//   const tbody = document.getElementById("ad-profile-table-body");
//   tbody.innerHTML = "";

//   profiles.forEach(profile => {
//     const row = document.createElement("tr");
//     const days = (profile.days_active || []).map(day =>
//       `<span class="badge badge-secondary mr-1">${day}</span>`
//     ).join("");

//     const dateStart = profile.date_start || "";
//     const dateEnd = profile.date_end || "";

//     row.innerHTML = `
//       <td><strong>${profile.name}</strong></td>
//       <td>${dateStart && dateEnd ? `${dateStart} → ${dateEnd}` : ""}</td>
//       <td>${days}</td>
//       <td class="text-center"><span class="badge-priority">${profile.priority}</span></td>
//       <td>
//         <button class="icon-btn icon-view" title="View Images" data-images='${JSON.stringify(profile.images)}'>
//           <i class="fas fa-image"></i>
//         </button>

//         <button class="icon-btn icon-edit" title="Edit Profile" data-id="${profile.id}">
//           <i class="fas fa-edit"></i>
//         </button>

//         <button class="icon-btn icon-delete" title="Delete Profile" data-id="${profile.id}">
//           <i class="fas fa-trash"></i>
//         </button>
//       </td>

//     `;

//     tbody.appendChild(row);
//   });

//   attachActionListeners();
// }
function renderAdProfiles(profiles) {
  const tbody = document.getElementById("ad-profile-table-body");
  tbody.innerHTML = "";

  profiles.forEach(profile => {
    const row = document.createElement("tr");

    // === Days Active (Compact with Tooltip) ===
    const fullDays = profile.days_active || [];
    const dayMap = {
      Monday: 'Mon', Tuesday: 'Tue', Wednesday: 'Wed', Thursday: 'Thu',
      Friday: 'Fri', Saturday: 'Sat', Sunday: 'Sun'
    };
    const short = fullDays.map(d => dayMap[d] || d);
    const titleText = fullDays.join(', ');
    const days = fullDays.length > 0
      ? `<span class="badge-days-active" data-toggle="tooltip" title="${titleText}">${short.join(', ')}</span>`
      : `<span class="text-muted"></span>`;
    console.log(days)

    const dateStart = profile.date_start || "";
    const dateEnd = profile.date_end || "";

    row.innerHTML = `
      <td><strong>${profile.name}</strong></td>
      <td>${dateStart && dateEnd ? `${dateStart} → ${dateEnd}` : ""}</td>
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
