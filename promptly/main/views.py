# This file is part of the Promptly.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""The routes module for the application."""

import os

from flask import abort
from flask import render_template

from promptly.utils import strtobool
from . import main


@main.before_app_request
def maintained():
    try:
        maintenance = strtobool(os.getenv('PROMPTLY_MAINTENANCE_MODE', 'False'))
        if bool(maintenance):
            abort(503)
    except ValueError:
        pass


@main.route('/')
def index():
    return render_template('home.html')
