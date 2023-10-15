# This file is part of the Promptly.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Models module.

This module initializes the models package and imports necessary modules for
ease of access.

"""

from .base import db  # noqa: F401
from .chat import Chat, ChatEntry  # noqa: F401
from .prompt import Prompt  # noqa: F401
