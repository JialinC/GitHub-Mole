"""add Repo model

Revision ID: 6619add7f597
Revises: bab5af5cf61e
Create Date: 2025-01-22 16:05:30.441636

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6619add7f597'
down_revision = 'bab5af5cf61e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('repositories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('author_github_login', sa.String(length=80), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('primary_language', sa.String(length=80), nullable=False),
    sa.Column('languages', sa.String(length=80), nullable=False),
    sa.Column('repository_type', sa.String(length=80), nullable=False),
    sa.Column('user_query_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_query_id'], ['user_queries.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('repositories')
    # ### end Alembic commands ###
