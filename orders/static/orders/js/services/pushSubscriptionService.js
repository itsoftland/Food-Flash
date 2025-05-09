export const PushSubscriptionService = (() => {
    const VAPID_PUBLIC_KEY = "BAv_HFvgMBKxx3Jnse3fLMjzUEn3n3zS76GwEGQ_oOPR_40U1e7O4AiezuOReRTK4ULx2EaGC9kGAz-lzV791Tw".trim();

    const subscribe = async (token, vendor_id) => {
        try {
            function getIOSVersion() {
                const match = navigator.userAgent.match(/OS (\d+)_?(\d+)?/);
                if (match) {
                    return parseFloat(`${match[1]}.${match[2] || 0}`);
                }
                return null;
            }
            
            const iosVersion = getIOSVersion();
            if (iosVersion && iosVersion < 18) {
                console.warn("Push notifications may be unreliable on iOS < 18.");
            }
            
            if (!token) {
                console.error("Token not provided. Cannot subscribe.");
                return;
            }

            if (Notification.permission !== "granted") {
                console.error("Notification permission is not granted.");
                return;
            }

            let registration = await navigator.serviceWorker.getRegistration();
            if (!registration) {
                console.warn("No service worker found. Registering...");
                registration = await navigator.serviceWorker.register('/service-worker.js', { scope: '/' });
            }

            if (!navigator.serviceWorker.controller) {
                console.warn("Service worker not controlling page. Reloading...");
                window.location.reload();
                return;
            }

            let subscription = await registration.pushManager.getSubscription();
            // if (subscription) {
            //     try {
            //         await subscription.unsubscribe();
            //         console.log("Unsubscribed existing subscription.");
            //     } catch (err) {
            //         console.error("Failed to unsubscribe:", err);
            //     }
            // }
            if (subscription) {
                const stored = localStorage.getItem("pushSubscription");
                const newKey = AppUtils.urlBase64ToUint8Array(VAPID_PUBLIC_KEY);
                const payloadToCompare = JSON.stringify(subscription.toJSON());
            
                if (payloadToCompare !== stored) {
                    try {
                        await subscription.unsubscribe();
                        console.log("Unsubscribed outdated push subscription.");
                    } catch (err) {
                        console.error("Failed to unsubscribe:", err);
                    }
                } else {
                    console.log("Subscription unchanged. Skip resubscription.");
                    return; // avoid re-subscribing on iOS 17.5
                }
            }
            

            const convertedKey = AppUtils.urlBase64ToUint8Array(VAPID_PUBLIC_KEY);
            subscription = await registration.pushManager.subscribe({
                userVisibleOnly: true,
                applicationServerKey: convertedKey
            });

            console.log("New push subscription:", subscription);

            const newSubscriptionJSON = JSON.stringify(subscription);
            const storedSubscription = localStorage.getItem("pushSubscription");

            if (storedSubscription !== newSubscriptionJSON) {
                const browserId = AppUtils.getBrowserId();
                const sub = subscription.toJSON();

                const payload = {
                    endpoint: sub.endpoint,
                    keys: sub.keys,
                    browser_id: browserId,
                    token_number: token,
                    vendor: vendor_id
                };

                const response = await fetch('/vendors/api/save-subscription/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': AppUtils.getCSRFToken()
                    },
                    credentials: 'same-origin',
                    body: JSON.stringify(payload)
                });

                if (response.ok) {
                    localStorage.setItem("pushSubscription", newSubscriptionJSON);
                    console.log("Push subscription updated successfully.");
                } else {
                    console.error("Failed to save subscription to server.");
                }
            } else {
                console.log("Push subscription unchanged.");
            }

        } catch (err) {
            console.error("Error in subscribe:", err);
        }
    };

    return {
        subscribe
    };
})();


