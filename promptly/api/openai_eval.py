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
def completion(*args, **kwargs) -> str:
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
    :raises Exception: ``openai.error.OpenAIError`` if there is an error in the
        API request.
    """
    # For details see https://platform.openai.com/docs/api-reference
    result = threaded_execute(openai.ChatCompletion.create, *args, **kwargs)
    if 'error' in result:
        logger.warning(result)
        raise openai.error.APIError(result['error'])
    return result
