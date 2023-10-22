# This file is part of the Promptly.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

from promptly.models import Chat


def test_chat_index_without_cookie(client):
    response = client.get('/')
    assert response.status_code == 200


def test_chat_index_with_cookie(client):
    chat_id = Chat.create_new_chat().id
    client.set_cookie(
        key='chat_id',
        value=str(chat_id),
        domain='localhost',
    )

    response = client.get('/')
    assert response.status_code == 302


def test_chat(client):
    chat_id = Chat.create_new_chat().id
    response = client.get(f'/{chat_id}')
    assert response.status_code == 200


def test_history(client):
    response = client.get('/history')
    assert response.status_code == 200
