"""add GH contribution model

Revision ID: 4352c9b469c6
Revises: eea480b1c214
Create Date: 2025-01-22 18:33:38.716143

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4352c9b469c6'
down_revision = 'eea480b1c214'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('github_contribution_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('author_github_login', sa.String(length=80), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('email', sa.String(length=80), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.Column('bio', sa.Text(), nullable=False),
    sa.Column('company', sa.String(length=80), nullable=False),
    sa.Column('watching', sa.Integer(), nullable=False),
    sa.Column('starred_repo', sa.Integer(), nullable=False),
    sa.Column('following', sa.Integer(), nullable=False),
    sa.Column('followers', sa.Integer(), nullable=False),
    sa.Column('private_contrib', sa.Integer(), nullable=False),
    sa.Column('commits', sa.Integer(), nullable=False),
    sa.Column('gists', sa.Integer(), nullable=False),
    sa.Column('issues', sa.Integer(), nullable=False),
    sa.Column('projects', sa.Integer(), nullable=False),
    sa.Column('pull_requests', sa.Integer(), nullable=False),
    sa.Column('pull_request_reviews', sa.Integer(), nullable=False),
    sa.Column('repositories', sa.Integer(), nullable=False),
    sa.Column('repo_discussions', sa.Integer(), nullable=False),
    sa.Column('commit_comments', sa.Integer(), nullable=False),
    sa.Column('issue_comments', sa.Integer(), nullable=False),
    sa.Column('gist_comments', sa.Integer(), nullable=False),
    sa.Column('repo_discussion_comments', sa.Integer(), nullable=False),
    sa.Column('selected_langs', sa.Text(), nullable=False),
    sa.Column('owned_original_repo', sa.Integer(), nullable=False),
    sa.Column('owned_original_repo_size', sa.Integer(), nullable=False),
    sa.Column('owned_original_repo_selected_langs_size', sa.Integer(), nullable=False),
    sa.Column('owned_original_repo_langs_number', sa.Integer(), nullable=False),
    sa.Column('owned_forked_repo', sa.Integer(), nullable=False),
    sa.Column('owned_forked_repo_size', sa.Integer(), nullable=False),
    sa.Column('owned_forked_repo_selected_langs_size', sa.Integer(), nullable=False),
    sa.Column('owned_forked_repo_langs_number', sa.Integer(), nullable=False),
    sa.Column('collaborating_original_repo', sa.Integer(), nullable=False),
    sa.Column('collaborating_original_repo_size', sa.Integer(), nullable=False),
    sa.Column('collaborating_original_repo_selected_langs_size', sa.Integer(), nullable=False),
    sa.Column('collaborating_original_repo_langs_number', sa.Integer(), nullable=False),
    sa.Column('collaborating_forked_repo', sa.Integer(), nullable=False),
    sa.Column('collaborating_forked_repo_size', sa.Integer(), nullable=False),
    sa.Column('collaborating_forked_repo_selected_langs_size', sa.Integer(), nullable=False),
    sa.Column('collaborating_forked_repo_langs_size_number', sa.Integer(), nullable=False),
    sa.Column('total_langs_number', sa.Integer(), nullable=False),
    sa.Column('user_query_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_query_id'], ['user_queries.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('github_contribution_data')
    # ### end Alembic commands ###
