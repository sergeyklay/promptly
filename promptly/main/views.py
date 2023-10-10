# This file is part of the Promptly.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""The routes module for the application."""

import os
import openai
from flask import abort, render_template, request, jsonify

from promptly.utils import strtobool
from . import main

GPT_MODEL = 'gpt-3.5-turbo-16k'


@main.before_app_request
def maintained():
    """Check if the application is in maintenance mode.

    This function is called before each request to the application.
    If the environment variable 'PROMPTLY_MAINTENANCE_MODE' is set to a truthy
    value, the function will abort the request with a 503 Service Unavailable
    status.

    :raises: 503 Service Unavailable, if the app is in maintenance mode.
    """
    try:
        mode = os.getenv('PROMPTLY_MAINTENANCE_MODE', 'False')
        if strtobool(mode):
            abort(503)
    except ValueError:
        pass


@main.route('/')
def index():
    """Render the homepage of the application.

    :return: The rendered homepage template.
    :rtype: str
    """
    return render_template('home.html')


@main.route('/conversation', methods=['POST'])
def process_chat():
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

    openai.api_key = os.getenv("OPENAI_API_KEY")
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
