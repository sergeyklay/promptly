# This file is part of the Promptly.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Manage the application creation and configuration process."""

import os

from flask import Flask

def create_app(config=None) -> Flask:
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)

    configure_app(app, config)
    configure_blueprints(app)
    configure_extensions(app)
    configure_context_processors(app)

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

    # Use the default config and override it afterwards
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
    #    $ export PROMPTLY_API_SETTINGS="/var/www/server/settings.cfg"
    #    $ flask --app runner:app run
    #
    # The configuration files themselves are actual Python files.  Only values
    # in uppercase are actually stored in the con fig object later on. So make
    # sure to use uppercase letters for your config keys.
    app.config.from_envvar('PRODUCTS_API_SETTINGS', silent=True)

def configure_blueprints(app: Flask):
    """Configure blueprints for the application."""
    # main blueprint registration
    from promptly.main import main as main_bp
    app.register_blueprint(main_bp)


def configure_extensions(app: Flask):
    """Configure extensions for the application."""
    pass


def configure_context_processors(app: Flask):
    """Configure the context processors."""
    pass
