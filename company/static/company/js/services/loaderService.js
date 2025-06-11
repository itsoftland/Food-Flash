export default function createLoaderService(form) {
  const loaderOverlay = document.getElementById("loaderOverlay");
  const loaderStatus = document.getElementById("loaderStatus");
  const okButton = document.getElementById("loaderOkBtn");
  const submitButton = form.querySelector('button[type="submit"]');

  let okCallback = null; // Store callback for OK button

  function showLoader(message = "Submitting data...", waitForUser = false, callback = null) {
    console.log("[Loader] showLoader called:", { message, waitForUser, callback });

    if (loaderOverlay) {
      loaderOverlay.style.display = "flex";
      console.log("[Loader] loaderOverlay displayed");
    }

    if (loaderStatus) {
      loaderStatus.textContent = message;
      console.log("[Loader] loaderStatus updated:", message);
    }

    if (submitButton) {
      submitButton.disabled = true;
      console.log("[Loader] submitButton disabled");
    }

    if (okButton) {
      if (waitForUser) {
        okButton.style.display = "inline-block";
        okCallback = callback;
        console.log("[Loader] OK button shown, callback set");
      } else {
        okButton.style.display = "none";
        okCallback = null;
        console.log("[Loader] OK button hidden, callback cleared");
      }
    }
  }

  function updateLoaderStatus(message, waitForUser = false, callback = null) {
    console.log("[Loader] updateLoaderStatus called:", { message, waitForUser, callback });

    if (loaderStatus) {
      loaderStatus.textContent = message;
      console.log("[Loader] loaderStatus updated:", message);
    }

    if (okButton) {
      if (waitForUser) {
        okButton.style.display = "inline-block";
        okCallback = callback;
        console.log("[Loader] OK button shown, callback set");

        if (loaderOverlay) {
          loaderOverlay.style.display = "flex";
          console.log("[Loader] loaderOverlay ensured visible");
        }

        if (submitButton) {
          submitButton.disabled = true;
          console.log("[Loader] submitButton disabled");
        }
      } else {
        okButton.style.display = "none";
        okCallback = null;
        console.log("[Loader] OK button hidden, callback cleared");

        if (loaderOverlay) {
          loaderOverlay.style.display = "none";
          console.log("[Loader] loaderOverlay hidden");
        }

        if (submitButton) {
          submitButton.disabled = false;
          console.log("[Loader] submitButton enabled");
        }
      }
    }
  }

  function hideLoader() {
    console.log("[Loader] hideLoader called");

    if (loaderOverlay) {
      loaderOverlay.style.display = "none";
      console.log("[Loader] loaderOverlay hidden");
    }

    if (submitButton) {
      submitButton.disabled = false;
      console.log("[Loader] submitButton enabled");
    }

    if (okButton) {
      okButton.style.display = "none";
      console.log("[Loader] OK button hidden");
    }

    // Don't clear okCallback here; let click handler manage it
  }

  // ✅ Bind OK button only once
  if (okButton && !okButton.dataset.bound) {
    console.log("[Loader] Binding OK button click listener");
    okButton.addEventListener("click", () => {
      console.log("[Loader] OK button clicked");

      if (okCallback) {
        const callback = okCallback;
        okCallback = null;
        console.log("[Loader] Executing okCallback...");
        hideLoader();       // Hide loader first
        callback();         // Then execute callback
      } else {
        console.warn("[Loader] OK button clicked but no okCallback found");
        hideLoader(); // Still hide loader even if no callback
      }
    });
    okButton.dataset.bound = "true";
  }

  return {
    showLoader,
    updateLoaderStatus,
    hideLoader,
  };
}
