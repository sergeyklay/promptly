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
export function autoResizePromptTextarea(e) {
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
export function createChatElement(message, chatEntryRole) {
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
