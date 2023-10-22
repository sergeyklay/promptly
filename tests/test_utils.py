# This file is part of the Promptly.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Module for Utils testing."""

import pytest

from promptly.utils import strtobool, threaded_execute, try_parse_int


@pytest.mark.parametrize(
    'value',
    ('y', 'Y', 'yes', 't', 'True', 'ON', 1,))
def test_should_return_true(value):
    assert strtobool(value) is True


@pytest.mark.parametrize(
    'value',
    ('n', 'N', 'no', 'f', 'False', 'OFF', 0))
def test_should_return_false(value):
    assert strtobool(value) is False


def test_should_raise_value_error():
    with pytest.raises(ValueError):
        strtobool('FOO_BAR')


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


@pytest.mark.parametrize(
    'provided, expected',
    [
        ('42', 42),
        ('0', 0),
        ('-1', -1),
        ('abc', None),
        (None, None),
        ('', None),
        ('3.14', None),  # float string
    ]
)
def test_try_parse_int(provided, expected):
    assert try_parse_int(provided) == expected
