// notificationService.js
import { updateChatOnPush } from './chatService.js';

let notificationsEnabled = true;
let activeNotificationToken = null;
let snoozeTimers = {};
let orderStates = AppUtils.loadOrderStates();  // 💾 Load from storage
let notificationModal = null;
let clearTimers = {};  // Store timers to clear token after 1 hour

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
                }, 30000); // Snooze for 30s
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

function showNotificationModal(pushData, source) {
    if (!notificationsEnabled || !pushData) return;

    const token = pushData.token_no;

    // Check if it's a new push notification (not a user action)
    if (source !== 'usercheck') { // Only show modal if it's a push notification
        orderStates[token] = {
            acknowledged: false,
            data: pushData,
            receivedAt: new Date().toISOString()
        };

        // Save state and trigger modal only on true new push
        activeNotificationToken = token;
        AppUtils.saveOrderStates(orderStates);  // 💾 Save to storage

        // Display modal content
        const modalHeader = document.querySelector('#notificationModal .modal-body h5');
        modalHeader.innerHTML = `Order <strong>${pushData.token_no}</strong> is <strong>${pushData.status}</strong> at Counter <strong>${pushData.counter_no}</strong>!`;
        notificationModal.show();

        // Play notification sound
        AppUtils.playNotificationSound();

        // Update chat UI with new push info
        const { vendor_id, logo_url, vendor_name } = pushData;
        updateChatOnPush(vendor_id, logo_url, vendor_name);

        // Set timeout to auto-clear order after 1 hour
        if (clearTimers[token]) clearTimeout(clearTimers[token]);
        clearTimers[token] = setTimeout(() => {
            delete orderStates[token];
            AppUtils.saveOrderStates(orderStates);  // 💾 Save updated state
        }, 3600000); // 1 hour timeout
    }
}


// Export methods
export { initNotificationModal, showNotificationModal };


