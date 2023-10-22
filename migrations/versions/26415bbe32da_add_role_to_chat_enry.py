# This file is part of the Promptly.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Add role to chat enry

Revision ID: 26415bbe32da
Revises: 02b742a74d0d
Create Date: 2023-10-22 18:32:29.794491

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '26415bbe32da'
down_revision = '02b742a74d0d'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('chat_entries', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                'role',
                sa.Enum('user', 'assistant', name='role_types'),
                nullable=False
            )
        )


def downgrade():
    with op.batch_alter_table('chat_entries', schema=None) as batch_op:
        batch_op.drop_column('role')
