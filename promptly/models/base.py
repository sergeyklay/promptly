# This file is part of the Promptly.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""
Database Models and Utilities Module.
-------------------------------------

This module provides classes and utility functions to work with the database
using SQLAlchemy ORM. It defines a set of mixin classes to extend SQLAlchemy
models with common methods and attributes, along with a configured metadata
object to enforce a naming convention for database constraints.

"""

from datetime import datetime

import sqlalchemy as sa
from flask import abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exists, MetaData, orm as so
from sqlalchemy.sql import func

convention = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s',
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(app=None, metadata=metadata)


class BaseMixin:
    """A base mixin class for application models.

    A base mixin class for ORM models to provide common methods for performing
    database operations. The class provides classmethods for fetching, creating
    records, and instance methods for saving or deleting records from the
    database.
    """

    @classmethod
    def get(cls, entity_id):
        """Fetch a record from the database by its identifier.

        :param entity_id: The identifier of the record to fetch.
        :type entity_id: Any
        :return: The fetched model instance if found, otherwise ``None``.
        """
        return db.session.get(cls, entity_id)

    @classmethod
    def get_or_404(cls, entity_id):
        """Fetch a record from the database by its identifier or abort.

        Fetches a record from the database by its identifier,
        aborts with a 404 error if the record is not found.

        :param entity_id: The identifier of the record to fetch.
        :type entity_id: Any
        :return: The fetched model instance.
        :raises werkzeug.exceptions.HTTPException: If the record is not found.
        """
        rv = cls.get(entity_id)
        if rv is None:
            abort(404, message=f'{cls.__name__} not found')
        return rv

    @classmethod
    def create(cls, **kwargs):
        """Create and save a new model instance.

        Creates a new instance of the model, saves it to the database,
        and returns the created instance.

        :param kwargs: The keyword arguments to initialize the model instance.
        :return: The created model instance.
        """
        instance = cls(**kwargs)
        instance.save()
        return instance

    def save(self):
        """Save the current model to the database.

        :return: None
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete the current model from the database.

        :return: None
        """
        db.session.delete(self)
        db.session.commit()


class IdentityMixin:
    """Mixin class to add identity fields to a SQLAlchemy model."""

    id: so.Mapped[int] = so.mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    def __repr__(self):
        """Returns the object representation in string format.

        :return: Object representation in string format.
        :rtype: str
        """
        return f'<{self.__class__.__name__} id={self.id!r}>'

    @classmethod
    def exists(cls, entity_id: int) -> bool:
        """Check if a record with the given ID exists in the database.

        This is a class method that uses SQLAlchemy's :func:`exists` function
        and the :meth:`scalar` method to efficiently check if a record with the
        specified ID is present in the database. It returns a boolean value
        indicating the presence or absence of the record.

        :param entity_id: The ID of the chat to be checked.
        :type entity_id: int
        :return: True if the chat exists, otherwise False.
        :rtype: bool

        .. note::
            This method assumes an active SQLAlchemy database session.

        """
        return db.session.query(exists().where(cls.id == entity_id)).scalar()


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
        """Get the time of the last model update.

        :return: The time of the last model update.
        :rtype: str
        """
        modified = self.updated_at or self.created_at or datetime.utcnow()
        return modified.strftime('%a, %d %b %Y %H:%M:%S GMT')
