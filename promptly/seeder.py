# This file is part of the Promptly.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""This module is responsible for seeding the database with fake data."""

import json
import os
import signal
import sys

from sqlalchemy.exc import IntegrityError

from promptly.app import db
from .models import Chat


def seed_all():
    """Seeds all fake data to the database."""
    seed_chat_history()


def load_json_data(filename):
    """Load JSON data from a file."""
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)


def seed_chat_history():
    """Seeds all chat history to the database."""
    file_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        'migrations',
        'seed-chats-history.json'
    )

    if not os.path.exists(file_path):
        sys.stderr.write(f'JSON file not found at {file_path}\n')
        sys.stderr.flush()
        sys.exit(2)  # No such file or directory

    chats = load_json_data(file_path)
    for index, chat_data in enumerate(chats):
        try:
            chat = Chat(**chat_data)
            db.session.add(chat)
            db.session.commit()
            chats[index] = chat
        except KeyboardInterrupt:  # the user hit control-C
            sys.stderr.write('\nReceived keyboard interrupt, terminating...\n')
            sys.stderr.flush()

            # Control-C is fatal error signal 2, for more see
            # https://tldp.org/LDP/abs/html/exitcodes.html
            sys.exit(128 + signal.SIGINT)
        except IntegrityError:
            db.session.rollback()
