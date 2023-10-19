# This file is part of the Promptly.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""The Chat models package for the application.

This module contains the SQLAlchemy models for handling chat conversations
within the application, including the :class:`.Chat` and
:class:`.ChatEntry` models.

.. note:: This module assumes the existence of a SQLAlchemy database session,
          and the necessary base mixins for identity and timestamp handling.
"""

from typing import List

import sqlalchemy as sa
from sqlalchemy import orm as so

from .base import BaseMixin, db, IdentityMixin, TimestampMixin


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

    teaser: so.Mapped[str] = so.mapped_column(
        sa.String(128),
        nullable=False,
    )

    entry: so.Mapped[List['ChatEntry']] = so.relationship(
        back_populates='chat',
    )


class ChatEntry(BaseMixin, IdentityMixin, TimestampMixin, db.Model):
    """ChatEntry Model.

    Represents a single message in a Chat.
    """

    __tablename__ = 'chat_entries'

    content: so.Mapped[str] = so.mapped_column(
        sa.Text,
        nullable=False,
    )

    chat_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey('chats.id'),
        nullable=False
    )

    chat: so.Mapped['Chat'] = so.relationship(
        back_populates='entry',
    )
