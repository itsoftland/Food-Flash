export const IosPwaInstallService = (() => {
    console.log("Ios Pwa Install Service called")
    let modalInstance = null;

    const isIosSafari = () => {
        const ua = window.navigator.userAgent.toLowerCase();
        const isIos = /iphone|ipad|ipod/.test(ua);
        const isSafari = /^((?!chrome|android).)*safari/i.test(window.navigator.userAgent);
        console.log(isIos && isSafari);
        return isIos && isSafari;
    };

    const isInStandaloneMode = () => {
        console.log('standalone' in window.navigator) && window.navigator.standalone;
        return ('standalone' in window.navigator) && window.navigator.standalone;
    };

    const hasAgreed = () => localStorage.getItem("iosA2HS") === "true";
    const hasDenied = () => localStorage.getItem("iosA2HS") === "false";

    const shouldShowPrompt = () => {
        console.log("should prompt")
        return !(hasAgreed() || hasDenied());
    };
    const shouldRePrompt = () => {
        return hasAgreed() && !isInStandaloneMode();
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
        console.log("modal shown")
    };

    const dismiss = () => {
        modalInstance?.hide();
    };

    const init = () => {
        if (isIosSafari() && !isInStandaloneMode() && shouldShowPrompt()) {
            console.log("showmodal")
            showModal();
        }
    };

    return {
        init,
        showModal,
        dismiss,
        hasAgreed,
        hasDenied,
        isInStandaloneMode,
        shouldRePrompt
    };
})();
