# This file is part of the Promptly.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""
This module provides a simplified interface to the OpenAI API.
--------------------------------------------------------------
"""

import logging
from typing import Any, Dict

import backoff
import openai

from promptly.utils import threaded_execute

logger = logging.getLogger(__name__)


@backoff.on_exception(
    wait_gen=backoff.expo,
    exception=(
        openai.error.ServiceUnavailableError,
        openai.error.APIError,
        openai.error.RateLimitError,
        openai.error.APIConnectionError,
        openai.error.Timeout,
    ),
    max_value=60,
    factor=1.5,
)
def completion(*args, **kwargs) -> Dict[str, Any]:
    """Generates a text completion using the OpenAI API.

    This function uses an exponential backoff strategy to handle the following
    exceptions:

    - ``openai.error.ServiceUnavailableError``
    - ``openai.error.APIError``
    - ``openai.error.RateLimitError``
    - ``openai.error.APIConnectionError``
    - ``openai.error.Timeout``

    The backoff delay starts at 1 second and increases by a factor of 1.5 with
    each retry, capping at a maximum delay of 60 seconds between retries.

    Any arguments or keyword arguments are forwarded directly to the
    ``openai.ChatCompletion.create`` method. The OpenAI API key is read from
    the ``OPENAI_API_KEY`` environment variable by any import openai's
    ``__init__.py`` file.

    :param args: Variable-length argument list.
    :param kwargs: Arbitrary keyword arguments.
    :return: The generated text completion.
    :rtype: dict
    :raises Exception: ``openai.error.OpenAIError`` if there is an error in the
        API request.
    """
    # For details see https://platform.openai.com/docs/api-reference
    result = threaded_execute(openai.ChatCompletion.create, *args, **kwargs)
    if 'error' in result:
        logger.warning(result)
        raise openai.error.APIError(result['error'])

    # Typically, the response is a single message, but it can be multiple
    # messages if the model is configured to generate multiple messages.
    #
    # Example response:
    # {
    #   'id': 'chatcmpl-8CPG5CegoglqliSS1kD6E7zCXjzXO',
    #   'object': 'chat.completion',
    #   'created': 1697967721,
    #   'model': 'gpt-3.5-turbo-16k-061',
    #   'choices': [
    #     {
    #       'index': 0,
    #       'message': {
    #         'role': 'assistant',
    #         'content': '2 + 2 = 4'
    #       },
    #       'finish_reason': 'stop',
    #     }
    #   ],
    #   'usage': {
    #     'prompt_tokens': 13,
    #     'completion_tokens': 7,
    #     'total_tokens': 20
    #   }
    # }
    return result
