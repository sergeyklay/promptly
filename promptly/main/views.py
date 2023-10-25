# This file is part of the Promptly.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""
General routes and views for the application.
---------------------------------------------

This module contains the general routes and views for the main section of the
Promptly application, including the homepage and maintenance mode handling.
"""

import os

from flask import abort, Blueprint, current_app, g

from promptly.utils import strtobool

main_bp = Blueprint('main', __name__)


PROMPTLY_MAINTENANCE_MODE: bool = strtobool(
    os.getenv('PROMPTLY_MAINTENANCE_MODE', 'False'))
"""The maintenance mode flag for the application.

This constant uses ``PROMPTLY_MAINTENANCE_MODE`` environment variable to
determine if the application is in maintenance mode. The value of the
environment variable is converted to a boolean value using the
:func:`.strtobool` function.
"""


@main_bp.before_app_request
def maintained():
    """Check if the application is in maintenance mode.

    This function is called before each request to the application.
    If the environment variable :const:`PROMPTLY_MAINTENANCE_MODE` is set to a
    truthy value, the function will abort the request with a 503 Service
    Unavailable status.

    :raises: HTTPException: 503 Service Unavailable, if the app is in
        maintenance mode.
    """
    try:
        if PROMPTLY_MAINTENANCE_MODE:
            abort(503)
    except ValueError:
        pass


@main_bp.before_request
def setting_globals():
    """Set the debug mode for the application."""
    g.debug_mode = current_app.config['DEBUG']
