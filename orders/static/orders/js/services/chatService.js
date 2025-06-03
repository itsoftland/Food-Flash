// static/js/chatService.js
import {ChatHistoryService}  from "./chatHistoryService.js";
export function updateChatOnPush(vendorId, logo_url, name) {
    document.querySelectorAll(".vendor-logo-wrapper").forEach(wrapper => {
        const logo = wrapper.querySelector("img");
        if (logo.dataset.vendorId == vendorId) {
            document.querySelectorAll(".vendor-logo-wrapper").forEach(w => w.classList.remove("active"));
            wrapper.classList.add("active");
            AppUtils.setSelectedOutletName(name);
            let ratingLink = localStorage.getItem("activeVendorRatingLink") || "https://default-rating-link.com";
            handleOutletSelection(vendorId, logo_url, ratingLink);
        }
    });
}

export function handleOutletSelection(vendorId, vendor_logo, placeId) {
    localStorage.setItem("activeVendor", vendorId);
    localStorage.setItem("activeVendorLogo", vendor_logo);
    localStorage.setItem("activeVendorRatingLink", placeId);

    const chatContainer = document.getElementById("chat-container");
    chatContainer.innerHTML = "";

    const outletName = AppUtils.getSelectedOutletName() || "our outlet";
    showWelcomeMessage(outletName);

    window.isRestoringHistory = true;
    const cachedMessages = ChatHistoryService.load(vendorId) || [];
    cachedMessages.forEach(msg => {
        appendMessage(msg.text, msg.sender, msg.timestamp);
    });
    window.isRestoringHistory = false;
}

export function showWelcomeMessage(outletName) {
    const chatContainer = document.getElementById("chat-container");
    if (!chatContainer) return;

    const messages = [
        `Hi, Good Day! Welcome to ${outletName}.`,
        "Kindly enter the Bill Number and Send so that we can track your order."
    ];

    messages.forEach(msg => {
        const messageRow = document.createElement("div");
        messageRow.classList.add("message-row", "server");

        const logoImg = document.createElement("img");
        logoImg.src = localStorage.getItem("activeVendorLogo") || "/static/images/default-logo.png";
        logoImg.alt = "Vendor Logo";
        logoImg.className = "server-logo";

        const messageBubble = document.createElement("div");
        messageBubble.classList.add("message-bubble", "server");
        messageBubble.textContent = msg;

        messageRow.appendChild(logoImg);
        messageRow.appendChild(messageBubble);
        chatContainer.appendChild(messageRow);
    });

    chatContainer.scrollTop = chatContainer.scrollHeight;
}

export function appendMessage(text, sender, timestamp = null) {
    const chatContainer = document.getElementById("chat-container");

    const messageRow = document.createElement('div');
    messageRow.classList.add('message-row', sender);

    const timeStamp = timestamp || new Date().toLocaleTimeString([], {
        hour: '2-digit',
        minute: '2-digit',
        hour12: true
    });

    const messageBubble = document.createElement('div');
    messageBubble.classList.add('message-bubble', sender);
    // <span class="message-check">&#10003;</span>
    messageBubble.innerHTML = `
    <div class="message-content">
        ${text}
        <span class="message-timestamp">
            ${timeStamp} 
        </span>
    </div>
    `;


    if (sender === 'server') {
        const activeLogo = localStorage.getItem("activeVendorLogo") || '/static/images/default-logo.png';
        const logoImg = document.createElement('img');
        logoImg.src = activeLogo;
        logoImg.alt = 'Vendor Logo';
        logoImg.className = 'server-logo';
        messageRow.appendChild(logoImg);
    }

    messageRow.appendChild(messageBubble);
    chatContainer.appendChild(messageRow);
    chatContainer.scrollTop = chatContainer.scrollHeight;

    if (!window.isRestoringHistory) {
        const activeVendorId = localStorage.getItem("activeVendor");
        if (activeVendorId) {
            const existingMessages = ChatHistoryService.load(activeVendorId) || [];
            existingMessages.push({ text, sender, timestamp: timeStamp });
            ChatHistoryService.save(activeVendorId, existingMessages);
        }
    }
    AppUtils.adjustChatResponsePadding();
}
