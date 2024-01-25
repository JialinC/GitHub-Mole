import os
from datetime import datetime
import pandas as pd
from collections import Counter
import github_query.util.helper as helper
from github_query.github_graphql.authentication import PersonalAccessTokenAuthenticator
from github_query.github_graphql.client import Client
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

client = Client(
    host="api.github.com", is_enterprise=False,
    authenticator=PersonalAccessTokenAuthenticator(token=os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN"))
)

enterprise_client = Client(
    host="github.ncsu.edu", is_enterprise=True,
    authenticator=PersonalAccessTokenAuthenticator(token=os.environ.get("GITHUB_ENTERPRISE_PERSONAL_ACCESS_TOKEN"))
)

df = pd.DataFrame(columns=['github', 'created_at', 'end_at', 'lifetime', 'res_con', 'commit', 'issue', 'pr', 'pr_review', 'repository', 'gists', 'repository_discussions',
                           'commit_comments', 'issue_comments', 'gist_comments', 'repository_discussion_comments',
                           'Atotal_count', 'Afork_count', 'Astargazer_count', 'Awatchers_count', 'Atotal_size', 'type_A_lang',
                           'Btotal_count', 'Bfork_count', 'Bstargazer_count', 'Bwatchers_count', 'Btotal_size', 'type_B_lang',
                           'Ctotal_count', 'Cfork_count', 'Cstargazer_count', 'Cwatchers_count', 'Ctotal_size', 'type_C_lang',
                           'Dtotal_count', 'Dfork_count', 'Dstargazer_count', 'Dwatchers_count', 'Dtotal_size', 'type_D_lang'])

logins = ["JialinC", "sdshao"]
for login in logins:
    start = client.execute(query=UserLogin(), substitutions={"user": login})["user"]["createdAt"]
    end = "2022-07-10T18:11:20Z"

    datetime_start = datetime.strptime(start, "%Y-%m-%dT%H:%M:%SZ")
    datetime_end = datetime.strptime(end, "%Y-%m-%dT%H:%M:%SZ")
    # Calculate the difference
    difference = datetime_end - datetime_start

    basic_stats = {'github': login, 'created_at': start, 'end_at': end, 'lifetime': difference.days}

    start_time = start
    period_end = helper.add_a_year(start)
    cumulated_contributions_collection = Counter({"res_con": 0, "commit": 0, "issue": 0, "pr": 0, "pr_review": 0, "repository": 0})
    temp = Counter({"res_con": 0, "commit": 0, "issue": 0, "pr": 0, "pr_review": 0, "repository": 0})

    type_A_repo = {"total_count": 0, "fork_count": 0, "stargazer_count": 0, "watchers_count": 0, "total_size": 0}
    type_A_lang = {}

    type_B_repo = {"total_count": 0, "fork_count": 0, "stargazer_count": 0, "watchers_count": 0, "total_size": 0}
    type_B_lang = {}

    type_C_repo = {"total_count": 0, "fork_count": 0, "stargazer_count": 0, "watchers_count": 0, "total_size": 0}
    type_C_lang = {}

    type_D_repo = {"total_count": 0, "fork_count": 0, "stargazer_count": 0, "watchers_count": 0, "total_size": 0}
    type_D_lang = {}

    try:
        while start < end:
            if period_end > end:
                period_end = end
            response = client.execute(query=UserContributionsCollection(),
                                      substitutions={"user": login,
                                                     "start": start,
                                                     "end": period_end})
            cumulated_contributions_collection += UserContributionsCollection.user_contributions_collection(response)
            start = period_end
            period_end = helper.add_a_year(start)
        cumulated_contributions_collection = Counter({key: cumulated_contributions_collection[key] + temp[key] for key in
                                                      set(cumulated_contributions_collection) | set(temp)})
        cumulated_contributions_collection = dict(cumulated_contributions_collection)
        ##print(cumulated_contributions_collection)

        # gists
        counter = 0
        for response in client.execute(query=UserGists(),
                                       substitutions={"user": login, "pg_size": 100}):
            counter += UserGists.created_before_time(UserGists.user_gists(response), end)
        cumulated_contributions_collection["gists"] = counter
        ##print(cumulated_contributions_collection)

        # repositoryDiscussions
        counter = 0
        for response in client.execute(query=UserRepositoryDiscussions(),
                                       substitutions={"user": login, "pg_size": 100}):
            counter += UserRepositoryDiscussions.created_before_time(
                UserRepositoryDiscussions.user_repository_discussions(response), end)
        cumulated_contributions_collection["repository_discussions"] = counter
        #print(cumulated_contributions_collection)

        # commitComments
        counter = 0
        for response in client.execute(query=UserCommitComments(), substitutions={"user": login, "pg_size": 100}):
            counter += UserCommitComments.created_before_time(UserCommitComments.user_commit_comments(response), end)
        cumulated_contributions_collection["commit_comments"] = counter
        #print(cumulated_contributions_collection)

        # issueComments
        counter = 0
        for response in client.execute(query=UserIssueComments(), substitutions={"user": login, "pg_size": 100}):
            counter += UserIssueComments.created_before_time(UserIssueComments.user_issue_comments(response), end)
        cumulated_contributions_collection["issue_comments"] = counter
        #print(cumulated_contributions_collection)

        # gistComments
        counter = 0
        for response in client.execute(query=UserGistComments(), substitutions={"user": login, "pg_size": 100}):
            counter += UserGistComments.created_before_time(UserGistComments.user_gist_comments(response), end)
        cumulated_contributions_collection["gist_comments"] = counter
        #print(cumulated_contributions_collection)

        # repositoryDiscussionComments
        counter = 0
        for response in client.execute(query=UserRepositoryDiscussionComments(),
                                       substitutions={"user": login, "pg_size": 100}):
            counter += UserRepositoryDiscussionComments.created_before_time(UserRepositoryDiscussionComments.user_repository_discussion_comments(response), end)
        cumulated_contributions_collection["repository_discussion_comments"] = counter
        #print(cumulated_contributions_collection)

        # TypeA
        for response in client.execute(query=UserRepositories(), substitutions={"user": login, "pg_size": 100,
                                                                                "is_fork": False,
                                                                                "ownership": "OWNER",
                                                                                "order_by": {"field": "CREATED_AT",
                                                                                             "direction": "ASC"}}):
            UserRepositories.cumulated_repository_stats(UserRepositories.user_repositories(response), type_A_repo, type_A_lang, end)
        type_A_repo = {'A' + key: value for key, value in type_A_repo.items()}
        cumulated_contributions_collection.update(type_A_repo)
        cumulated_contributions_collection["type_A_lang"] = type_A_lang
        #print(cumulated_contributions_collection)

        # TypeB
        for response in client.execute(query=UserRepositories(), substitutions={"user": login, "pg_size": 100,
                                                                                "is_fork": True,
                                                                                "ownership": "OWNER",
                                                                                "order_by": {"field": "CREATED_AT",
                                                                                             "direction": "ASC"}}):
            UserRepositories.cumulated_repository_stats(UserRepositories.user_repositories(response), type_B_repo, type_B_lang, end)
        type_B_repo = {'B' + key: value for key, value in type_B_repo.items()}
        cumulated_contributions_collection.update(type_B_repo)
        cumulated_contributions_collection["type_B_lang"] = type_B_lang
        #print(cumulated_contributions_collection)
        # TypeC
        for response in client.execute(query=UserRepositories(), substitutions={"user": login, "pg_size": 100,
                                                                                "is_fork": False,
                                                                                "ownership": "COLLABORATOR",
                                                                                "order_by": {"field": "CREATED_AT",
                                                                                             "direction": "ASC"}}):
            UserRepositories.cumulated_repository_stats(UserRepositories.user_repositories(response), type_C_repo, type_C_lang, end)
        type_C_repo = {'C' + key: value for key, value in type_C_repo.items()}
        cumulated_contributions_collection.update(type_C_repo)
        cumulated_contributions_collection["type_C_lang"] = type_C_lang
        #print(cumulated_contributions_collection)
        # TypeD
        for response in client.execute(query=UserRepositories(), substitutions={"user": login, "pg_size": 100,
                                                                                "is_fork": True,
                                                                                "ownership": "COLLABORATOR",
                                                                                "order_by": {"field": "CREATED_AT",
                                                                                             "direction": "ASC"}}):
            UserRepositories.cumulated_repository_stats(UserRepositories.user_repositories(response), type_D_repo, type_D_lang, end)
        type_D_repo = {'D' + key: value for key, value in type_D_repo.items()}
        cumulated_contributions_collection.update(type_D_repo)
        cumulated_contributions_collection["type_D_lang"] = type_D_lang
        #print(cumulated_contributions_collection)

        cumulated_contributions_collection["lifetime"] = difference.days
        #print(cumulated_contributions_collection)

    except Exception:
        print("DNE")

    #print(df)
    cumulated_contributions_collection.update(basic_stats)
    df = pd.concat([df, pd.DataFrame([cumulated_contributions_collection])], ignore_index=True)

df.to_csv("test.csv")
# #print(cumulated_contributions_collection)
# cumulated_contributions_collection = Counter({key: cumulated_contributions_collection[key] + temp[key] for key in
#                                               set(cumulated_contributions_collection) | set(temp)})
# #print(cumulated_contributions_collection)

#
#
#
#
#
#
# contributors = RepositoryContributors.extract_unique_author(response)
# contributors_ids = []
# for contributor in contributors:
#     user = client.execute(
#         query=UserLogin(),
#         substitutions={"user": contributor})['user']
#     contributors_ids.append((user['login'], user['id']))
#
# for login, user_id in contributors_ids:
#     response = client.execute(query=RepositoryContributorsContribution(),
#                               substitutions={"owner": owner,
#                                              "repo_name": repository,
#                                              "id": {"id": user_id}})
#     repo_login_cum = {"repo": repository, "login": login}
#     cumulated_contribution = RepositoryContributorsContribution.user_cumulated_contribution(response)
#     repo_login_cum.update(cumulated_contribution)
#     new_row_cum = pd.DataFrame([repo_login_cum])
#     df1 = pd.concat([df1, new_row_cum], ignore_index=True)
#
#     individual_contribution = RepositoryContributorsContribution.user_commit_contribution(response)
#     for i,v in enumerate(individual_contribution):
#         repo_login_ind = {"repo": repository, "login": login}
#         repo_login_ind.update(v)
#         individual_contribution[i] = repo_login_ind
#     new_rows_ind = pd.DataFrame(individual_contribution)
#     df2 = pd.concat([df2, new_rows_ind], ignore_index=True)
#
# #print(df1)
# #print(df2)
