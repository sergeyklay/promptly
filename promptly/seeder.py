# This file is part of the Promptly.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Module for seeding the database with fake data.

This module contains functions necessary for loading fake data from
a JSON file and seeding it into the database using SQLAlchemy ORM.
"""

import json
import os
import sys
from contextlib import contextmanager

from sqlalchemy.exc import IntegrityError

from promptly.models import db


def seed_all():
    """Seed all fake data to the database.

    This function reads a JSON file named ``fake-data.json`` located in
    the ``fixtures`` directory relative to this module's directory. Each
    entry in the JSON file should be a dictionary with three keys:
    'table', 'model', and 'data'. The 'table' value should be the name
    of the database table, 'model' should be the name of the SQLAlchemy
    model class, and 'data' should be a list of dictionaries where each
    dictionary represents a row to be inserted into the table.

    Usage::

        An example ``fake-data.json`` file might look like this:

        [
            {
                "table": "chats",
                "model": "Chat",
                "data": [
                    {"title": "GANs Discussion", "teaser": "..."},
                    {"title": "NLP Enthusiasts", "teaser": "..."}
                ]
            }
        ]

    :raises SystemExit:
        1. If the ``fake-data.json`` file does not exist.
        2. If failed to parse JSON data from the ``fake-data.json`` file.
        3. If a necessary key ('table', 'model', or 'data') is missing in
           the JSON data.
        4. If the model class cannot be found.
        5. If there is a TypeError when attempting to create a new model
           instance.
    """
    file_path = get_file_path('fixtures', 'fake-data.json')
    json_data = load_json_data(file_path)

    for entry in json_data:
        seed_entry(entry)


def get_file_path(*path_parts):
    """Construct file path."""
    return os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        *path_parts
    )


def load_json_data(filename):
    """Load JSON data from a file.

    This function reads a JSON file and returns the parsed data.

    :param str filename: The name of the file to read.
    :return: The parsed JSON data.
    :rtype: dict
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        error_exit(f'Failed to parse JSON data from {filename}', 1)
        return None  # to mute R1710


def seed_entry(entry):
    """Seed a single entry to the database."""
    try:
        table, model, table_data = get_entry_data(entry)
        model_class = get_model_class(model, table)
        for row_data in table_data:
            seed_row(model_class, table, row_data)
    except KeyError:
        error_exit('Invalid JSON data', 1)


def get_entry_data(entry):
    """Extract data from entry."""
    return entry.pop('table'), entry.pop('model'), entry.pop('data')


def get_model_class(model, table):
    """Get the model class from the model name."""
    model_class = getattr(sys.modules['promptly.models'], model, None)
    if not model_class:
        error_exit(f'Failed to find model class for {table}', 1)
    return model_class


def seed_row(model_class, table, row_data):
    """Seed a single row to the database."""
    try:
        instance = model_class().create(**row_data)
        with db_session() as session:
            session.add(instance)
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
