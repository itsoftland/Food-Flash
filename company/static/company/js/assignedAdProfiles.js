import { fetchWithAutoRefresh } from '/static/utils/js/services/authFetchService.js';

document.addEventListener('DOMContentLoaded', async () => {
  setupOutletGreeting();
  await loadAssignedProfiles();
});

// =================== INIT HELPERS ===================

function setupOutletGreeting() {
  const outletInfoContainer = document.getElementById('outlet-info');
  const outletName = localStorage.getItem('username') || 'Admin';
  outletInfoContainer.innerHTML = `<h3 class="card-title mb-0">Welcome, ${outletName}</h3>`;
}
// ========== Load Assigned Profiles ==========
// async function loadAssignedProfiles() {
//   const tableBody = document.getElementById('ad-profile-table-body');
//   tableBody.innerHTML = `<tr><td colspan="3" class="text-center">Loading...</td></tr>`;

//   try {
//     const response = await fetchWithAutoRefresh('/company/api/assigned_profiles/');
//     const data = await response.json();

//     if (response.ok) {
//       if (data.profiles.length === 0) {
//         tableBody.innerHTML = `<tr><td colspan="3" class="text-center">No assigned profiles found.</td></tr>`;
//         return;
//       }

//       tableBody.innerHTML = '';

//       data.profiles.forEach((outlet) => {
//         const profileNames = outlet.assigned_profiles.map(p => p.name).join(', ');
//         const row = document.createElement('tr');

//         row.innerHTML = `
//           <td>${outlet.outlet_name}</td>
//           <td>${profileNames || '<span class="text-muted">No Profiles Assigned</span>'}</td>
//           <td>
//             <!-- Future: Add action buttons -->
//             <button class="btn btn-sm btn-outline-primary disabled">View</button>
//           </td>
//         `;

//         tableBody.appendChild(row);
//       });
//     } else {
//       showError('Failed to load assigned profiles.');
//       console.error(data);
//     }
//   } catch (error) {
//     console.error('Error fetching profiles:', error);
//     tableBody.innerHTML = `<tr><td colspan="3" class="text-danger text-center">Error loading data.</td></tr>`;
//   }
// }

// // ========== Optional: Global Error Modal ==========
// function showError(message) {
//   alert(message); // Replace with a modal if needed
// }

async function loadAssignedProfiles() {
    const accordion = document.getElementById('outletAccordion');
    accordion.innerHTML = `<p class="text-muted text-center">Loading...</p>`;

    try {

        const response = await fetchWithAutoRefresh('/company/api/assigned_profiles/');
        const data = await response.json();

        if (!response.ok) throw new Error();
        const outlets = data.profiles;

        if (!outlets.length) {
        console.log("success");
        accordion.innerHTML = `<p class="text-muted text-center">No profiles assigned yet.</p>`;
        return;
        }

        accordion.innerHTML = '';
        outlets.forEach(outlet => {
            const assignedChips = outlet.assigned_profiles.map(profile => `
            <span class="profile-chip" onclick="window.location.href='/company/ad_profiles/'">
                ${profile.name}
                <i class="fas fa-times remove-icon" onclick="event.stopPropagation(); removeProfile(${outlet.outlet_id}, ${profile.id})"></i>
            </span>
            `).join('');
            accordion.innerHTML += `
            <div class="card mb-2 border-0 shadow-sm">
                <div class="card-header bg-light-gray d-flex justify-content-between align-items-center"
                    data-bs-toggle="collapse"
                    data-bs-target="#collapse${outlet.outlet_id}"
                    style="cursor: pointer;">
                
                    <!-- Outlet Name (left-aligned) -->
                    <div class="d-flex align-items-center gap-2">
                        <i class="fas fa-store text-muted"></i>
                        <span class="fw-semibold text-dark">${outlet.outlet_name}</span>
                    </div>

                    <!-- Profile Count + Dropdown (right-aligned) -->
                    <div class="d-flex align-items-center gap-2 ms-auto" style="margin-left: auto;">
                        <span class="badge bg-secondary bg-opacity-25 text-dark">
                            ${outlet.assigned_count} ${outlet.assigned_count === 1 ? 'Profile' : 'Profiles'}
                        </span>
                        <i class="fas fa-chevron-down text-muted dropdown-chevron chevron-${outlet.outlet_id}"></i>
                    </div>
                </div>

                <div id="collapse${outlet.outlet_id}" class="collapse" data-bs-parent="#outletAccordion">
                    <div class="card-body">
                        <label class="form-label fw-bold text-secondary">Assigned Profiles:</label>
                        <div class="profile-chip-container mb-3">
                            ${assignedChips || '<span class="text-muted">No Profiles Assigned</span>'}
                        </div>

                        <button class="btn btn-sm btn-outline-primary" onclick="openAssignModal(${outlet.outlet_id})">
                            + Add Profile
                        </button>
                    </div>
                </div>
            </div>
        `;

        },
        setTimeout(() => {
        document.querySelectorAll('[id^="collapse"]').forEach(collapseEl => {
            const outletId = collapseEl.id.replace('collapse', '');
            const chevron = document.querySelector(`.chevron-${outletId}`);

            collapseEl.addEventListener('show.bs.collapse', () => {
            chevron?.classList.add('rotate');
            });

            collapseEl.addEventListener('hide.bs.collapse', () => {
            chevron?.classList.remove('rotate');
            });
        });
        }, 50))
        } catch (err) {
        accordion.innerHTML = `<p class="text-danger text-center">Error loading data.</p>`;
        }
    }

  window.removeProfile = async (outletId, profileId) => {
    if (!confirm('Remove this profile from the outlet?')) return;
    try {
      const res = await fetchWithAutoRefresh(`/company/api/unassign_profile/`, {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ outlet_id: outletId, profile_id: profileId })
      });
      if (res.ok) loadAssignedProfiles();
    } catch (err) {
      alert('Failed to remove profile');
    }
  };

  window.openAssignModal = (outletId) => {
    alert('Modal to assign profiles to outlet ' + outletId + ' will be implemented here.');
    // Optional: Build modal with profile list fetched from another API
  };