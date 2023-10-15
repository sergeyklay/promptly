# This file is part of the Promptly.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""This module initializes the models package and imports necessary modules for
ease of access.

Imports
-------
- `promptly.models.chat.Chat` and `promptly.models.chat.ChatEntry` from `promptly.models.chat`: These are the primary models for handling chat conversations.
- `promptly.models.base.db` from `promptly.models.base.base`: SQLAlchemy database instance for use throughout the application.

"""

from .chat import Chat, ChatEntry
from .base import db
