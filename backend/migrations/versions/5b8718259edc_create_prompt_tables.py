# This file is part of the Promptly.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Create prompt tables

Revision ID: 5b8718259edc
Revises: b943c7643aa5
Create Date: 2023-10-16 11:00:49.699946

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '5b8718259edc'
down_revision = 'b943c7643aa5'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'prompts',
        sa.Column('prompt', sa.Text(), nullable=False),
        sa.Column('role', sa.String(length=32), nullable=False),
        sa.Column('field', sa.String(length=32), nullable=False),
        sa.Column('task', sa.String(length=128), nullable=False),
        sa.Column('task_description', sa.Text(), nullable=False),
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('(CURRENT_TIMESTAMP)'),
            nullable=False
        ),
        sa.Column(
            'updated_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('(CURRENT_TIMESTAMP)'),
            nullable=False
        ),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_prompts'))
    )
    with op.batch_alter_table('prompts', schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f('ix_prompts_created_at'),
            ['created_at'],
            unique=False
        )
        batch_op.create_index(
            batch_op.f('ix_prompts_updated_at'),
            ['updated_at'],
            unique=False
        )

    op.create_table(
        'prompt_criteria',
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('prompt_id', sa.Integer(), nullable=False),
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.ForeignKeyConstraint(
            ['prompt_id'],
            ['prompts.id'],
            name=op.f('fk_prompt_criteria_prompt_id_prompts')
        ),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_prompt_criteria'))
    )
    with op.batch_alter_table('prompt_criteria', schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f('ix_prompt_criteria_name'),
            ['name'],
            unique=True
        )

    op.create_table(
        'prompt_references',
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('author', sa.String(length=100), nullable=False),
        sa.Column('year', sa.Integer(), nullable=False),
        sa.Column('prompt_id', sa.Integer(), nullable=False),
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.ForeignKeyConstraint(
            ['prompt_id'],
            ['prompts.id'],
            name=op.f('fk_prompt_references_prompt_id_prompts')
        ),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_prompt_references'))
    )
    with op.batch_alter_table('prompt_references', schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f('ix_prompt_references_author'),
            ['author'],
            unique=False
        )
        batch_op.create_index(
            batch_op.f('ix_prompt_references_title'),
            ['title'],
            unique=True
        )

    op.create_table(
        'prompt_rules',
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('prompt_id', sa.Integer(), nullable=False),
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.ForeignKeyConstraint(
            ['prompt_id'],
            ['prompts.id'],
            name=op.f('fk_prompt_rules_prompt_id_prompts')
        ),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_prompt_rules'))
    )

    fk = 'fk_prompt_reference_key_insights_reference_id_prompt_references'
    op.create_table(
        'prompt_reference_key_insights',
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('reference_id', sa.Integer(), nullable=False),
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.ForeignKeyConstraint(
            ['reference_id'],
            ['prompt_references.id'],
            name=op.f(fk)
        ),
        sa.PrimaryKeyConstraint(
            'id',
            name=op.f('pk_prompt_reference_key_insights')
        )
    )


def downgrade():
    op.drop_table('prompt_reference_key_insights')
    op.drop_table('prompt_rules')
    with op.batch_alter_table('prompt_references', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_prompt_references_title'))
        batch_op.drop_index(batch_op.f('ix_prompt_references_author'))

    op.drop_table('prompt_references')
    with op.batch_alter_table('prompt_criteria', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_prompt_criteria_name'))

    op.drop_table('prompt_criteria')
    with op.batch_alter_table('prompts', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_prompts_updated_at'))
        batch_op.drop_index(batch_op.f('ix_prompts_created_at'))

    op.drop_table('prompts')
