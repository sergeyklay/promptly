# This file is part of the Promptly.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Main module for the Promptly Flask application.

This module contains the general routes and views for the main section of the
Promptly application, including the homepage and maintenance mode handling.
"""

import os

from flask import abort, render_template

from promptly.utils import strtobool
from . import main


@main.before_app_request
def maintained():
    """Check if the application is in maintenance mode.

    This function is called before each request to the application.
    If the environment variable 'PROMPTLY_MAINTENANCE_MODE' is set to a truthy
    value, the function will abort the request with a 503 Service Unavailable
    status.

    :raises: 503 Service Unavailable, if the app is in maintenance mode.
    """
    try:
        mode = os.getenv('PROMPTLY_MAINTENANCE_MODE', 'False')
        if strtobool(mode):
            abort(503)
    except ValueError:
        pass


@main.route('/')
def index():
    """Render the homepage of the application.

    :return: The rendered homepage template.
    :rtype: str
    """
    return render_template('home.html')
