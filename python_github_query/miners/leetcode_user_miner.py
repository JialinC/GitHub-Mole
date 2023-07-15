from datetime import datetime
import pandas as pd
from collections import Counter
import python_github_query.util.helper as helper
from python_github_query.github_graphql.client import Client, QueryFailedException
from python_github_query.queries.contributions.user_repositories import UserRepositories
from python_github_query.queries.profile.user_profile_stats import UserProfileStats
from python_github_query.queries.time_range_contributions.user_contributions_collection import \
    UserContributionsCollection


class LeetcodeUserMiner:
    """
    Helps mining LeetCode user's GitHub data.
    """

    def __init__(self, client: Client):
        self._client = client
        self.exceptions = []
        self.total_contributions = pd.DataFrame(
            columns=['github', 'created_at', 'end_at', 'lifetime', 'company', 'followers',
                     'gists', 'issues', 'projects', 'pull_requests', 'repositories',
                     'repository_discussions', 'res_con', 'commit', 'pr_review',
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

    def run(self, login: str):
        """
        Collect GitHub metric data for a user in the give time span.
        Args:
            login: user GitHub account
        """
        try:
            response = self._client.execute(query=UserProfileStats(), substitutions={"user": login})
            profile_stats = UserProfileStats.profile_stats(response)
            end = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
            start = profile_stats['created_at']
            datetime_start = datetime.strptime(start, "%Y-%m-%dT%H:%M:%SZ")
            datetime_end = datetime.strptime(end, "%Y-%m-%dT%H:%M:%SZ")
            # Calculate the difference
            difference = datetime_end - datetime_start
            basic_stats = {'end_at': end, 'lifetime': difference.days}

            period_end = helper.add_a_year(start)
            cumulated_contributions_collection = Counter({"res_con": 0, "commit": 0, 'pr_review': 0})
            temp = Counter({"res_con": 0, "commit": 0, 'pr_review': 0})

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
                queried_contribution = UserContributionsCollection.user_contributions_collection(response)
                for key in cumulated_contributions_collection:
                    cumulated_contributions_collection[key] += queried_contribution[key]
                start = period_end
                period_end = helper.add_a_year(start)

            cumulated_contributions_collection = Counter(
                {key: cumulated_contributions_collection[key] + temp[key] for key in
                 set(cumulated_contributions_collection) | set(temp)})
            cumulated_contributions_collection = dict(cumulated_contributions_collection)
            cumulated_contributions_collection.update(profile_stats)

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
            self.exceptions.append(login)

        except Exception as e:
            self.exceptions.append(login)
