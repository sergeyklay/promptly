# This file is part of the Promptly.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Module for seeder testing."""

import json

import pytest

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
