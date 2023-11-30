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
        openai.APIConnectionError,
        openai.APITimeoutError,
        openai.InternalServerError,
        openai.RateLimitError,
    ),
    max_value=60,
    factor=1.5,
)
def completion(*args, **kwargs) -> Dict[str, Any]:
    """Generates a text completion using the OpenAI API.

    This function uses an exponential backoff strategy to handle the following
    exceptions:

    - ``openai.APIConnectionError``
    - ``openai.APITimeoutError``
    - ``openai.InternalServerError``
    - ``openai.RateLimitError``

    The backoff delay starts at 1 second and increases by a factor of 1.5 with
    each retry, capping at a maximum delay of 60 seconds between retries.

    Any arguments or keyword arguments are forwarded directly to the
    ``openai.resources.chat.completions.Completions.create`` method. The OpenAI
    API key is read from the ``OPENAI_API_KEY`` environment variable by any
    import openai's ``__init__.py`` file.

    :param args: Variable-length argument list.
    :param kwargs: Arbitrary keyword arguments.
    :return: The generated text completion.
    :rtype: dict
    :raises Exception: ``openai.OpenAIError`` if there is an error in the
        API request.
    """
    # For details see https://platform.openai.com/docs/api-reference
    client = openai.OpenAI()
    result = threaded_execute(client.chat.completions.create, *args, **kwargs)
    # FIXME: This API was changed in openai-python >= 0.28.1 and now it not
    # returns a dict, but a Completions object.  We need to update this code
    if 'error' in result:
        logger.warning(result)
        raise openai.OpenAIError(result['error'])

    # Typically, the response is a single message, but it can be multiple
    # messages if the model is configured to generate multiple messages.
    #
    # Example response:
    # {
    #   'id': 'chatcmpl-8CPG5CegoglqliSS1kD6E7zCXjzXO',
    #   'object': 'chat.completion',
    #   'created': 1697967721,
    #   'model': 'gpt-3.5-turbo-16k-061',
    #   'system_fingerprint': 'fp_44709d6fcb',
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
