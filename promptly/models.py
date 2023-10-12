# This file is part of the Promptly.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""ORM models and helper functions for the application."""

from datetime import datetime
from typing import List

import sqlalchemy as sa
from sqlalchemy import orm as so
from sqlalchemy.sql import func

# TODO: Sortout with the "bug" bellow
# pylint: disable=cyclic-import
from .app import db


class IdentityMixin:
    """Mixin class to add identity fields to a SQLAlchemy model."""

    id: so.Mapped[int] = so.mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    def __repr__(self):
        """Returns the object representation in string format."""
        return f'<{self.__class__.__name__} id={self.id!r}>'


class TimestampMixin:
    """Mixin class to add timestamp fields to a SQLAlchemy model."""

    created_at: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime(timezone=True),
        nullable=False,
        index=True,
        server_default=func.now(),
    )

    updated_at: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime(timezone=True),
        nullable=False,
        index=True,
        onupdate=func.now(),
        server_default=func.now(),
    )

    def last_modified(self) -> str:
        """Get the time of the last model update."""
        modified = self.updated_at or self.created_at or datetime.utcnow()
        return modified.strftime('%a, %d %b %Y %H:%M:%S GMT')


class Chat(IdentityMixin, TimestampMixin, db.Model):
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


class ChatEntry(IdentityMixin, TimestampMixin, db.Model):
    """ChatEntry Model.

    Represents a single message in a Chat.
    """

    __tablename__ = 'chat_entries'

    teaser: so.Mapped[str] = so.mapped_column(
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
