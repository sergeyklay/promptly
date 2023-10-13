# This file is part of the Promptly.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Module for seeder testing."""

import pytest

from promptly.seeder import load_json_data


@pytest.fixture
def mock_open(mocker):
    return mocker.patch('builtins.open', mocker.mock_open(read_data='{"foo": "bar"}'))


@pytest.fixture
def mock_json_load(mocker):
    return mocker.patch('json.load', return_value={"foo": "bar"})


def test_load_json_data(mock_open, mock_json_load):
    filename = 'fake-data.json'
    result = load_json_data(filename)
    mock_open.assert_called_once_with(filename, 'r', encoding='utf-8')
    mock_json_load.assert_called_once()
    assert result == {"foo": "bar"}