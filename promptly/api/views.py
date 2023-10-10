# This file is part of the Promptly.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Module for serving chat API request."""

import os

import openai
from flask import jsonify, request

from . import api


GPT_MODEL = 'gpt-3.5-turbo-16k'


@api.route('/conversation', methods=['POST'])
def conversation():
    """Process a user's chat message and return the model's response.

    Extracts the user's message from the request form, sends it to OpenAI for
    processing, extracts the response from OpenAI's reply, and sends the
    response back to the user.

    :return: A JSON object containing the model's response to the user's
             message.
    :rtype: flask.Response
    :raises: A variety of exceptions, such as `openai.error.OpenAIError` for
             issues with the OpenAI call.
    """
    query = request.form.get('message')

    openai.api_key = os.getenv('OPENAI_API_KEY')
    response = openai.ChatCompletion.create(
        messages=[{'role': 'user', 'content': query}],
        model=GPT_MODEL,
        temperature=0,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    response_message = response['choices'][0]['message']['content']

    return jsonify({'message': response_message})
