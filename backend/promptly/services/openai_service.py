# This file is part of the Promptly.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""
OpenAI Service Wrapper.
-----------------------

The :mod:`promptly.services.openai_service` module provides a service for
interacting with the OpenAI's API through the :class:`.OpenAIService` class.
It handles query construction, API calls, and response extraction.

"""

import logging
import os

from promptly.api.openai_eval import completion

logger = logging.getLogger(__name__)


class OpenAIService:
    """
    A service class for interacting with the OpenAI API.

    Attributes:
        model (str): The model to be used by OpenAI. Default is
            ``gpt-3.5-turbo`` or can be set via the environment variable
            ``OPENAI_MODEL``. For details on available models, see
            the `OpenAI API documentation
            <https://platform.openai.com/docs/models/overview>`_.
    """

    def __init__(self):
        """Initialize the OpenAIService with the specified model."""
        self.model = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')

    def get_response(self, query: str) -> str:
        """
        Send a query to OpenAI and return the model's response.

        The method constructs a message from the query, sends it to OpenAI for
        processing, and extracts the response from OpenAI's reply.

        :param query: The user's message.
        :type query: str
        :return: The model's response.
        :rtype: str
        """
        response = completion(
            messages=[{'role': 'user', 'content': query}],
            model=self.model,
            temperature=0,
            max_tokens=2048,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        logger.debug('OpenAI response: {}', response)
        return response['choices'][0]['message']['content']
