// notificationService.js
let notificationsEnabled = true;
let modalHasBeenAcknowledged = false;
let notificationModal;

function initNotificationModal(modalInstance) {
    notificationModal = modalInstance;

    document.getElementById('ok-notification').addEventListener('click', () => {
        modalHasBeenAcknowledged = true;
        notificationModal.hide();
    });

    document.getElementById('disable-notifications').addEventListener('click', () => {
        notificationModal.hide();
        if (!modalHasBeenAcknowledged) {
            setTimeout(() => {
                if (!modalHasBeenAcknowledged) {
                    showNotificationModal(lastPushData); // retry with previous data
                }
            }, 30000);
        }
    });
}

let lastPushData = null;

function showNotificationModal(pushData) {
    if (!modalHasBeenAcknowledged && notificationsEnabled && pushData) {
        lastPushData = pushData;

        const modalHeader = document.querySelector('#notificationModal .modal-body h5');
        modalHeader.innerHTML = `Order <strong>${pushData.token_no}</strong> is <strong>${pushData.status}</strong> at Counter <strong>${pushData.counter_no}</strong>!`;

        notificationModal.show();
    }
}

// Expose methods
export { initNotificationModal, showNotificationModal };
