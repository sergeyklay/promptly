# This file is part of the Promptly.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

import os

import pytest
from flask_migrate import upgrade

from promptly.app import create_app


@pytest.fixture()
def project_root() -> str:
    """Get actual project root path."""
    return os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))
    )


@pytest.fixture()
def app(project_root: str):
    """An application for the tests."""
    app_instance = create_app('testing')
    app_instance.config.update({
        'TESTING': True,
    })
    with app_instance.app_context():
        upgrade(os.path.join(project_root, 'migrations'))
        yield app_instance


@pytest.fixture()
def client(app):
    """A Flask test client."""
    with app.test_client() as client:
        yield client


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
