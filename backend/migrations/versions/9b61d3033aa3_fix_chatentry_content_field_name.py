# This file is part of the Promptly.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Fix ChatEntry content field name

Revision ID: 9b61d3033aa3
Revises: 5b8718259edc
Create Date: 2023-10-19 21:43:19.596419

"""

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = '9b61d3033aa3'
down_revision = '5b8718259edc'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('chat_entries', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('content', sa.Text(), nullable=False))
        batch_op.drop_column('teaser')


def downgrade():
    with op.batch_alter_table('chat_entries', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('teaser', sa.TEXT(), nullable=False))
        batch_op.drop_column('content')
