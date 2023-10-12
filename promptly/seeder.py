# This file is part of the Promptly.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""This module is responsible for seeding the database with fake data."""

import signal
import sys

from sqlalchemy.exc import IntegrityError

from promptly.app import db
from .models import Chat


def seed_all():
    """Seeds all fake data to the database."""
    seed_chat_history()


def seed_chat_history():
    """Seeds all chat history to the database."""
    chats = [
        {
            'title': 'GANs Discussion',
            'teaser': 'Do you think GANs are overhyped?...',
        },
        {
            'title': 'NLP Enthusiasts',
            'teaser': 'Is the Transformer still cool?...',
        },
        {
            'title': 'Reinforcement Learning',
            'teaser': 'Heard about the new OpenAI algo?..',
        },
        {
            'title': 'Quantum Computing',
            'teaser': 'Is it the future or just a fad?...',
        },
        {
            'title': 'Climate Change Debate',
            'teaser': 'What are the actionable steps?...',
        },
        {
            'title': 'SpaceX Fans',
            'teaser': 'Next launch predictions?...',
        },
        {
            'title': 'Python vs Rust',
            'teaser': "Which one's actually better?...",
        },
        {
            'title': 'CRISPR Talks',
            'teaser': 'Ethical concerns anyone?...',
        },
        {
            'title': 'AI in Healthcare',
            'teaser': 'How soon is the revolution?...',
        },
        {
            'title': 'Cybersecurity 101',
            'teaser': 'Best practices for 2023?...',
        },
        {
            'title': 'Big Data Analysis',
            'teaser': 'Is Hadoop still relevant?...',
        },
        {
            'title': 'Serverless Architecture',
            'teaser': 'When not to go serverless?...',
        },
        {
            'title': 'Evolution Theory',
            'teaser': 'How accurate are the timelines?...',
        },
        {
            'title': 'Particle Physics',
            'teaser': 'Is the Higgs Boson overrated?...',
        },
        {
            'title': 'Dark Matter Research',
            'teaser': 'Latest breakthroughs?...',
        },
    ]

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
