# This file is part of the Promptly.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""The api blueprint module for the application."""

from flask import Blueprint

api = Blueprint('api', __name__)

# TODO: Sortout with the "bug" bellow
# pylint: disable=cyclic-import
from . import views  # noqa: F401, E402
