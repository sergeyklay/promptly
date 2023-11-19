# This file is part of the Promptly.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

import pytest

from promptly.services import OpenAIService


@pytest.fixture
def openai_service(monkeypatch):
    def mock_get_response(_ignore, *args):
        return 'Hello, world!'

    monkeypatch.setattr(OpenAIService, 'get_response', mock_get_response)
    return OpenAIService()


def test_conversation(client, openai_service):
    response = client.post(
        '/conversation',
        json={'message': 'Hello, world!', 'chat_id': 1},
    )

    assert response.status_code == 200
    assert response.json['message'] == 'Hello, world!'
    assert response.json['chat_id'] == 1
    assert len(response.json) == 2
