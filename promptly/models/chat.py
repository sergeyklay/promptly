# This file is part of the Promptly.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""
The Chat models package for the application.
--------------------------------------------

This module contains the SQLAlchemy models for handling chat conversations
within the application, including the :class:`.Chat` and
:class:`.ChatEntry` models.

.. note:: This module assumes the existence of a SQLAlchemy database session,
          and the necessary base mixins for identity and timestamp handling.
"""

from enum import Enum
from typing import List

import sqlalchemy as sa
from sqlalchemy import orm as so

from .base import BaseMixin, db, IdentityMixin, TimestampMixin

__all__ = ['Chat', 'ChatEntry']


class Chat(BaseMixin, IdentityMixin, TimestampMixin, db.Model):
    """Chat Model.

    Represents a chat conversation in the application.
    """

    __tablename__ = 'chats'

    title: so.Mapped[str] = so.mapped_column(
        sa.String(64),
        unique=False,
        index=True,
        nullable=False,
    )

    entry: so.Mapped[List['ChatEntry']] = so.relationship(
        back_populates='chat',
    )

    def teaser(self, length=None) -> str:
        """Return a teaser for the chat."""
        if not self.entry:
            return ''

        first_entry = min(self.entry, key=lambda x: x.created_at)
        length = length or 150

        if len(first_entry.content) > length:
            return first_entry.content[:length - 3] + '...'

        return first_entry.content[:length]

    @classmethod
    def create_new_chat(cls, title=None):
        """Create a new chat and return the new chat."""
        title = title or 'New chat'
        new_chat = cls.create(title=title)
        new_chat.save()
        return new_chat


class ChatEntry(BaseMixin, IdentityMixin, TimestampMixin, db.Model):
    """ChatEntry Model.

    Represents a single message in a Chat.
    """
    class Role(Enum):
        """Represents the role of a :class:`.ChatEntry`."""

        USER = 'user'
        ASSISTANT = 'assistant'

        def __str__(self) -> str:
            """Get a string representation of this role.

            :return: The name of this role.
            :rtype: str
            """
            return self.name.strip().lower()

    __tablename__ = 'chat_entries'

    content: so.Mapped[str] = so.mapped_column(
        sa.Text,
        nullable=False,
    )

    chat_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey('chats.id'),
        nullable=False
    )

    role: so.Mapped[Role] = so.mapped_column(
        sa.Enum(
            Role,
            name='role_types',
            values_callable=lambda obj: [str(item.value) for item in obj]
        ),
        nullable=False,
    )

    chat: so.Mapped['Chat'] = so.relationship(
        back_populates='entry',
    )
