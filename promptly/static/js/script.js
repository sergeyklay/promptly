/**
 * This file is part of the Promptly.
 *
 * Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
 *
 * For the full copyright and license information, please view
 * the LICENSE file that was distributed with this source code.
 */

// Function to auto-resize the textarea
function autoResize(element) {
  // Reset height to auto to shrink back if needed
  $(element).css('height', 'auto');

  var newHeight;
  if(element.scrollHeight > 304) {  // 304 = 38*8, where 38 is the line-height
    newHeight = 304;
    $(element).css('overflow-y', 'auto');
  } else {
    newHeight = element.scrollHeight;
    $(element).css('overflow-y', 'hidden');
  }

  // Set the height to the scroll height or max-height
  $(element).css('height', newHeight + 'px');
}

// Add the input event listener to the textarea using jQuery
$(document).on('input', 'textarea', function() {
  autoResize(this);
});

$(document).ready(function() {
  $('#minimize-btn').on('click', function() {
    $('#sidebar').toggleClass('minimized');
  });

  $('#send-btn').on('click', function() {
    var messageText = $('#prompt-textarea').val().trim();
    if (messageText.length > 0) {
      $('#prompt-textarea').val('');

      // TODO: Send request to server

      var newMessageHtml = '<div class="chat-message">' +
          '<p>' + messageText + '</p>' +
          '</div>';

      $('#chat-output').append(newMessageHtml);
      $('#chat-output').scrollTop($('#chat-output')[0].scrollHeight);
    }
  });

  $('#prompt-textarea').on('keypress', function(e) {
    if (e.which == 13 && !e.shiftKey) {
      e.preventDefault();
      $('#send-btn').click();
    }
  });
});
