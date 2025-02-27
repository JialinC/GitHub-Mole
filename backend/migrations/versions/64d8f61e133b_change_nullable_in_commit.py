"""change nullable in commit

Revision ID: 64d8f61e133b
Revises: 87022104a3c0
Create Date: 2025-02-03 17:02:57.235430

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '64d8f61e133b'
down_revision = '87022104a3c0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('commits', schema=None) as batch_op:
        batch_op.alter_column('authored_date',
               existing_type=mysql.DATETIME(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('commits', schema=None) as batch_op:
        batch_op.alter_column('authored_date',
               existing_type=mysql.DATETIME(),
               nullable=False)

    # ### end Alembic commands ###
