// static/utils/js/services/modalService.js

export const ModalService = (() => {
  const showError = (message = "An unknown error occurred.") => {
    const modalBody = document.getElementById('errorModalBody');
    modalBody.innerText = message;
    const errorModal = new bootstrap.Modal(document.getElementById('errorModal'));
    errorModal.show();
  };
  const showSuccess = (message = "Operation completed successfully.", onOkCallback = null) => {
    const modalBody = document.getElementById('successModalBody');
    const successModalEl = document.getElementById('successModal');
    const successModal = new bootstrap.Modal(successModalEl);

    modalBody.innerText = message;

    // Get OK button and remove previous click listener if any
    const okBtn = successModalEl.querySelector('.success-ok-btn');
    const newOkBtn = okBtn.cloneNode(true);
    okBtn.parentNode.replaceChild(newOkBtn, okBtn); // Prevent multiple listeners

    newOkBtn.addEventListener('click', () => {
      if (typeof onOkCallback === 'function') {
        onOkCallback();
      }
    });

    successModal.show();
  };
  const showCustom = ({ title, body, onShown }) => {
    const modalEl = document.getElementById("customModal");
    modalEl.querySelector(".modal-title").innerHTML = title;
    modalEl.querySelector(".modal-body").innerHTML = body;

    // Create modal with options: backdrop static, keyboard false
    const modal = new bootstrap.Modal(modalEl, {
      backdrop: 'static',   // Do NOT close on outside click
      keyboard: false       // Do NOT close on ESC key
    });

    modal.show();

    if (typeof onShown === 'function') {
      setTimeout(onShown, 100); // After DOM is rendered
    }
  };


  return {
    showError,
    showSuccess,
    showCustom
  };
})();
