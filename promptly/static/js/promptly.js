/**
 * This file is part of the Promptly.
 *
 * Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
 *
 * For the full copyright and license information, please view
 * the LICENSE file that was distributed with this source code.
 */

import { autoResizePromptTextarea, createChatElement } from './chat.js';
import { getCookie, setCookie } from './cookie.js';

document.addEventListener('DOMContentLoaded', function() {
  const textarea = document.getElementById('prompt-textarea');
  const sendButton = document.getElementById('send-button');

  textarea.addEventListener('input', () => {
    autoResizePromptTextarea(textarea);
  });

  textarea.addEventListener('keypress', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendButton.click();
    }
  });

  sendButton.addEventListener('click', function() {
    const userInput = textarea.value;
    const chatOutput = document.getElementById('chat-output');

    if (userInput.length > 0) {
      textarea.value = '';
      textarea.style.height = 'initial';

      chatOutput.appendChild(createChatElement(userInput, 'user'));
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
        chatOutput.appendChild(createChatElement(data.message, 'assistant'));
      })
      .catch(() => {
        // TODO: Log error
        loadingRow.remove();
      });

      chatOutput.scrollTop = chatOutput.scrollHeight;
    }
  });
});
