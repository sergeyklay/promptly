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
 * @param {HTMLTextAreaElement} textarea - The textarea element to resize.
 * @returns {void}
 */
export function autoResizePromptTextarea(textarea) {
  if (!textarea || !textarea.nodeName || textarea.nodeName !== 'TEXTAREA') {
    return;
  }

  let overflowStatus = 'hidden';
  const currentMaxHeight = window.getComputedStyle(textarea).maxHeight;

  if (currentMaxHeight !== 'none' && parseFloat(currentMaxHeight) < textarea.scrollHeight) {
    overflowStatus = 'auto';
  }

  textarea.style.height = '0';
  textarea.style.overflowY = overflowStatus;

  const lineCount = textarea.value.split('\n').length;
  textarea.style.height = `${calculateTextareaHeight(lineCount, textarea)}px`;
}

/**
 * Calculates the textarea height based on its content.
 *
 * @param {number} lineCount - The number of lines in the textarea.
 * @param {HTMLTextAreaElement} textarea - The textarea element to resize.
 * @returns {number} The calculated textarea height.
 */
export function calculateTextareaHeight (lineCount, textarea) {
    const styles = window.getComputedStyle(textarea);
    const borderBottom = parseFloat(styles.borderBottomWidth) || 0;
    const borderTop = parseFloat(styles.borderTopWidth) || 0;
    const fontSize = parseFloat(styles.fontSize) || 0;
    const paddingBottom = parseFloat(styles.paddingBottom) || 0;
    const paddingTop = parseFloat(styles.paddingTop) || 0;

    let lineHeight = 0;
    if (styles.lineHeight === 'normal') {
        lineHeight = 1.2 * fontSize;
    } else {
        lineHeight = parseFloat(styles.lineHeight) || 0;
    }

    const stylesHeight = lineHeight * lineCount + borderBottom + borderTop + paddingBottom + paddingTop;
    const scrollHeight = textarea.scrollHeight + borderBottom + borderTop;

    return Math.max(stylesHeight, scrollHeight);
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
