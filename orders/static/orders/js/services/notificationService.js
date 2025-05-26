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
    console.log("notified");
    if (!notificationsEnabled || !pushData) return;

    const token = pushData.token_no;

    // If order state for token does not exist, initialize it
    if (!orderStates[token]) {
        orderStates[token] = {
            acknowledged: false,
            data: pushData,
            receivedAt: new Date().toISOString()
        };
    }

    const isPush = source !== 'usercheck';

    // If it's user-initiated and already acknowledged, skip
    if (!isPush && orderStates[token].acknowledged) {
        console.log(`Token ${token} already acknowledged. Skipping user modal.`);
        return;
    }

    // If it's a push, reset acknowledged to false so modal shows again
    if (isPush) {
        orderStates[token].acknowledged = false;
        orderStates[token].data = pushData;
        orderStates[token].receivedAt = new Date().toISOString();
    }

    // Show modal
    activeNotificationToken = token;
    AppUtils.saveOrderStates(orderStates);

    const modalHeader = document.querySelector('#notificationModal .modal-body h5');
    modalHeader.innerHTML = `Order <strong>${pushData.token_no}</strong> is <strong>${pushData.status}</strong> at Counter <strong>${pushData.counter_no}</strong>!`;
    notificationModal.show();

    AppUtils.playNotificationSound();

    const { vendor_id, logo_url, vendor_name } = pushData;
    updateChatOnPush(vendor_id, logo_url, vendor_name);

    // Set or reset the 1-hour auto-clear timer
    if (clearTimers[token]) clearTimeout(clearTimers[token]);
    clearTimers[token] = setTimeout(() => {
        delete orderStates[token];
        AppUtils.saveOrderStates(orderStates);
    }, 3600000); // 1 hour
}



// Export methods
export { initNotificationModal, showNotificationModal };