// export const PushSubscriptionService = (() => {
//     const VAPID_PUBLIC_KEY = "BAv_HFvgMBKxx3Jnse3fLMjzUEn3n3zS76GwEGQ_oOPR_40U1e7O4AiezuOReRTK4ULx2EaGC9kGAz-lzV791Tw".trim();

//     const getIOSVersion = () => {
//         const match = navigator.userAgent.match(/OS (\d+)_?(\d+)?/);
//         if (match) {
//             return parseFloat(`${match[1]}.${match[2] || 0}`);
//         }
//         return null;
//     };

//     const isIOS17Buggy = () => {
//         const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent);
//         const iosVersion = getIOSVersion();
//         return isIOS && iosVersion && iosVersion < 18;
//     };

//     const subscribe = async (token, vendor_id) => {
//         try {
//             if (!token) {
//                 console.error("Token not provided. Cannot subscribe.");
//                 return;
//             }

//             if (Notification.permission !== "granted") {
//                 console.error("Notification permission is not granted.");
//                 return;
//             }

//             let registration = await navigator.serviceWorker.getRegistration();
//             if (!registration) {
//                 console.warn("No service worker found. Registering...");
//                 registration = await navigator.serviceWorker.register('/service-worker.js', { scope: '/' });
//             }

//             if (!navigator.serviceWorker.controller) {
//                 console.warn("Service worker not controlling page. Reloading...");
//                 window.location.reload();
//                 return;
//             }

//             let subscription = await registration.pushManager.getSubscription();
//             const storedSubscription = localStorage.getItem("pushSubscription");
//             const convertedKey = AppUtils.urlBase64ToUint8Array(VAPID_PUBLIC_KEY);

//             const shouldUnsubscribe = subscription && !isIOS17Buggy() && JSON.stringify(subscription.toJSON()) !== storedSubscription;

//             if (shouldUnsubscribe) {
//                 try {
//                     await subscription.unsubscribe();
//                     console.log("Unsubscribed outdated push subscription.");
//                     subscription = null;
//                 } catch (err) {
//                     console.error("Failed to unsubscribe:", err);
//                 }
//             } else if (subscription && isIOS17Buggy()) {
//                 console.warn("iOS < 18 detected — skipping unsubscribe to avoid bug.");
//             }

//             if (!subscription) {
//                 try {
//                     subscription = await registration.pushManager.subscribe({
//                         userVisibleOnly: true,
//                         applicationServerKey: convertedKey
//                     });
//                     console.log("Successfully created new push subscription:", subscription);
//                 } catch (subErr) {
//                     console.error("Failed to subscribe for push:", subErr);
//                     return;
//                 }
//             } else {
//                 console.log("Using existing push subscription.");
//             }

//             // Send to server
//             const newSubscriptionJSON = JSON.stringify(subscription);
//             if (newSubscriptionJSON !== storedSubscription) {
//                 const browserId = AppUtils.getBrowserId();
//                 const sub = subscription.toJSON();

//                 const payload = {
//                     endpoint: sub.endpoint,
//                     keys: sub.keys,
//                     browser_id: browserId,
//                     token_number: token,
//                     vendor: vendor_id
//                 };

//                 const response = await fetch('/vendors/api/save-subscription/', {
//                     method: 'POST',
//                     headers: {
//                         'Content-Type': 'application/json',
//                         'X-CSRFToken': AppUtils.getCSRFToken()
//                     },
//                     credentials: 'same-origin',
//                     body: JSON.stringify(payload)
//                 });

//                 if (response.ok) {
//                     localStorage.setItem("pushSubscription", newSubscriptionJSON);
//                     console.log("Push subscription saved to server.");
//                 } else {
//                     console.error("Failed to save subscription to server.");
//                 }
//             } else {
//                 console.log("Push subscription unchanged. Skipping server update.");
//             }

//         } catch (err) {
//             console.error("Error in subscribe:", err);
//         }
//     };

//     return {
//         subscribe
//     };
// })();
