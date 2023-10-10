# This file is part of the Promptly.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""A module with utility functions."""

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


def strtobool(value: str) -> bool:
    """Convert a string representation of truth to true (1) or false (0).

    String values are case insensitive and can be any of: 'y', 'yes', 't',
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
