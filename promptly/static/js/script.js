/**
 * This file is part of the Promptly.
 *
 * Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
 *
 * For the full copyright and license information, please view
 * the LICENSE file that was distributed with this source code.
 */

/**
 * Automatically resizes the textarea element based on its content.
 *
 * @param {HTMLTextAreaElement} e - The textarea element to resize.
 */
function autoResizePromptTextarea(e) {
  e.style.height = "auto";

  let newHeight;
  const computedLineHeight = window.getComputedStyle(e).lineHeight;
  const numericLineHeight = parseFloat(computedLineHeight);
  const maxHeight = numericLineHeight * 8;

  if (e.scrollHeight > maxHeight) {
    newHeight = maxHeight;
    e.style.overflowY = "auto";
  } else {
    newHeight = e.scrollHeight;
    e.style.overflowY = "hidden";
  }

  e.style.height = `${newHeight}px`;
}

/**
 * Appends a new message to the chat output container.
 *
 * @param {string} message - The message text to append.
 * @param {HTMLElement} outputContainer - The DOM element to which the message will be appended.
 */
function appendMessageToChat(message, outputContainer, isUserMessage) {
  const messageDiv = document.createElement('div');
  messageDiv.className = isUserMessage ? 'chat-message user-message' : 'chat-message server-response';

  const header = document.createElement('div');
  header.className = 'message-header';
  header.textContent = isUserMessage ? 'You' : 'AI';

  const body = document.createElement('div');
  body.className = 'message-body';
  body.innerHTML = `<p>${message}</p>`;

  messageDiv.appendChild(header);
  messageDiv.appendChild(body);

  outputContainer.appendChild(messageDiv);
}

document.addEventListener("DOMContentLoaded", function() {
  // Add the input event listener to the textarea
  document.addEventListener("input", function(event) {
    if (event.target.tagName.toLowerCase() === "textarea") {
      autoResizePromptTextarea(event.target);
    }
  });

  let sidebarVisible = true;

  const sidebarTogglerBtn = document.getElementById("sidebar-toggler-btn");
  sidebarTogglerBtn.addEventListener("click", function() {
    const sidebar = document.getElementById("sidebar");
    const chatWindow = document.getElementById("chat-window");
    const iconElement = this.querySelector("i");

    if (sidebarVisible) {
      sidebar.style.left = "-250px";
      this.style.left = "10px";
      chatWindow.style.left = "0";
      chatWindow.style.width = "100%";
      iconElement.textContent = "chevron_right";
    } else {
      sidebar.style.left = "0";
      this.style.left = "180px";
      chatWindow.style.left = "250px";
      chatWindow.style.width = "calc(100% - 250px)";
      iconElement.textContent = "menu";
    }

    sidebarVisible = !sidebarVisible;
  });

  const newChatBtn = document.getElementById("new-chat");
  newChatBtn.addEventListener("click", function() {
    alert("New chat created!");
  });

  const sendButton = document.getElementById("send-button");
  sendButton.addEventListener("click", function() {
    const userMessage = document.getElementById("prompt-textarea").value;
    const chatOutput = document.getElementById("chat-output");

    if (userMessage.length > 0) {
      document.getElementById("prompt-textarea").value = '';
      appendMessageToChat(userMessage, chatOutput, true);

      const loadingElement = document.createElement("div");
      loadingElement.className = "loading";
      loadingElement.textContent = "Waiting for server response";
      chatOutput.appendChild(loadingElement);

      // Replace with fetch API instead of jQuery's $.ajax
      fetch('/conversation', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userMessage })
      })
      .then(response => response.json())
      .then(data => {
        loadingElement.remove();
        appendMessageToChat(data.message, chatOutput, false);
      })
      .catch(() => {
        // TODO: Show error
        loadingElement.remove();
      });

      chatOutput.scrollTop = chatOutput.scrollHeight;
    }
  });

  const promptTextarea = document.getElementById("prompt-textarea");
  promptTextarea.addEventListener("keypress", function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendButton.click();
    }
  });
});
