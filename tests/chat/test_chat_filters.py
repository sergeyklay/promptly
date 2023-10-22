# This file is part of the Promptly.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

from datetime import datetime, timedelta

import pytest

from promptly.chat.template_filters import human_readable_date


@pytest.mark.parametrize(
    'provided, expected',
    [
        (datetime.now().date(), 'Today'),
        ((datetime.now() - timedelta(days=1)).date(), 'Yesterday'),
        ((datetime.now() - timedelta(days=6)).date(), 'Previous 7 Days'),
        ((datetime.now() - timedelta(days=29)).date(), 'Previous 30 Days'),
        ((datetime.now() - timedelta(days=364)).date(), 'Previous Year'),
        ((datetime.now() - timedelta(days=366)).date(), 'Older'),
    ]
)
def test_human_readable_date(provided, expected):
    """Test the human_readable_date filter."""
    value = datetime.combine(provided, datetime.min.time())
    assert human_readable_date(value) == expected
