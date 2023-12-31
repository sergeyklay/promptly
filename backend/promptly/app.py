# This file is part of the Promptly.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""
Manage the application creation and configuration process.
----------------------------------------------------------
"""

import os

from flask import Flask


def create_app(config=None) -> Flask:
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, static_url_path='')

    configure_app(app, config)
    configure_extensions(app)
    configure_context_processors(app)
    configure_blueprints(app)

    return app


def load_env_vars(base_path: str):
    """Load the current dotenv as system environment variable."""
    dotenv_path = os.path.join(base_path, '.env')

    from dotenv import load_dotenv
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path=dotenv_path)


def configure_app(app: Flask, config_name=None):
    """Configure application."""
    from promptly.config import config, Config

    # Use the default config and override it afterward
    app.config.from_object(config['default'])

    if config is not None:
        # Config name as a string
        if isinstance(config_name, str) and config_name in config:
            app.config.from_object(config[config_name])
            config[config_name].init_app(app)
        # Config as an object
        else:
            app.config.from_object(config_name)
            if isinstance(config_name, Config):
                config_name.init_app(app)

    # Update config from environment variable (if any). This environment
    # variable can be set in the shell before starting the server:
    #
    #    $ export PROMPTLY_SETTINGS="/var/www/server/settings.cfg"
    #    $ flask --app runner:app run
    #
    # The configuration files themselves are actual Python files.  Only values
    # in uppercase are actually stored in the config object later on. So make
    # sure to use uppercase letters for your config keys.
    app.config.from_envvar('PROMPTLY_SETTINGS', silent=True)


def configure_extensions(app: Flask):
    """Configure extensions for the application."""
    from promptly.models import db
    from flask_migrate import Migrate, upgrade

    # Flask-SQLAlchemy
    db.init_app(app)

    # Flask-Migrate
    migrate = Migrate()
    migrate.init_app(app, db)

    @app.cli.command()
    def deploy():
        """Run deployment tasks."""
        # Migrate database to latest revision.
        upgrade()

    @app.cli.command()
    def seed():
        """Add seed data to the database."""
        from tests.seeder import seed
        seed()


def configure_context_processors(app: Flask):
    """Configure the context processors."""
    import inspect
    from promptly import models

    ctx = {}
    for pair in inspect.getmembers(models, inspect.isclass):
        # Do not reimport non-project models
        if pair[1].__module__ == models.__name__:
            ctx[pair[0]] = pair[1]

    @app.shell_context_processor
    def make_shell_context():
        """Configure flask shell command to autoimport app objects."""
        return {
            'app': app,
            'db': models.db,
            **ctx
        }


def configure_blueprints(app: Flask):
    """Configure blueprints for the application."""
    # main blueprint registration
    from promptly.main import main_bp
    app.register_blueprint(main_bp)

    # chat blueprint registration
    from promptly.chat import chat_bp
    app.register_blueprint(chat_bp)

    # api blueprint registration
    from promptly.api import api_bp
    app.register_blueprint(api_bp)
