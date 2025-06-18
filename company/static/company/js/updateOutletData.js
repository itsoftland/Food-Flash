import { fetchWithAutoRefresh } from '/static/utils/js/services/authFetchService.js';
import { MenuFileManagerService } from './services/menuService.js';

document.addEventListener('DOMContentLoaded', async () => {
  const urlParams = new URLSearchParams(window.location.search);
  const vendorId = urlParams.get('vendor_id');

  const locationSelect = document.getElementById('location');
  const tvSelect = document.getElementById('tv-select');
  const deviceSelect = document.getElementById('device-select');
  const name = document.getElementById('name');
  const alias = document.getElementById('alias_name');
  const placeId = document.getElementById('place_id');

  let vendorData = {};
  let unmappedVendorData = {};
  let vendorDetails = {};

  try {
    // 1️⃣ Fetch vendor details (current data)
    const vendorRes = await fetchWithAutoRefresh(`/company/api/get_vendor_details?vendor_id=${vendorId}`);
    if (!vendorRes.ok) throw new Error("Vendor details fetch failed");
    vendorDetails = await vendorRes.json();
    vendorData = vendorDetails.vendor_data;
    unmappedVendorData = vendorDetails.unmapped_data;

    } catch (error) {
    console.error("Fetch error:", error);
    return;
  }

    // 3️⃣ Prefill text inputs
  name.value = vendorData.name || '';
  alias.value = vendorData.alias_name || '';
  placeId.value = vendorData.place_id || '';
  console.log(vendorData);

  const { unmapped_locations, unmapped_android_tvs, unmapped_keypad_devices } = unmappedVendorData;
  const currentLocation = vendorData.location_id;
  if (locationSelect) {
    locationSelect.innerHTML = '';
    unmapped_locations.forEach(loc => {
      const option = document.createElement('option');
      option.value = loc.value;
      option.textContent = loc.key;
      if (loc.value === currentLocation) {
        option.selected = true;
      }
      locationSelect.appendChild(option);
    });
  }

  //Populate & Preselect Android TVs
  const selectedTVs = (vendorData.android_tvs || []).map(tv => tv.mac_address);
  if (tvSelect) {
    tvSelect.innerHTML = '';
    
    unmapped_android_tvs.forEach(tv => {
      const option = document.createElement('option');
      option.value = tv.mac_address;
      option.textContent = tv.mac_address;
      tvSelect.appendChild(option);
    });
    const android_tvsChoices = new Choices(tvSelect, {
      removeItemButton: true,
      classNames: {
        containerInner: 'choices-inner-foodflash',
        item: 'choices-item-foodflash',
      },
      placeholderValue: 'Select TVs',
      searchEnabled: true
    });
    // Set selected values after initialization
    android_tvsChoices.setChoiceByValue(selectedTVs);
  }
  const selectedKeypadDevices = (vendorData.keypad_devices || []).map(device => device.serial_no);
  if (deviceSelect) {
    deviceSelect.innerHTML = '';

    unmapped_keypad_devices.forEach(keypad => {
      const option = document.createElement('option');
      option.value = keypad.serial_no;
      option.textContent = keypad.serial_no;
      deviceSelect.appendChild(option);
    });

    const keypadDeviceChoices = new Choices(deviceSelect, {
      removeItemButton: true,
      classNames: {
        containerInner: 'choices-inner-foodflash',
        item: 'choices-item-foodflash',
      },
      placeholderValue: 'Select TVs',
      searchEnabled: true
    });

    // Set selected values after initialization
    keypadDeviceChoices.setChoiceByValue(selectedKeypadDevices);
  }

  if (vendorData.logo_url) {
    const img = document.querySelector('#logo + p img');
    img.src = vendorData.logo_url;
  }
  if (vendorData.menu_files && Array.isArray(vendorData.menu_files)) {
    MenuFileManagerService.init(vendorData.menu_files)
  }
});

