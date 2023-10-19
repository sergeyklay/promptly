# This file is part of the Promptly.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Chat module for the Promptly Flask application."""

from flask import Blueprint, render_template


chat_bp = Blueprint('chat', __name__)


@chat_bp.route('/')
def chat():
    """Render the homepage of the application.

    :return: The rendered homepage template.
    :rtype: str
    """
    from promptly.models import Chat
    chats = Chat.query.all()
    return render_template('chat.html', chats=chats)
