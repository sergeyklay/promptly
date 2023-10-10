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
    try:
        mode = os.getenv('PROMPTLY_MAINTENANCE_MODE', 'False')
        if strtobool(mode):
            abort(503)
    except ValueError:
        pass


@main.route('/')
def index():
    return render_template('home.html')


@main.route('/conversation', methods=['POST'])
def process_chat():
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
