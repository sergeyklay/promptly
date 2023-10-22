# This file is part of the Promptly.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""
The chat module for the application.
------------------------------------
"""

from datetime import datetime, timedelta

from flask import (
    Blueprint,
    make_response,
    redirect,
    render_template,
    request,
    Response,
    url_for,
)
from sqlalchemy import desc

from promptly.models import Chat
from promptly.utils import try_parse_int

chat_bp = Blueprint('chat', __name__)


@chat_bp.route('/', methods=['GET'])
def chat_index() -> Response:
    """Redirect to the appropriate chat page based on cookie value.

    This function checks if a ``chat_id`` exists in cookies and if so,
    redirects the user to that specific chat page. Otherwise, a new chat page
    is rendered.

    :return: Redirect response or a call to :func:`.chat` function.
    :rtype: flask.Response
    """
    chat_id = try_parse_int(request.cookies.get('chat_id'))
    if chat_id and Chat.exists(chat_id):
        return redirect(url_for('chat.chat', chat_id=chat_id))

    return chat()


@chat_bp.route('/<int:chat_id>', methods=['GET'])
def chat(chat_id=None) -> Response:
    """Render the chat page of the application.

    :param int chat_id: The ID of the chat. If not exists, a new chat is
        created.
    :return: The rendered chat page template.
    :rtype: flask.Response
    """
    chat_instance = Chat.get(chat_id)
    if not chat_instance:
        chat_instance = Chat.create_new_chat()

    template = render_template(
        'chat/chat.html',
        chat=chat_instance,
        active_page='chat',
    )
    resp = make_response(template)
    resp.set_cookie('chat_id', str(chat_instance.id))
    return resp


@chat_bp.route('/history', methods=['GET'])
def history() -> str:
    """Render the chat history page of the application.

    :return: The rendered chat history template.
    :rtype: str
    """
    chats = Chat.query.order_by(desc(Chat.created_at)).all()
    return render_template(
        'chat/history.html',
        chats=chats,
        active_page='history'
    )


@chat_bp.app_template_filter()
def human_readable_date(value: datetime) -> str:
    """Convert a datetime object to a human-readable date.

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
