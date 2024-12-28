"""update Repository model for owner id

Revision ID: 539c1e5db2b0
Revises: db856281182e
Create Date: 2024-12-28 01:25:04.741298

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '539c1e5db2b0'
down_revision = 'db856281182e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('repositories', schema=None) as batch_op:
        batch_op.add_column(sa.Column('owner_id', sa.String(length=80), nullable=False))
        batch_op.add_column(sa.Column('affiliation_login', sa.String(length=80), nullable=False))
        batch_op.drop_column('author_github_login')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('repositories', schema=None) as batch_op:
        batch_op.add_column(sa.Column('author_github_login', mysql.VARCHAR(length=80), nullable=False))
        batch_op.drop_column('affiliation_login')
        batch_op.drop_column('owner_id')

    # ### end Alembic commands ###
