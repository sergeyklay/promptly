# This file is part of the Promptly.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Module for seeding the database with fake data.

This module is part of the Promptly application and provides functionality for
seeding the database with fake data. The data is generated using the Faker
library, and is inserted into the database using the SQLAlchemy ORM.
"""

import random
import sys
from contextlib import contextmanager

from faker import Faker
from faker.providers import company, lorem, python
from sqlalchemy.exc import IntegrityError

from promptly.models import ChatEntry, db


def seed():
    """Init the seeding process by seeding chat and chat entry entities."""
    chats = seed_entities(create_chats())
    seed_chat_entries(chats)


def create_chats(chats_count=None):
    """Generate a specified number of fake chat data."""
    fake = Faker()

    fake.add_provider(company)
    fake.add_provider(lorem)
    fake.add_provider(python)

    if chats_count is None:
        chats_count = 15

    seed_data = {
        'model': 'Chat',
        'table': 'chats',
        'data': [],
    }

    while len(seed_data['data']) < chats_count:
        seed_data['data'].append({
            'title': fake.company(),
            'teaser': fake.paragraph(nb_sentences=1),
        })

    return seed_data


def seed_chat_entries(chats):
    """
    Seed the chat entries table with a specified chats.

    :param chats: A list of chats to which the chat entries will be associated.
    :type chats: list
    """
    fake = Faker()

    fake.add_provider(company)
    fake.add_provider(lorem)
    fake.add_provider(python)

    entries_count = 500
    created = 0

    while created < entries_count:
        try:
            chat_entry = ChatEntry.create(
                content=fake.paragraph(nb_sentences=2),
                chat=random.choice(chats),
            )
            db.session.add(chat_entry)
            db.session.commit()
            created += 1
        except IntegrityError:
            db.session.rollback()


def seed_entities(entry):
    """
    Seed a single table based on the provided entry data.

    :param dict entry: A dictionary containing the model name, table name, and
        a list of dictionaries where each dictionary represents a row to be
        inserted into the table.
    :return: A list of instances that have been added to the session.
    :rtype: list
    """
    entities = []
    table, model, table_data = get_entry_data(entry)
    model_class = get_model_class(model, table)
    for row_data in table_data:
        entities.append(seed_row(model_class, table, row_data))

    return entities


def get_entry_data(entry):
    """Extract data from entry."""
    return entry.pop('table'), entry.pop('model'), entry.pop('data')


def get_model_class(model, table):
    """
    Retrieve the model class based on the provided model name.

    :param str model: The name of the model class to retrieve.
    :param str table: The name of the table associated with the model, used for
        error messaging.
    :return: The model class if found, or exits the program with an error
        message if not found.
    :rtype: flask_sqlalchemy.model.DefaultMeta
    :raises SystemExit: If the model class cannot be found.
    """
    model_class = getattr(sys.modules['promptly.models'], model, None)
    print(f'model_class: {model_class} type: {type(model_class)}')
    if not model_class:
        error_exit(f'Failed to find model class for {table}', 1)
    return model_class


# pylint: disable=inconsistent-return-statements
def seed_row(model_class, table, row_data):
    """
    Insert a single row into the specified table based on the provided data.

    :param model_class: The SQLAlchemy model class for the table.
    :type model_class: flask_sqlalchemy.model.DefaultMeta
    :param str table: The name of the table.
    :param dict row_data: The data for the row to be inserted.
    :return: The instance of the model class representing the inserted row.
    :rtype: sqlalchemy.orm.state.InstanceState|None

    :raises TypeError: If there's a type error when attempting to create a new
        model instance.
    :raises sqlalchemy.exc.IntegrityError: If there's an integrity error when
        attempting to insert the row into the table.

    """
    try:
        instance = model_class().create(**row_data)
        with db_session() as session:
            session.add(instance)
            return instance
    except TypeError:
        error_exit(f'''
        Failed to use {row_data} to insert into "{table}" table
        '''.strip(), 1)
    except IntegrityError:
        error_exit(f'Failed to insert {row_data} into {table}', 1)


@contextmanager
def db_session():
    """Provide a transactional scope around a series of operations."""
    session = db.session()
    try:
        yield session
        session.commit()
    except IntegrityError as e:
        session.rollback()
        raise e
    finally:
        session.close()


def error_exit(message, exit_code):
    """Write error message to stderr and exit."""
    sys.stderr.write(message + '\n')
    sys.stderr.flush()
    sys.exit(exit_code)
