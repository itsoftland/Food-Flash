// notificationService.js
console.log("notification Service");
import { updateChatOnPush } from './chatService.js';

let notificationsEnabled = true;
let activeNotificationToken = null;
let snoozeTimers = {};
let orderStates = AppUtils.loadOrderStates();  // 💾 Load from storage
let notificationModal = null;
let clearTimers = {};  // Store timers to clear token after 1 hour

function initNotificationModal(modalInstance) {
    console.log("notificationInit Service");
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
                const userSnoozeDuration = 60000; // 🕒 Replace with actual user input (e.g., dropdown value)
                const now = Date.now();
    
                orderStates[token].snoozedAt = now;
                orderStates[token].snoozeDuration = userSnoozeDuration;
                AppUtils.saveOrderStates(orderStates);
    
                if (snoozeTimers[token]) clearTimeout(snoozeTimers[token]);
    
                snoozeTimers[token] = setTimeout(() => {
                    if (!orderStates[token].acknowledged) {
                        showNotificationModal(orderStates[token].data);
                        AppUtils.notifyOrderReady(orderStates[token].data);
                    }
                }, userSnoozeDuration);
            }
            activeNotificationToken = null;
        }
    });

    for (const [token, state] of Object.entries(orderStates)) {
        console.log("recall");
        if (!state.acknowledged && state.snoozedAt && state.snoozeDuration) {
            const now = Date.now();
            const elapsed = now - state.snoozedAt;
            const remaining = state.snoozeDuration - elapsed;
    
            if (remaining > 0) {
                snoozeTimers[token] = setTimeout(() => {
                    if (!orderStates[token].acknowledged) {
                        showNotificationModal(state.data);
                        AppUtils.notifyOrderReady(state.data);
                    }
                }, remaining);
            } else {
               
                // Snooze already expired while page was reloading
                showNotificationModal(state.data);
                AppUtils.notifyOrderReady(state.data);
            }
        }
    }     
}

function showNotificationModal(pushData, source) {
    console.log(orderStates)
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
    modalHeader.innerHTML = `
    Order <strong>${pushData.token_no}</strong> for <strong>${pushData.name}</strong>
     is now <strong>${pushData.status}</strong> at <strong>Counter ${pushData.counter_no}</strong>.`;
    const snoozeBtn = document.getElementById('disable-notifications');
    snoozeBtn.disabled = false;
    notificationModal.show();

    AppUtils.playNotificationSound();

    const { vendor_id, logo_url, name } = pushData;
    updateChatOnPush(vendor_id, logo_url, name);

    // Set or reset the 1-hour auto-clear timer
    if (clearTimers[token]) clearTimeout(clearTimers[token]);
    clearTimers[token] = setTimeout(() => {
        delete orderStates[token];
        AppUtils.saveOrderStates(orderStates);
    }, 60000); // 1 hour
}
// 3600000


// Export methods
export { initNotificationModal, showNotificationModal };


