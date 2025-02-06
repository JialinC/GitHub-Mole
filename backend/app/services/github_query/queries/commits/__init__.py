"""
Import repository related queries
"""

from .repository_contributor_contributions import RepositoryContributorContributions
from .user_repository_names import UserRepositoryNames


__all__ = [
    "RepositoryContributorContributions",
    "UserRepositoryNames",
]
