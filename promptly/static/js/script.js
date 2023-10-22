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
  e.style.height = 'auto';

  let newHeight;
  const computedLineHeight = window.getComputedStyle(e).lineHeight;
  const numericLineHeight = parseFloat(computedLineHeight);
  const maxHeight = numericLineHeight * 8;

  if (e.scrollHeight > maxHeight) {
    newHeight = maxHeight;
    e.style.overflowY = 'auto';
  } else {
    newHeight = e.scrollHeight;
    e.style.overflowY = 'hidden';
  }

  e.style.height = `${newHeight}px`;
}

/**
 * Create chat HTML node.
 *
 * @param {string} message - The message text to use to create chat element.
 * @param {string} chatEntryRole - The chat entry role to use to create chat element.
 * @returns {HTMLDivElement}
 */
function createChatElement(message, chatEntryRole) {
  const messageWrapper = document.createElement('div');
  messageWrapper.className = 'row chat-message';
  messageWrapper.setAttribute('data-entry-role', chatEntryRole)

  const messageContainer = document.createElement('div');
  messageContainer.className = 'col-12'

  const messageCard = document.createElement('div');
  messageCard.className = 'card bg-light py-2 py-md-3 border';

  const messageBody = document.createElement('div');
  messageBody.className = 'card-body';
  messageBody.textContent = message;

  messageWrapper.appendChild(messageContainer);
  messageContainer.appendChild(messageCard);
  messageCard.appendChild(messageBody);

  return messageWrapper;
}

/**
 * Sets a cookie with the given name, value, and expiration time.
 *
 * This function sets a cookie in the user's browser with a specific
 * name, value, and expiration time. The cookie will be accessible
 * from the JavaScript code for as long as it has not expired.
 *
 * @param {string} name - The name of the cookie.
 * @param {string} value - The value to store in the cookie.
 * @param {number} days - The number of days until the cookie expires.
 */
function setCookie(name, value, days) {
  let expires = '';
  if (days) {
    const date = new Date();
    date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
    expires = `; expires=${date.toUTCString()}`;
  }

  document.cookie = `${name}=${value || ''}${expires}; path=/`;
}

/**
 * Retrieves a cookie value by its name.
 *
 * This function attempts to find a cookie set in the user's browser
 * with the given name. If found, it returns the value of that cookie;
 * otherwise, it returns null.
 *
 * @param {string} name - The name of the cookie to retrieve.
 * @returns {string|null} The value of the cookie or null if not found.
 */
function getCookie(name) {
  const nameEQ = `${name}=`;
  const ca = document.cookie.split(';');
  for (let i = 0; i < ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) === ' ') c = c.substring(1, c.length);
    if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
  }
  return null;
}

document.addEventListener('DOMContentLoaded', function() {
  const textarea = document.getElementById('prompt-textarea');
  textarea.addEventListener('input', () => {
    autoResizePromptTextarea(textarea);
  });

  const sendButton = document.getElementById('send-button');
  sendButton.addEventListener('click', function() {
    const userInput = document.getElementById('prompt-textarea').value;
    const chatOutput = document.getElementById('chat-output');

    if (userInput.length > 0) {
      document.getElementById('prompt-textarea').value = '';
      const userMessage = createChatElement(
          userInput,
          'user'
      );
      chatOutput.appendChild(userMessage);
      const loadingRow = createChatElement(
          'Waiting for server response',
          'assistant'
      );
      chatOutput.appendChild(loadingRow);

      let currentChatId = getCookie('chat_id');
      fetch('/conversation', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userInput, chat_id: currentChatId })
      })
      .then(response => response.json())
      .then(data => {
        currentChatId = data.chat_id;
        setCookie('chat_id', currentChatId, 30);
        loadingRow.remove();

        const assistantMessage = createChatElement(
            data.message,
            'assistant'
        );
        chatOutput.appendChild(assistantMessage);
      })
      .catch(() => {
        // TODO: Log error
        loadingRow.remove();
      });

      chatOutput.scrollTop = chatOutput.scrollHeight;
    }
  });

  const promptTextarea = document.getElementById('prompt-textarea');
  promptTextarea.addEventListener('keypress', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendButton.click();
    }
  });
});
