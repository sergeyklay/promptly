# This file is part of the Promptly.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""The Prompt models package for the application.

This module defines the structure and relationship of prompts, rules,
references, criteria, and key insights using SQLAlchemy ORM. It's an integral
part of the data model layer of the application.

"""

from typing import List

import sqlalchemy as sa
from sqlalchemy import orm as so

from .base import BaseMixin, db, IdentityMixin, TimestampMixin


class Prompt(BaseMixin, IdentityMixin, TimestampMixin, db.Model):
    """Represent a prompt in the system."""

    __tablename__ = 'prompts'

    prompt: so.Mapped[str] = so.mapped_column(
        sa.Text,
        nullable=False,
    )

    role: so.Mapped[str] = so.mapped_column(
        sa.String(32),
        nullable=False,
    )

    field: so.Mapped[str] = so.mapped_column(
        sa.String(32),
    )

    task: so.Mapped[str] = so.mapped_column(
        sa.String(128),
        nullable=False,
    )

    task_description: so.Mapped[str] = so.mapped_column(
        sa.Text,
        nullable=False,
    )

    rule: so.Mapped[List['Rule']] = so.relationship(
        back_populates='prompt',
    )

    reference: so.Mapped[List['Reference']] = so.relationship(
        back_populates='prompt',
    )

    criterion: so.Mapped[List['Reference']] = so.relationship(
        back_populates='prompt',
    )


class Rule(BaseMixin, db.Model):
    """Represent a rule associated with a prompt."""

    __tablename__ = 'prompt_rules'

    description: so.Mapped[str] = so.mapped_column(
        sa.Text,
        nullable=False,
    )

    prompt_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey('prompts.id'),
        nullable=False
    )

    prompt: so.Mapped['Prompt'] = so.relationship(
        back_populates='rule',
    )


class Reference(BaseMixin, IdentityMixin, db.Model):
    """Represent a reference associated with a prompt."""

    __tablename__ = 'prompt_references'

    title: so.Mapped[str] = so.mapped_column(
        sa.String(200),
        unique=True,
        index=True,
        nullable=False,
    )

    author: so.Mapped[str] = so.mapped_column(
        sa.String(100),
        unique=False,
        index=True,
        nullable=False,
    )

    year: so.Mapped[int] = so.mapped_column(
        sa.Integer,
        nullable=False
    )

    prompt_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey('prompts.id'),
        nullable=False
    )

    prompt: so.Mapped['Prompt'] = so.relationship(
        back_populates='reference',
    )

    key_insight: so.Mapped[List['KeyInsight']] = so.relationship(
        back_populates='reference',
    )


class KeyInsight(db.Model):
    """Represent a key insight associated with a reference."""

    __tablename__ = 'prompt_reference_key_insights'

    description: so.Mapped[str] = so.mapped_column(
        sa.Text,
        nullable=False,
    )

    reference_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey('prompt_references.id'),
        nullable=False
    )

    reference: so.Mapped['Reference'] = so.relationship(
        back_populates='key_insight',
    )


class Criteria(BaseMixin, IdentityMixin, db.Model):
    """Represent a criterion associated with a prompt."""

    __tablename__ = 'prompt_criteria'

    name: so.Mapped[str] = so.mapped_column(
        sa.String(100),
        unique=True,
        index=True,
        nullable=False,
    )

    description: so.Mapped[str] = so.mapped_column(
        sa.Text,
        nullable=False,
    )

    prompt_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey('prompts.id'),
        nullable=False
    )

    prompt: so.Mapped['Prompt'] = so.relationship(
        back_populates='criterion',
    )
