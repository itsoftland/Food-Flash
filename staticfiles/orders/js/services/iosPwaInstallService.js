export const IosPwaInstallService = (() => {
    let modalInstance = null;

    const isIosSafari = () => {
        const ua = window.navigator.userAgent.toLowerCase();
        const isIos = /iphone|ipad|ipod/.test(ua);
        const isSafari = /^((?!chrome|android).)*safari/i.test(window.navigator.userAgent);
        return isIos && isSafari;
    };

    const isInStandaloneMode = () => {
        return ('standalone' in window.navigator) && window.navigator.standalone;
    };

    const shouldShowPrompt = () => {
        const alreadyShown = localStorage.getItem("iosPwaPromptShown");
        return !alreadyShown;
    };

    const showModal = () => {
        const modalEl = document.getElementById("iosInstallModal");
        if (modalEl && !modalInstance) {
            modalInstance = new bootstrap.Modal(modalEl, {
                backdrop: 'static',
                keyboard: false
            });
        }
        modalInstance?.show();
    };

    const dismiss = () => {
        if (modalInstance) {
            modalInstance.hide();
        }
        localStorage.setItem("iosPwaPromptShown", "true");
    };

    const init = () => {
        if (isIosSafari() && !isInStandaloneMode() && shouldShowPrompt()) {
            showModal();
        }
    };

    return {
        init,
        dismiss
    };
})();
