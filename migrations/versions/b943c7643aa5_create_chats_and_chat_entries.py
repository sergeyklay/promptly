# This file is part of the Promptly.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Create chats and chat entries

Revision ID: b943c7643aa5
Revises:
Create Date: 2023-10-12 11:10:11.824409

"""

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = 'b943c7643aa5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'chats',
        sa.Column('title', sa.String(length=64), nullable=False),
        sa.Column('teaser', sa.String(length=128), nullable=False),
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
        sa.PrimaryKeyConstraint('id', name=op.f('pk_chats'))
    )

    with op.batch_alter_table('chats', schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f('ix_chats_created_at'),
            ['created_at'],
            unique=False
        )
        batch_op.create_index(
            batch_op.f('ix_chats_title'),
            ['title'],
            unique=False
        )
        batch_op.create_index(
            batch_op.f('ix_chats_updated_at'),
            ['updated_at'],
            unique=False
        )

    op.create_table(
        'chat_entries',
        sa.Column('teaser', sa.Text(), nullable=False),
        sa.Column('chat_id', sa.Integer(), nullable=False),
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
        sa.ForeignKeyConstraint(
            ['chat_id'],
            ['chats.id'],
            name=op.f('fk_chat_entries_chat_id_chats')
        ),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_chat_entries'))
    )

    with op.batch_alter_table('chat_entries', schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f('ix_chat_entries_created_at'),
            ['created_at'],
            unique=False
        )
        batch_op.create_index(
            batch_op.f('ix_chat_entries_updated_at'),
            ['updated_at'],
            unique=False
        )


def downgrade():
    with op.batch_alter_table('chat_entries', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_chat_entries_updated_at'))
        batch_op.drop_index(batch_op.f('ix_chat_entries_created_at'))

    op.drop_table('chat_entries')
    with op.batch_alter_table('chats', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_chats_updated_at'))
        batch_op.drop_index(batch_op.f('ix_chats_title'))
        batch_op.drop_index(batch_op.f('ix_chats_created_at'))

    op.drop_table('chats')
