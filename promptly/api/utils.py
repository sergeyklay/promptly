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
from concurrent.futures import ThreadPoolExecutor, TimeoutError


logger = logging.getLogger(__name__)

PROMPTLY_THREAD_TIMEOUT = float(os.environ.get('PROMPTLY_THREAD_TIMEOUT', '60'))


def threaded_execute(func, *args, timeout=PROMPTLY_THREAD_TIMEOUT, **kwargs):
    """Worker thread for timed request execution.

    This function will continuously attempt to execute ``func`` until it
    succeeds without encountering a :class:`concurrent.futures.TimeoutError`.
    If a :class:`concurrent.futures.TimeoutError` occurs, a warning is logged,
    and the function is re-invoked with the same arguments.

    :param func: The function to be executed.
    :param args: Positional arguments to pass to ``func``.
    :param timeout: The time, in seconds, within which ``func`` should complete
        execution. Defaults to ``PROMPTLY_THREAD_TIMEOUT``.
    :param kwargs: Keyword arguments to pass to ``func``.
    :return: The return value of ``func``, if it completes successfully within
        the allotted time.
    :raises: Any exceptions raised by ``func``, except for TimeoutError which is
        caught and logged.
    """
    while True:
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(func, *args, **kwargs)
            try:
                return future.result(timeout=timeout)
            except TimeoutError as exc:
                logger.warning(exc)
                continue


def completion(*args, **kwargs) -> str:
    """Generates a text completion using the OpenAI API.

    Any arguments or keyword arguments are forwarded directly to the
    ``openai.ChatCompletion.create`` method. The OpenAI API key is read from the
    ``OPENAI_API_KEY`` environment variable.

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
