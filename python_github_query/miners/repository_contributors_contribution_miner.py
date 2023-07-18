import pandas as pd
import json
import python_github_query.util.helper as helper
from python_github_query.github_graphql.client import Client, QueryFailedException
from python_github_query.queries.profile.user_login import UserLogin
from python_github_query.queries.repositories.repository_contributors import RepositoryContributors
from python_github_query.queries.repositories.repository_contributors_contribution import \
    RepositoryContributorsContribution


class RepositoryContributorsContributionMiner:
    """
    Helps mining repository data.
    """

    def __init__(self, client: Client):
        self._client = client
        self.cumulated_contribution = pd.DataFrame(columns=['repo', 'login', 'commits', 'additions', 'deletions'])
        self.individual_contribution = pd.DataFrame(columns=['repo', 'login', 'authoredDate', 'changedFiles',
                                                             'additions', 'deletions', 'message'])

    def run(self, link: str):
        """
        Collect data for a repository using a link.
        Args:
            link: Link to the repository
        """
        try:
            owner, repository = helper.get_owner_and_name(link)
            response = self._client.execute(query=RepositoryContributors(),
                                            substitutions={"owner": owner, "repo_name": repository})
        except QueryFailedException as e:
            message = e.response.json()['errors'][0]['message']
            print(message)
            dne = pd.DataFrame(
                [{'repo': message, 'login': pd.NA, 'commits': pd.NA, 'additions': pd.NA, 'deletions': pd.NA}])
            self.cumulated_contribution = pd.concat([self.cumulated_contribution, dne], ignore_index=True)
            return

        contributors = RepositoryContributors.extract_unique_author(response)
        contributors_ids = []
        for contributor in contributors:
            user = self._client.execute(query=UserLogin(), substitutions={"user": contributor})['user']
            contributors_ids.append((user['login'], user['id']))

        for login, user_id in contributors_ids:
            print(f"querying user: {login}")
            response = self._client.execute(query=RepositoryContributorsContribution(),
                                            substitutions={"owner": owner,
                                                           "repo_name": repository,
                                                           "id": {"id": user_id}})

            repo_login_cum = {"repo": repository, "login": login}
            cumulated_contribution = RepositoryContributorsContribution.user_cumulated_contribution(response)
            repo_login_cum.update(cumulated_contribution)
            new_row_cum = pd.DataFrame([repo_login_cum])
            self.cumulated_contribution = pd.concat([self.cumulated_contribution, new_row_cum], ignore_index=True)

            individual_contribution = RepositoryContributorsContribution.user_commit_contribution(response)
            for i, v in enumerate(individual_contribution):
                repo_login_ind = {"repo": repository, "login": login}
                repo_login_ind.update(v)
                individual_contribution[i] = repo_login_ind
            new_rows_ind = pd.DataFrame(individual_contribution)
            self.individual_contribution = pd.concat([self.individual_contribution, new_rows_ind], ignore_index=True)
