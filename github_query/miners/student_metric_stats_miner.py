from datetime import datetime
import pandas as pd
from collections import Counter
import github_query.util.helper as helper
from github_query.github_graphql.client import Client, QueryFailedException
from github_query.queries.profile.user_login import UserLogin
from github_query.queries.contributions.user_gists import UserGists
from github_query.queries.contributions.user_repositories import UserRepositories
from github_query.queries.contributions.user_repository_discussions import UserRepositoryDiscussions
from github_query.queries.time_range_contributions.user_contributions_collection import \
    UserContributionsCollection
from github_query.queries.comments.user_gist_comments import UserGistComments
from github_query.queries.comments.user_issue_comments import UserIssueComments
from github_query.queries.comments.user_commit_comments import UserCommitComments
from github_query.queries.comments.user_repository_discussion_comments import UserRepositoryDiscussionComments


class UserMetricStatsMiner:
    """
    Helps mining repository data.
    """

    def __init__(self, client: Client):
        self._client = client
        self.exceptions = []
        self.total_contributions = pd.DataFrame(columns=['github', 'created_at', 'end_at', 'lifetime', 'res_con',
                                                         'commit', 'issue', 'pr', 'pr_review', 'repository', 'gists',
                                                         'repository_discussions',
                                                         'commit_comments', 'issue_comments',
                                                         'gist_comments', 'repository_discussion_comments',
                                                         'Atotal_count', 'Afork_count', 'Astargazer_count',
                                                         'Awatchers_count', 'Atotal_size', 'type_A_lang',
                                                         'Btotal_count', 'Bfork_count', 'Bstargazer_count',
                                                         'Bwatchers_count', 'Btotal_size', 'type_B_lang',
                                                         'Ctotal_count', 'Cfork_count', 'Cstargazer_count',
                                                         'Cwatchers_count', 'Ctotal_size', 'type_C_lang',
                                                         'Dtotal_count', 'Dfork_count', 'Dstargazer_count',
                                                         'Dwatchers_count', 'Dtotal_size', 'type_D_lang'])

    def run(self, login: str, start: str = None, end: str = None):
        """
        Collect GitHub metric data for a user in the give time span.
        Args:
            login: user GitHub account
            start: start time
            end: end time
        """
        try:
            if not start:
                start = self._client.execute(query=UserLogin(), substitutions={"user": login})["user"]["createdAt"]
            if end is None:
                end = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')

            datetime_start = datetime.strptime(start, "%Y-%m-%dT%H:%M:%SZ")
            datetime_end = datetime.strptime(end, "%Y-%m-%dT%H:%M:%SZ")
            # Calculate the difference
            difference = datetime_end - datetime_start

            basic_stats = {'github': login, 'created_at': start, 'end_at': end, 'lifetime': difference.days}

            period_end = helper.add_a_year(start)
            cumulated_contributions_collection = Counter({"res_con": 0, "commit": 0, "issue": 0,
                                                          "pr": 0, "pr_review": 0, "repository": 0})

            temp = Counter({"res_con": 0, "commit": 0, "issue": 0, "pr": 0, "pr_review": 0, "repository": 0})

            type_A_repo = {"total_count": 0, "fork_count": 0, "stargazer_count": 0, "watchers_count": 0,
                           "total_size": 0}
            type_A_lang = {}

            type_B_repo = {"total_count": 0, "fork_count": 0, "stargazer_count": 0, "watchers_count": 0,
                           "total_size": 0}
            type_B_lang = {}

            type_C_repo = {"total_count": 0, "fork_count": 0, "stargazer_count": 0, "watchers_count": 0,
                           "total_size": 0}
            type_C_lang = {}

            type_D_repo = {"total_count": 0, "fork_count": 0, "stargazer_count": 0, "watchers_count": 0,
                           "total_size": 0}
            type_D_lang = {}

            while start < end:
                if period_end > end:
                    period_end = end
                response = self._client.execute(query=UserContributionsCollection(),
                                                substitutions={"user": login,
                                                               "start": start,
                                                               "end": period_end})

                cumulated_contributions_collection += UserContributionsCollection.user_contributions_collection(
                    response)
                start = period_end
                period_end = helper.add_a_year(start)


            cumulated_contributions_collection = Counter(
                {key: cumulated_contributions_collection[key] + temp[key] for key in
                 set(cumulated_contributions_collection) | set(temp)})
            cumulated_contributions_collection = dict(cumulated_contributions_collection)

            # gists
            counter = 0
            for response in self._client.execute(query=UserGists(),
                                                 substitutions={"user": login, "pg_size": 100}):
                counter += UserGists.created_before_time(UserGists.user_gists(response), end)
            cumulated_contributions_collection["gists"] = counter

            # repositoryDiscussions
            counter = 0
            for response in self._client.execute(query=UserRepositoryDiscussions(),
                                                 substitutions={"user": login, "pg_size": 100}):
                counter += UserRepositoryDiscussions.created_before_time(
                    UserRepositoryDiscussions.user_repository_discussions(response), end)
            cumulated_contributions_collection["repository_discussions"] = counter

            # commitComments
            counter = 0
            for response in self._client.execute(query=UserCommitComments(),
                                                 substitutions={"user": login, "pg_size": 100}):
                counter += UserCommitComments.created_before_time(UserCommitComments.user_commit_comments(response),
                                                                  end)
            cumulated_contributions_collection["commit_comments"] = counter

            # issueComments
            counter = 0
            for response in self._client.execute(query=UserIssueComments(),
                                                 substitutions={"user": login, "pg_size": 100}):
                counter += UserIssueComments.created_before_time(UserIssueComments.user_issue_comments(response),
                                                                 end)
            cumulated_contributions_collection["issue_comments"] = counter

            # gistComments
            counter = 0
            for response in self._client.execute(query=UserGistComments(),
                                                 substitutions={"user": login, "pg_size": 100}):
                counter += UserGistComments.created_before_time(UserGistComments.user_gist_comments(response), end)
            cumulated_contributions_collection["gist_comments"] = counter

            # repositoryDiscussionComments
            counter = 0
            for response in self._client.execute(query=UserRepositoryDiscussionComments(),
                                                 substitutions={"user": login, "pg_size": 100}):
                counter += UserRepositoryDiscussionComments.created_before_time(
                    UserRepositoryDiscussionComments.user_repository_discussion_comments(response), end)
            cumulated_contributions_collection["repository_discussion_comments"] = counter

            # TypeA
            for response in self._client.execute(query=UserRepositories(),
                                                 substitutions={"user": login, "pg_size": 100,
                                                                "is_fork": False,
                                                                "ownership": "OWNER",
                                                                "order_by": {
                                                                    "field": "CREATED_AT",
                                                                    "direction": "ASC"}}):
                UserRepositories.cumulated_repository_stats(UserRepositories.user_repositories(response),
                                                            type_A_repo, type_A_lang, end)
            type_A_repo = {'A' + key: value for key, value in type_A_repo.items()}
            cumulated_contributions_collection.update(type_A_repo)
            cumulated_contributions_collection["type_A_lang"] = type_A_lang

            # TypeB
            for response in self._client.execute(query=UserRepositories(),
                                                 substitutions={"user": login, "pg_size": 100,
                                                                "is_fork": True,
                                                                "ownership": "OWNER",
                                                                "order_by": {
                                                                    "field": "CREATED_AT",
                                                                    "direction": "ASC"}}):
                UserRepositories.cumulated_repository_stats(UserRepositories.user_repositories(response),
                                                            type_B_repo, type_B_lang, end)
            type_B_repo = {'B' + key: value for key, value in type_B_repo.items()}
            cumulated_contributions_collection.update(type_B_repo)
            cumulated_contributions_collection["type_B_lang"] = type_B_lang

            # TypeC
            for response in self._client.execute(query=UserRepositories(),
                                                 substitutions={"user": login, "pg_size": 100,
                                                                "is_fork": False,
                                                                "ownership": "COLLABORATOR",
                                                                "order_by": {
                                                                    "field": "CREATED_AT",
                                                                    "direction": "ASC"}}):
                UserRepositories.cumulated_repository_stats(UserRepositories.user_repositories(response),
                                                            type_C_repo, type_C_lang, end)
            type_C_repo = {'C' + key: value for key, value in type_C_repo.items()}
            cumulated_contributions_collection.update(type_C_repo)
            cumulated_contributions_collection["type_C_lang"] = type_C_lang

            # TypeD
            for response in self._client.execute(query=UserRepositories(),
                                                 substitutions={"user": login, "pg_size": 100,
                                                                "is_fork": True,
                                                                "ownership": "COLLABORATOR",
                                                                "order_by": {
                                                                    "field": "CREATED_AT",
                                                                    "direction": "ASC"}}):
                UserRepositories.cumulated_repository_stats(UserRepositories.user_repositories(response),
                                                            type_D_repo, type_D_lang, end)
            type_D_repo = {'D' + key: value for key, value in type_D_repo.items()}
            cumulated_contributions_collection.update(type_D_repo)
            cumulated_contributions_collection["type_D_lang"] = type_D_lang

            cumulated_contributions_collection.update(basic_stats)
            self.total_contributions = pd.concat(
                [self.total_contributions, pd.DataFrame([cumulated_contributions_collection])], ignore_index=True)

        except QueryFailedException:
            dne = pd.DataFrame([{'github': login, 'created_at': "Do Not Exist", 'end_at': pd.NA, 'lifetime': pd.NA,
                                 'res_con': pd.NA, 'commit': pd.NA, 'issue': pd.NA, 'pr': pd.NA, 'pr_review': pd.NA,
                                 'repository': pd.NA, 'gists': pd.NA, 'repository_discussions': pd.NA,
                                 'commit_comments': pd.NA, 'issue_comments': pd.NA, 'gist_comments': pd.NA,
                                 'repository_discussion_comments': pd.NA,
                                 'Atotal_count': pd.NA, 'Afork_count': pd.NA, 'Astargazer_count': pd.NA,
                                 'Awatchers_count': pd.NA, 'Atotal_size': pd.NA, 'type_A_lang': pd.NA,
                                 'Btotal_count': pd.NA, 'Bfork_count': pd.NA, 'Bstargazer_count': pd.NA,
                                 'Bwatchers_count': pd.NA, 'Btotal_size': pd.NA, 'type_B_lang': pd.NA,
                                 'Ctotal_count': pd.NA, 'Cfork_count': pd.NA, 'Cstargazer_count': pd.NA,
                                 'Cwatchers_count': pd.NA, 'Ctotal_size': pd.NA, 'type_C_lang': pd.NA,
                                 'Dtotal_count': pd.NA, 'Dfork_count': pd.NA, 'Dstargazer_count': pd.NA,
                                 'Dwatchers_count': pd.NA, 'Dtotal_size': pd.NA, 'type_D_lang': pd.NA}])

            self.total_contributions = pd.concat(
                [self.total_contributions, dne], ignore_index=True)
            self.exceptions.append(login)

        except Exception as e:
            dne = pd.DataFrame([{'github': login, 'created_at': "Do Not Exist", 'end_at': "Unknown exception", 'lifetime': pd.NA,
                                 'res_con': pd.NA, 'commit': pd.NA, 'issue': pd.NA, 'pr': pd.NA, 'pr_review': pd.NA,
                                 'repository': pd.NA, 'gists': pd.NA, 'repository_discussions': pd.NA,
                                 'commit_comments': pd.NA, 'issue_comments': pd.NA, 'gist_comments': pd.NA,
                                 'repository_discussion_comments': pd.NA,
                                 'Atotal_count': pd.NA, 'Afork_count': pd.NA, 'Astargazer_count': pd.NA,
                                 'Awatchers_count': pd.NA, 'Atotal_size': pd.NA, 'type_A_lang': pd.NA,
                                 'Btotal_count': pd.NA, 'Bfork_count': pd.NA, 'Bstargazer_count': pd.NA,
                                 'Bwatchers_count': pd.NA, 'Btotal_size': pd.NA, 'type_B_lang': pd.NA,
                                 'Ctotal_count': pd.NA, 'Cfork_count': pd.NA, 'Cstargazer_count': pd.NA,
                                 'Cwatchers_count': pd.NA, 'Ctotal_size': pd.NA, 'type_C_lang': pd.NA,
                                 'Dtotal_count': pd.NA, 'Dfork_count': pd.NA, 'Dstargazer_count': pd.NA,
                                 'Dwatchers_count': pd.NA, 'Dtotal_size': pd.NA, 'type_D_lang': pd.NA}])
            self.total_contributions = pd.concat(
                [self.total_contributions, dne], ignore_index=True)
            self.exceptions.append(login)




