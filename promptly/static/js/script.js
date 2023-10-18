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
 * @returns {HTMLDivElement}
 */
function createChatElement(message) {
  const messageWrapper = document.createElement('div');
  messageWrapper.className = 'row chat-message';

  const messageContainer = document.createElement('div');
  messageContainer.className = 'col-md-12'

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

document.addEventListener('DOMContentLoaded', function() {
  const textarea = document.getElementById('prompt-textarea');
  textarea.addEventListener('input', () => {
    autoResizePromptTextarea(textarea);
  });

  const sendButton = document.getElementById('send-button');
  sendButton.addEventListener('click', function() {
    const userMessage = document.getElementById('prompt-textarea').value;
    const chatOutput = document.getElementById('chat-output');

    if (userMessage.length > 0) {
      document.getElementById('prompt-textarea').value = '';
      chatOutput.appendChild(createChatElement(userMessage));

      const loadingRow = createChatElement('Waiting for server response');
      chatOutput.appendChild(loadingRow);

      fetch('/conversation', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userMessage })
      })
      .then(response => response.json())
      .then(data => {
        loadingRow.remove();
        chatOutput.appendChild(createChatElement(data.message));
      })
      .catch(() => {
        // TODO: Show error
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
