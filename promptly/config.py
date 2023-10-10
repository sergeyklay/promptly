# This file is part of the Promptly.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Configuration module for the application.

Provides the base configuration and specific configurations for development,
testing, and production. Includes the 'config' dictionary for easy switching
between different configurations.

"""

import os


class Config:
    """Base config, uses staging database server."""
    TESTING = False
    DEBUG = False
    BASE_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    @staticmethod
    def init_app(app):
        """Initialize the application with configuration-specific settings.

        This method takes a Flask application instance and configures it
        with settings defined in the configuration object.

        :param app: The Flask application instance.
        :type app: Flask

        Usage::

            config_obj = DevelopmentConfig()
            config_obj.init_app(app)

        """


class DevelopmentConfig(Config):
    """Uses development database server."""
    DEBUG = True


class TestingConfig(Config):
    """Uses in-memory database server."""
    TESTING = True


class ProductionConfig(Config):
    """Uses production database server."""


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}
