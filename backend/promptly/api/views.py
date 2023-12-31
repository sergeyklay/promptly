# This file is part of the Promptly.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""
Module for serving chat API request.
------------------------------------

This module contains a blueprint for a Flask application to handle chat API
requests. It processes a user's chat message and returns the model's
response.
"""

from flask import Blueprint, jsonify, request

from promptly.models import Chat, ChatEntry
from promptly.services import OpenAIService
from promptly.utils import try_parse_int

api_bp = Blueprint('api', __name__)
openai_service = OpenAIService()


@api_bp.route('/conversation', methods=['POST'])
def conversation():
    """Process a user's chat message and return the model's response.

    Extracts the user's message from the request form, sends it to OpenAI for
    processing, extracts the response from OpenAI's reply, and sends the
    response back to the user.

    :return: A JSON object containing the model's response to the user's
        message.
    :rtype: flask.Response
    :raises Exception: ``openai.error.OpenAIError`` for issues with the OpenAI
        call.
    """
    data = request.json
    message, chat_id = data.get('message'), data.get('chat_id')

    chat_id = try_parse_int(chat_id)
    chat = Chat.get(chat_id) if chat_id else Chat.create_new_chat()
    if chat is None:
        chat = Chat.create_new_chat()

    ChatEntry.create(content=message, chat=chat, role='user').save()

    response = openai_service.get_response(message)
    ChatEntry.create(content=response, chat=chat, role='assistant').save()

    return jsonify({
        'message': response,
        'chat_id': chat.id,
    })
