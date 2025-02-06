"""add Repo Diss  model

Revision ID: bab5af5cf61e
Revises: a5ca609ea928
Create Date: 2025-01-22 14:55:47.170494

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bab5af5cf61e'
down_revision = 'a5ca609ea928'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('repository_discussions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('author_github_login', sa.String(length=80), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('body_text', sa.Text(), nullable=False),
    sa.Column('user_query_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_query_id'], ['user_queries.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('repository_discussions')
    # ### end Alembic commands ###
