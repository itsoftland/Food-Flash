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

  // const showSuccess = (message = "Operation completed successfully.") => {
  //   const modalBody = document.getElementById('successModalBody');
  //   modalBody.innerText = message;
  //   const successModal = new bootstrap.Modal(document.getElementById('successModal'));
  //   successModal.show();
  // };

  return {
    showError,
    showSuccess,
  };
})();
