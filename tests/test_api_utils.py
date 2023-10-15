# This file is part of the Promptly.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Module for :promptly.api.utils testing."""

from promptly.api.utils import threaded_execute


def test_threaded_execute_success():
    def fast_func():
        return 'Success'

    result = threaded_execute(fast_func)
    assert result == 'Success'


def test_threaded_execute_non_timeout_exception():
    def failing_func():
        raise ValueError('Something went wrong')

    try:
        threaded_execute(failing_func)
    except ValueError as e:
        assert str(e) == 'Something went wrong'
