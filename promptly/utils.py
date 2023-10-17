# This file is part of the Promptly.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""A module with utility functions."""

import concurrent
import logging
from os import environ as env

_BOOL_MAP = {
    # True
    'y': True,
    'yes': True,
    't': True,
    'true': True,
    'on': True,
    '1': True,

    # False
    'n': False,
    'no': False,
    'f': False,
    'false': False,
    'off': False,
    '0': False
}

PROMPTLY_THREAD_TIMEOUT = float(env.get('PROMPTLY_THREAD_TIMEOUT', '60'))

logger = logging.getLogger(__name__)


def strtobool(value: str) -> bool:
    """Convert a string representation of truth to true (1) or false (0).

    String values are case-insensitive and can be any of: 'y', 'yes', 't',
    'true', 'on', '1', 'n', 'no', 'f', 'false', 'off', '0'.

    :param value: The string to convert to a boolean.
    :type value: str
    :return: The boolean representation of the string.
    :rtype: bool
    :raises ValueError: If the value does not represent a truth value.

    Usage::

        bool_value = strtobool('True')
        # bool_value is now True

    """
    try:
        return _BOOL_MAP[str(value).lower()]
    except KeyError as exc:
        raise ValueError(f'''"{value}" is not a valid bool value''') from exc


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
    :raises: Any exceptions raised by ``func``, except for
        ``concurrent.futures.TimeoutError`` which is caught and logged.
    """
    while True:
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(func, *args, **kwargs)
            try:
                return future.result(timeout=timeout)
            except concurrent.futures.TimeoutError as exc:
                logger.warning(exc)
                continue
