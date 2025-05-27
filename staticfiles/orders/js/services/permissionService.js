export const PermissionService = (() => {

    const showModal = () => {
        const modalElement = document.getElementById("permissionModal");
        if (!localStorage.getItem("permissionStatus") && modalElement) {
            const bsModal = new bootstrap.Modal(modalElement, {
                backdrop: 'static',
                keyboard: false
            });
            bsModal.show();
        }
    };

    const requestPermissions = async () => {
        const current = Notification.permission;
        console.log("Current notification permission:", current);

        if (current === "granted") {
            return true;
        }

        if (current === "denied") {
            showDeniedModal();
            return false;
        }

        const permission = await Notification.requestPermission();
        if (permission === "granted") {
            return true;
        } else {
            showDeniedModal();
            return false;
        }
    };

    const showDeniedModal = () => {
        const helpModal = document.getElementById("notificationHelpModal");
        if (helpModal) {
            const bsHelpModal = new bootstrap.Modal(helpModal, {
                backdrop: 'static',
                keyboard: true
            });
            bsHelpModal.show();
        } else {
            AppUtils.showToast("You won’t receive real-time notifications unless enabled manually from browser settings");
        }
    };

    const handleAgree = () => {
        localStorage.setItem("permissionStatus", "granted");
        bootstrap.Modal.getInstance(document.getElementById("permissionModal"))?.hide();
        requestPermissions();
        playWelcomeMessage();
    };

    const handleDeny = () => {
        localStorage.setItem("permissionStatus", "denied");
        bootstrap.Modal.getInstance(document.getElementById("permissionModal"))?.hide();
        showDeniedModal();
    };

    const bindEvents = () => {
        document.getElementById("grant-permission")?.addEventListener("click", handleAgree);
        document.getElementById("deny-permission")?.addEventListener("click", handleDeny);
    };

    const playWelcomeMessage = () => {
        const welcome = new SpeechSynthesisUtterance('Hi, Welcome. Please enter your token number to track your order.');
        speechSynthesis.speak(welcome);
    };

    return {
        init: bindEvents,
        showModal,
        requestPermissions
    };
})();
