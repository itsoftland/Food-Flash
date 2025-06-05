// loaderService.js

export default function createLoaderService(form) {
    const loaderOverlay = document.getElementById("loaderOverlay");
    const loaderStatus = document.getElementById("loaderStatus");
    const submitButton = form.querySelector('button[type="submit"]');
  
    function showLoader(message = "Submitting data...") {
      if (loaderOverlay) loaderOverlay.style.display = "flex";
      if (loaderStatus) loaderStatus.textContent = message;
      if (submitButton) submitButton.disabled = true;
    }
  
    function updateLoaderStatus(message) {
      if (loaderStatus) loaderStatus.textContent = message;
    }
  
    function hideLoader() {
      if (loaderOverlay) loaderOverlay.style.display = "none";
      if (submitButton) submitButton.disabled = false;
    }
  
    return {
      showLoader,
      updateLoaderStatus,
      hideLoader,
    };
  }
  