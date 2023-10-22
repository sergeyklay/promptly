# This file is part of the Promptly.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""
Application models and convenient imports.
==========================================

The :mod:`promptly.models` module provides application models and imports
necessary modules for ease of access.

"""

from .base import db  # noqa: F401
from .chat import *  # noqa: F401, F403
from .prompt import *  # noqa: F401, F403
