# This file is part of the Promptly.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""
The template filters module for the chat.
-----------------------------------------
"""

from datetime import datetime, timedelta


def human_readable_date(value: datetime) -> str:
    """Convert a datetime object to a human-readable date.

    This function takes a datetime object and returns a string that represents
    a more human-readable and context-sensitive representation of the time. The
    output will be one of the following:

    - ``Today``
    - ``Yesterday``
    - ``Previous 7 Days``
    - ``Previous 30 Days``
    - ``Previous Year``
    - ``Older``

    :param datetime.datetime value: The datetime object to be converted.
    :return: A string representing the human-readable date.
    :rtype: str
    """
    today = datetime.now().date()
    date_val = str(value).split(' ', maxsplit=1)[0]
    value_date = datetime.strptime(date_val, '%Y-%m-%d').date()

    time_ranges = [
        (0, 'Today'),
        (1, 'Yesterday'),
        (7, 'Previous 7 Days'),
        (30, 'Previous 30 Days'),
        (365, 'Previous Year')
    ]

    for days, label in time_ranges:
        if today - timedelta(days=days) <= value_date <= today:
            return label

    return 'Older'
