document.addEventListener("DOMContentLoaded", function () {
    console.log("Order tracking system initialized");
    const orderSlotIds = [
        'left-col-1',
        'left-col-2',
        'right-col-1',
        'right-col-2',
        'right-col-3',
        'right-col-4',
        'right-col-5',
        'right-col-6'
    ];
    
    function fetchAndDisplayRecentOrders() {
        fetch('/api/get_recent_orders/')
            .then(response => {
                if (!response.ok) {
                    throw new Error("Failed to fetch orders");
                }
                return response.json();
            })
            .then(data => {
                // Clear previous content
                orderSlotIds.forEach(id => {
                    const slot = document.getElementById(id);
                    if (slot) slot.innerHTML = '';
                });

                // Filter only ready orders and sort by most recent
                const readyOrders = data
                    .filter(order => order.status === 'ready')
                    .sort((a, b) => new Date(b.updated_at) - new Date(a.updated_at))
                    .slice(0, 8);

                readyOrders.forEach((order, index) => {
                    const slotId = orderSlotIds[index];
                    const slotEl = document.getElementById(slotId);

                    if (slotEl) {
                        const orderHTML = `
                            <div class="order-card" style="animation-delay: ${index * 0.05}s">
                                <div class="order-number">${order.token_no}</div>
                                <div class="order-details" style="display: none;">
                                    <p class="mb-1">Vendor: ${order.vendor || 'N/A'}</p>
                                    <small>Ready at: ${new Date(order.updated_at).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</small>
                                </div>
                            </div>
                        `;
                        slotEl.innerHTML = orderHTML;
                    }
                });

                // Hide any unused slots
                for (let i = readyOrders.length; i < orderSlotIds.length; i++) {
                    const slot = document.getElementById(orderSlotIds[i]);
                    if (slot) slot.innerHTML = '';
                }
            })
            .catch(error => {
                console.error("Error fetching recent orders:", error);
                // Optional: Display error to user
            });
    }
    
    // Enhanced auto-refresh with error handling
    let refreshInterval = setInterval(() => {
        try {
            fetchAndDisplayRecentOrders();
        } catch (e) {
            console.error("Error in refresh cycle:", e);
        }
    }, 5000);
    
    // Initial load with error handling
    try {
        fetchAndDisplayRecentOrders();
    } catch (e) {
        console.error("Initial load failed:", e);
    }

    // Clean up interval when page unloads
    window.addEventListener('beforeunload', () => {
        clearInterval(refreshInterval);
    });
});