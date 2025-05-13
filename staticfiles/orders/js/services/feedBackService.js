import { appendMessage } from './chatService.js';

export const FeedbackService = (() => {
    const steps = [
        { key: 'feedback_type', question: 'Select Feedback Type', options: ['Complaint', 'Suggestion', 'Compliment'] },
        { key: 'category', question: 'Is it about Dish or Service?', options: ['Dish', 'Service'] },
        { key: 'final', question: 'Leave your comment', input: true }
    ];

    let formData = {};
    let isCooldown = false;

    const clearFromStep = (stepIndex) => {
        // Remove buttons and inputs from DOM starting from the affected step
        const chatContainer = document.getElementById("chat-container");
        const allInteractive = chatContainer.querySelectorAll('button, input, textarea');
        allInteractive.forEach(el => el.remove());

        // Clear data from all steps after stepIndex
        for (let i = stepIndex + 1; i < steps.length; i++) {
            delete formData[steps[i].key];
        }
    };

    const renderStep = (fromStep = 0) => {
        const step = steps[fromStep];
        if (!step) return;

        const chatContainer = document.getElementById("chat-container");
        appendMessage(step.question, "server");

        if (step.options) {
            clearFromStep(fromStep);

            step.options.forEach(option => {
                const btn = document.createElement('button');
                btn.className = 'btn btn-outline-primary m-1';
                btn.textContent = option;

                btn.onclick = () => {
                    const selectedValue = option.toLowerCase();

                    // Save or update selection
                    const previous = formData[step.key];
                    if (previous !== selectedValue) {
                        appendMessage(option, "user");
                        formData[step.key] = selectedValue;

                        // Clear next steps & rerender
                        renderStep(fromStep + 1);
                    }
                };

                chatContainer.appendChild(btn);
            });
        }

        if (step.input) {
            clearFromStep(fromStep);

            const nameInput = document.createElement('input');
            nameInput.className = 'form-control my-2';
            nameInput.placeholder = 'Your name (optional)';
            nameInput.id = 'feedback-name';

            const commentBox = document.createElement('textarea');
            commentBox.className = 'form-control my-2';
            commentBox.placeholder = 'Your comment...';
            commentBox.id = 'feedback-comment';

            const submitBtn = document.createElement('button');
            submitBtn.className = 'btn btn-outline-primary mt-2';
            submitBtn.textContent = 'Submit';

            submitBtn.onclick = () => {
                const name = nameInput.value.trim();
                const comment = commentBox.value.trim();
                if (!name && !comment) {
                    appendMessage("⚠️ Please provide at least a comment or name.", "server");
                    return;
                }
                formData['name'] = name;
                formData['comment'] = comment;
                submitBtn.disabled = true;
                console.log("Feedback form submitted:", formData);
                submitFeedback(submitBtn);
            };

            chatContainer.appendChild(nameInput);
            chatContainer.appendChild(commentBox);
            chatContainer.appendChild(submitBtn);
        }

        chatContainer.scrollTop = chatContainer.scrollHeight;
    };

    const submitFeedback = async (submitBtn) => {
        if (isCooldown) {
            appendMessage("⏳ Please wait before submitting again.", "server");
            return;
        }

        const vendorId = AppUtils.getActiveVendor();
        if (!vendorId) {
            appendMessage("⚠️ Vendor not found. Please try again later.", "server");
            return;
        }

        try {
            const response = await fetch("/api/submit_feedback/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": AppUtils.getCSRFToken()
                },
                body: JSON.stringify({
                    vendor_id: vendorId,
                    ...formData
                })
            });

            const data = await response.json();
            if (data.success) {
                appendMessage("✅ Thank you for your feedback!", "server");
                clearFromStep(0);
                formData = {};
                isCooldown = true;

                setTimeout(() => {
                    isCooldown = false;
                }, 60000);
            } else {
                appendMessage(data.message || "❌ Failed to submit feedback.", "server");
                if (submitBtn) submitBtn.disabled = false;
            }
        } catch (error) {
            console.error("Error submitting feedback:", error);
            appendMessage("❌ An error occurred. Please try again later.", "server");
            if (submitBtn) submitBtn.disabled = false;
        }
    };

    const startFeedback = () => {
        if (isCooldown) {
            appendMessage("⏳ Please wait before submitting again.", "server");
            return;
        }

        formData = {};
        renderStep(0);
    };

    const bindEvents = () => {
        const buttons = document.querySelectorAll(".footer-button");
        buttons.forEach(button => {
            button.addEventListener("click", function () {
                buttons.forEach(btn => btn.classList.remove("active"));
                this.classList.add("active");

                if (this.classList.contains("feedback-btn")) {
                    startFeedback();
                }
            });
        });
    };

    return {
        init: bindEvents,
        startFeedback
    };
})();
