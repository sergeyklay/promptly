# This file is part of the Promptly.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Remove teaser from chat model

Revision ID: 02b742a74d0d
Revises: 9b61d3033aa3
Create Date: 2023-10-22 10:44:23.157698

"""

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = '02b742a74d0d'
down_revision = '9b61d3033aa3'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('chats', schema=None) as batch_op:
        batch_op.drop_column('teaser')


def downgrade():
    with op.batch_alter_table('chats', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('teaser', sa.VARCHAR(length=128), nullable=False))
