# This file is part of the Promptly.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Module for seeder testing."""

import json

import pytest

from promptly.seeder import load_json_data


MOCK_DATA = [
    {
        "model": "Chat",
        "table": "chats",
        "data": [
            {
                "title": "GANs Discussion",
                "teaser": "Do you think GANs are overhyped?..."
            },
            {
                "title": "NLP Enthusiasts",
                "teaser": "Is the Transformer still cool?..."
            }
        ]
    }
]


@pytest.fixture
def mock_open(mocker):
    return mocker.patch(
        'builtins.open', mocker.mock_open(read_data=json.dumps(MOCK_DATA)))


@pytest.fixture
def mock_json_load(mocker):
    return mocker.patch('json.load', return_value=MOCK_DATA)


def test_load_json_data(mock_open, mock_json_load):
    filename = 'fake-data.json'
    result = load_json_data(filename)
    mock_open.assert_called_once_with(filename, 'r', encoding='utf-8')
    mock_json_load.assert_called_once()
    assert result == MOCK_DATA
