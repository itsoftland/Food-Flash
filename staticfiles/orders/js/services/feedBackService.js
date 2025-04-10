export const FeedbackService = (() => {
    const openModal = () => {
        const modalElement = document.getElementById("feedbackModal");
        if (modalElement) {
            const bsModal = new bootstrap.Modal(modalElement, {
                backdrop: 'static',
                keyboard: true
            });
            bsModal.show();
        }
    };

    const submitFeedback = async () => {
        const vendorId = getActiveVendor();
        const comment = document.getElementById("feedback-textarea").value;

        if (!vendorId || !comment.trim()) {
            alert("Please enter feedback.");
            return;
        }

        try {
            const response = await fetch("/api/submit_feedback/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken()
                },
                body: JSON.stringify({
                    vendor_id: vendorId,
                    comment: comment.trim()
                })
            });

            const data = await response.json();
            if (data.success) {
                alert("Thank you for your feedback!");
                document.getElementById("feedback-textarea").value = "";
                bootstrap.Modal.getInstance(document.getElementById("feedbackModal")).hide();
            } else {
                alert(data.message || "Failed to submit feedback.");
            }

        } catch (error) {
            console.error("Error submitting feedback:", error);
            alert("An error occurred. Please try again later.");
        }
    };

    const bindEvents = () => {
        document.getElementById("feedback-button")?.addEventListener("click", openModal);
        document.getElementById("submit-feedback-btn")?.addEventListener("click", submitFeedback);
    };

    return {
        init: bindEvents
    };
})();
