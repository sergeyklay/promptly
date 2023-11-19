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

from promptly.models import db
from promptly.models.chat import ChatEntry

fake = Faker()

fake.add_provider(company)
fake.add_provider(lorem)
fake.add_provider(python)


def seed():
    """Init the seeding process by seeding chat and chat entry entities."""
    chats = seed_entities(create_chats())
    _ = seed_entities(create_chat_entries(chats))

    prompts = seed_entities(create_prompts())
    _ = seed_entities(create_prompt_rules(prompts))
    _ = seed_entities(create_prompt_criteria(prompts))

    references = seed_entities(create_prompt_references(prompts))
    _ = seed_entities(create_prompt_reference_key_insights(references))


def create_chats(entries_count=None):
    """Generate a specified number of fake chat data."""
    if entries_count is None:
        entries_count = 15
    seed_data = {
        'model': 'Chat',
        'table': 'chats',
        'data': [],
    }

    while len(seed_data['data']) < entries_count:
        seed_data['data'].append({'title': fake.sentence(nb_words=3)})

    return seed_data


def create_chat_entries(chats):
    """
    Seed the chat entries table with a specified chats.

    :param chats: A list of chats to which the chat entries will be associated.
    :type chats: list
    """
    entries_count = len(chats) * 10
    seed_data = {
        'model': 'ChatEntry',
        'table': 'chat_entries',
        'data': [],
    }

    while len(seed_data['data']) < entries_count:
        if len(seed_data['data']) % 2 == 0:
            role = ChatEntry.Role.USER
        else:
            role = ChatEntry.Role.ASSISTANT

        seed_data['data'].append({
            'content': fake.paragraph(nb_sentences=4),
            'role': role,
            'chat': random.choice(chats),
        })

    return seed_data


def create_prompts():
    entries_count = 10
    seed_data = {
        'model': 'Prompt',
        'table': 'prompts',
        'data': [],
    }

    while len(seed_data['data']) < entries_count:
        seed_data['data'].append({
            'prompt': fake.paragraph(nb_sentences=1),
            'role': random.choice([
                'Software Engineer',
                'Engineering Manager',
            ]),
            'field': random.choice([
                'Engineering',
                'Product',
            ]),
            'task': random.choice([
                'Create A User Guide',
                'Write A Blog Post',
                'Create A New Feature',

            ]),
            'task_description': fake.paragraph(nb_sentences=2),
        })

    return seed_data


def create_prompt_references(prompts):
    entries_count = len(prompts) * 2
    seed_data = {
        'model': 'Reference',
        'table': 'prompt_references',
        'data': [],
    }

    while len(seed_data['data']) < entries_count:
        seed_data['data'].append({
            'title': fake.paragraph(nb_sentences=1),
            'author': fake.name(),
            'year': fake.year(),
            'prompt': random.choice(prompts),
        })

    return seed_data


def create_prompt_criteria(prompts):
    entries_count = len(prompts) * 8
    seed_data = {
        'model': 'Criterion',
        'table': 'prompt_criteria',
        'data': [],
    }

    while len(seed_data['data']) < entries_count:
        seed_data['data'].append({
            'name': f'{fake.unique.word()} {fake.unique.word()}',
            'description': fake.paragraph(nb_sentences=1),
            'prompt': random.choice(prompts),
        })

    return seed_data


def create_prompt_reference_key_insights(references):
    entries_count = len(references) * 8
    seed_data = {
        'model': 'KeyInsight',
        'table': 'prompt_reference_key_insights',
        'data': [],
    }

    while len(seed_data['data']) < entries_count:
        seed_data['data'].append({
            'description': fake.paragraph(nb_sentences=1),
            'reference': random.choice(references),
        })

    return seed_data


def create_prompt_rules(prompts):
    entries_count = len(prompts) * 6
    seed_data = {
        'model': 'Rule',
        'table': 'prompt_rules',
        'data': [],
    }

    while len(seed_data['data']) < entries_count:
        seed_data['data'].append({
            'description': fake.paragraph(nb_sentences=1),
            'prompt': random.choice(prompts),
        })

    return seed_data


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
