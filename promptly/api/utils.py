# This file is part of the Promptly.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""This module provides a simplified interface to the OpenAI API."""

import logging
import os

import openai


logger = logging.getLogger(__name__)


def completion(*args, **kwargs) -> str:
    """Generates a text completion using the OpenAI API.

    Any arguments or keyword arguments are forwarded directly to the
    `openai.ChatCompletion.create` method. The OpenAI API key is read from the
    `OPENAI_API_KEY` environment variable.

    Parameters:
        *args: Variable-length argument list.
        **kwargs: Arbitrary keyword arguments.

    Returns:
        str: The generated text completion.

    Raises:
        openai.error.APIError: If there is an error in the API request.
    """
    openai.api_key = os.getenv('OPENAI_API_KEY')
    result = openai.ChatCompletion.create(*args, **kwargs)
    if 'error' in result:
        logger.warning(result)
        raise openai.error.APIError(result["error"])
    return result
