// notificationService.js
import { updateChatOnPush } from './chatService.js';

let notificationsEnabled = true;
let activeNotificationToken = null;
let snoozeTimers = {};
let orderStates = AppUtils.loadOrderStates();  // 💾 Load from storage
let notificationModal = null;

function initNotificationModal(modalInstance) {
    notificationModal = modalInstance;
    
    document.getElementById('ok-notification').addEventListener('click', () => {
        if (activeNotificationToken && orderStates[activeNotificationToken]) {
            orderStates[activeNotificationToken].acknowledged = true;
            AppUtils.saveOrderStates(orderStates);  // 💾 Save updated state
        }
        activeNotificationToken = null;
        notificationModal.hide();
    });

    document.getElementById('disable-notifications').addEventListener('click', () => {
        if (activeNotificationToken) {
            const token = activeNotificationToken;
            notificationModal.hide();

            if (orderStates[token] && !orderStates[token].acknowledged) {
                if (snoozeTimers[token]) clearTimeout(snoozeTimers[token]);

                snoozeTimers[token] = setTimeout(() => {
                    if (!orderStates[token].acknowledged) {
                        AppUtils.playNotificationSound();
                        showNotificationModal(orderStates[token].data);
                        AppUtils.notifyOrderReady(orderStates[token].data);
                    }
                }, 3000); // Snooze for 30s
            }
            activeNotificationToken = null;
        }
    });

    // 💤 Re-trigger any snoozed but not acknowledged notifications after reload
    for (const [token, state] of Object.entries(orderStates)) {
        if (!state.acknowledged) {
            snoozeTimers[token] = setTimeout(() => {
                AppUtils.playNotificationSound();
                showNotificationModal(state.data);
                AppUtils.notifyOrderReady(state.data);   
            }, 30000); // Delay after reload to avoid instant spam
        }
    }
}

function showNotificationModal(pushData) {
    if (!notificationsEnabled || !pushData) return;

    const token = pushData.token_no;

    if (!orderStates[token]) {
        orderStates[token] = {
            acknowledged: false,
            data: pushData
        };
    } else {
        orderStates[token].data = pushData;
    }

    if (orderStates[token].acknowledged) return;

    activeNotificationToken = token;
    AppUtils.saveOrderStates(orderStates);  // 💾 Save to storage
    console.log("order states",orderStates)
    const modalHeader = document.querySelector('#notificationModal .modal-body h5');
    modalHeader.innerHTML = `Order <strong>${token}</strong> is <strong>${pushData.status}</strong> at Counter <strong>${pushData.counter_no}</strong>!`;

    AppUtils.playNotificationSound();
    notificationModal.show();

    const { vendor_id, logo_url, vendor_name } = pushData;
    updateChatOnPush(vendor_id, logo_url, vendor_name);
}

// Export methods
export { initNotificationModal, showNotificationModal };
