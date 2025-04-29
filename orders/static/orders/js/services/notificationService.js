// notificationService.js
let notificationsEnabled = true;
let activeNotificationToken = null;
let snoozeTimers = {};
let orderStates = {};  // token_no: { acknowledged: boolean, data: pushData }
let notificationModal;

function initNotificationModal(modalInstance) {
    notificationModal = modalInstance;

    document.getElementById('ok-notification').addEventListener('click', () => {
        if (activeNotificationToken) {
            orderStates[activeNotificationToken].acknowledged = true;
            activeNotificationToken = null;
        }
        notificationModal.hide();
    });

    document.getElementById('disable-notifications').addEventListener('click', () => {
        if (activeNotificationToken) {
            const token = activeNotificationToken;
            notificationModal.hide();

            if (!orderStates[token].acknowledged) {
                if (snoozeTimers[token]) {
                    clearTimeout(snoozeTimers[token]);
                }
                snoozeTimers[token] = setTimeout(() => {
                    if (!orderStates[token].acknowledged) {
                        showNotificationModal(orderStates[token].data);
                    }
                }, 30000);  // 30 sec snooze
            }

            activeNotificationToken = null;
        }
    });
}

function showNotificationModal(pushData) {
    if (!notificationsEnabled || !pushData) return;

    const token = pushData.token_no;

    // Initialize order state if not already present
    if (!orderStates[token]) {
        orderStates[token] = {
            acknowledged: false,
            data: pushData
        };
    } else {
        // Update latest data
        orderStates[token].data = pushData;
    }

    // Don't show modal if it's already acknowledged
    if (orderStates[token].acknowledged) return;

    activeNotificationToken = token;
    console.log("notification service",pushData)
    const modalHeader = document.querySelector('#notificationModal .modal-body h5');
    modalHeader.innerHTML = `Order <strong>${token}</strong> is <strong>${pushData.status}</strong> at Counter <strong>${pushData.counter_no}</strong>!`;

    AppUtils.playNotificationSound();
    notificationModal.show();
}

// Expose methods
export { initNotificationModal, showNotificationModal };
