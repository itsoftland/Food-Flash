export const FeedbackService = (() => {
    const steps = [
        { key: 'feedback_type', question: 'Select Feedback Type', options: ['Complaint', 'Suggestion', 'Compliment'] },
        { key: 'category', question: 'Is it about Dish or Service?', options: ['Dish', 'Service'] },
        { key: 'final', question: 'Leave your comment (optional)', input: true }
    ];

    let currentStep = 0;
    let formData = {};

    const container = document.getElementById('multi-step-feedback');
    const stepContainer = document.getElementById('feedback-step-container');
    const nextBtn = document.getElementById('feedback-next');
    const prevBtn = document.getElementById('feedback-prev');

    const renderStep = () => {
        console.log("Rendering step:", currentStep);
        const step = steps[currentStep];
        console.log("Current step object:", step);
        stepContainer.innerHTML = '';
    
        if (!step) {
            stepContainer.innerHTML = '<p>Error: Step not found</p>';
            return;
        }
    
        const title = document.createElement('h5');
        title.textContent = step.question;
        stepContainer.appendChild(title);
    
        if (step.input) {
            console.log("Rendering input fields...");
    
            const nameInput = document.createElement('input');
            nameInput.className = 'form-control mt-2';
            nameInput.placeholder = 'Your name (optional)';
            nameInput.id = 'feedback-name';
            stepContainer.appendChild(nameInput);
    
            const commentBox = document.createElement('textarea');
            commentBox.className = 'form-control mt-2';
            commentBox.placeholder = 'Your comment...';
            commentBox.id = 'feedback-comment';
            stepContainer.appendChild(commentBox);
        } else {
            console.log("Rendering options...", step.options);
    
            step.options.forEach(option => {
                const btn = document.createElement('button');
                btn.className = 'btn btn-outline-primary m-1';
                btn.textContent = option;
                btn.onclick = () => {
                    formData[step.key] = option.toLowerCase();
                    goToNextStep();
                };
                stepContainer.appendChild(btn);
            });
        }
    
        // Show/hide navigation buttons
        prevBtn.style.display = currentStep > 0 ? 'inline-block' : 'none';
        nextBtn.style.display = step.input ? 'inline-block' : 'none';
    };
    

    const goToNextStep = () => {
        if (currentStep < steps.length - 1) {
            currentStep++;
            renderStep();
        } else {
            submitFeedback();
        }
    };

    const goToPrevStep = () => {
        if (currentStep > 0) {
            currentStep--;
            renderStep();
        }
    };

    const submitFeedback = async () => {
        const vendorId = getActiveVendor();
        const name = document.getElementById("feedback-name")?.value || '';
        const comment = document.getElementById("feedback-comment")?.value || '';

        if (!vendorId || (!comment.trim() && !name.trim())) {
            alert("Please provide at least a comment or name.");
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
                    ...formData,
                    name,
                    comment
                })
            });

            const data = await response.json();
            if (data.success) {
                alert("Thank you for your feedback!");
                container.style.display = 'none';
                currentStep = 0;
                formData = {};
            } else {
                alert(data.message || "Failed to submit feedback.");
            }

        } catch (error) {
            console.error("Error submitting feedback:", error);
            alert("An error occurred. Please try again later.");
        }
    };

    const openForm = () => {
        console.log("button clicked")
        console.log(container); // add this inside openForm
        console.log("stepContainer is", stepContainer);
        container.style.display = 'block';
        currentStep = 0;
        formData = {};
        renderStep();
    };

    const bindEvents = () => {
        document.getElementById("feedback-button")?.addEventListener("click", openForm);
        nextBtn?.addEventListener("click", goToNextStep);
        prevBtn?.addEventListener("click", goToPrevStep);
    };

    return {
        init: bindEvents
    };
})();
