// static/js/apiEndpoints.js
export const API_ENDPOINTS = {
  CONFIG: '/company/api/config/',
  DASHBOARD_METRICS: '/company/api/dashboard_metrics/',
  GET_VENDORS: '/company/api/get_vendors/',
  GET_VENDOR_DETAILS: '/company/api/get_vendor_details/',
  GET_OUTLET_CREATION_DATA: '/company/api/get_outlet_creation_data/',
  UNMAP_PROFILE: (vendorId, profileId) => `/company/api/unmap_profile/${vendorId}/${profileId}/`,
  MAP_PROFILE: (vendorId, profileId) => `/company/api/map_profile/${vendorId}/${profileId}/`,
  GET_OUTLETS: '/company/api/get_outlets/',
 
 
 
  
  // Add more endpoints here
};
