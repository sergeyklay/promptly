# This file is part of the Promptly.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Chat module for the Promptly Flask application."""

from datetime import datetime, timedelta

from flask import Blueprint, render_template

chat_bp = Blueprint('chat', __name__)


@chat_bp.route('/')
def chat():
    """Render the homepage of the application.

    :return: The rendered homepage template.
    :rtype: str
    """
    return render_template('chat/chat.html', active_page='chat')


@chat_bp.route('/history')
def history():
    """Render the chat history of the application.

    :return: The rendered chat history template.
    :rtype: str
    """
    from promptly.models import Chat
    chats = Chat.query.all()
    return render_template(
        'chat/history.html',
        chats=chats,
        active_page='history'
    )


@chat_bp.app_template_filter()
def human_readable_date(value: datetime):
    """Convert a datetime object to a human readable date.

    This function takes a datetime object and returns a string that represents
    a more human-readable and context-sensitive representation of the time. The
    output will be one of the following:

    - ``Today``
    - ``Yesterday``
    - ``Previous 7 Days``
    - ``Previous 30 Days``
    - ``Previous Year``
    - ``Older``

    :param datetime.datetime value: The datetime object to be converted.
    :return: A string representing the human-readable date.
    :rtype: str

    Example::

        >>> human_readable_date(datetime(2023, 10, 21))
        'Today'

    """
    today = datetime.now().date()
    date_val = str(value).split(' ', maxsplit=1)[0]
    value_date = datetime.strptime(date_val, '%Y-%m-%d').date()

    time_ranges = [
        (0, 'Today'),
        (1, 'Yesterday'),
        (7, 'Previous 7 Days'),
        (30, 'Previous 30 Days'),
        (365, 'Previous Year')
    ]

    for days, label in time_ranges:
        if today - timedelta(days=days) <= value_date <= today:
            return label

    return 'Older'
