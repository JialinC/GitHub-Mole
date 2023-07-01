import os
from string import Template
import json
#from helper.helper import print_methods, print_attr
from python_github_query.github_graphql.query import QueryNodePaginator, QueryNode, Query, PaginatedQuery
from python_github_query.github_graphql.authentication import PersonalAccessTokenAuthenticator
from python_github_query.github_graphql.client import Client
from python_github_query.queries.login import UserLoginViewer, UserLogin
from python_github_query.queries.metrics import UserMetrics
from python_github_query.queries.commits import UserCommits
from python_github_query.queries.comments import UserComments
from python_github_query.queries.contributions import UserContributions
from python_github_query.queries.repositories import UserRepositories

import requests
from requests import Response

if __name__ == '__main__':
    client = Client(
        host="api.github.com", is_enterprise=False,
        authenticator=PersonalAccessTokenAuthenticator(token=os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN"))
    )

    enterprise_client = Client(
        host="github.ncsu.edu", is_enterprise=True,
        authenticator=PersonalAccessTokenAuthenticator(token=os.environ.get("GITHUB_ENTERPRISE_PERSONAL_ACCESS_TOKEN"))
    )

    path1 = "https://api.github.com/graphql"
    header1 = client._generate_headers()
    path2 = "https://github.ncsu.edu/api/graphql"
    header2 = enterprise_client._generate_headers()

    args = {"user": "JialinC", "pg_size": 2, "comment_type": "issueComments"}
    response = client.execute(
        query=UserLoginViewer(), substitutions={}
    )
    print(response)

    test = UserCommits()
    print(test)
    # print(Query.convert_dict())
    # args = {"user": "JialinC", "pg_size": 5, "is_fork": True, "ownership": "OWNER", "order_by": {"field": "CREATED_AT", "direction": "ASC"}}
    # converted = Query.convert_dict(args)
    print(test.substitute(**{"user": "jcui9", "start": "2020-02-07T18:11:20Z", "end": "2021-02-07T18:11:20Z"}))

    # pullRequests, issues, gists, repositoryDiscussions
    # print("True", "OWNER")
    # for response in client.execute(query=UserRepositories(), substitutions={"user": "JialinC",
    #                                                                         "pg_size": 5,
    #                                                                         "is_fork": True,
    #                                                                         "ownership": "OWNER",
    #                                                                         "order_by": {"field": "CREATED_AT", "direction": "ASC"}}):
    #     print(response)
    #
    # print("True", "COLLABORATOR")
    # for response in client.execute(query=UserRepositories(), substitutions={"user": "JialinC",
    #                                                                         "pg_size": 5,
    #                                                                         "is_fork": True,
    #                                                                         "ownership": "COLLABORATOR",
    #                                                                         "order_by": {"field": "CREATED_AT",
    #                                                                                      "direction": "ASC"}}):
    #     print(response)
    #
    # print("False", "OWNER")
    # for response in client.execute(query=UserRepositories(), substitutions={"user": "JialinC",
    #                                                                         "pg_size": 5,
    #                                                                         "is_fork": False,
    #                                                                         "ownership": "OWNER",
    #                                                                         "order_by": {"field": "CREATED_AT",
    #                                                                                      "direction": "ASC"}}):
    #     print(response)
    #
    # print("False", "COLLABORATOR")
    # for response in client.execute(query=UserRepositories(), substitutions={"user": "JialinC",
    #                                                                         "pg_size": 5,
    #                                                                         "is_fork": False,
    #                                                                         "ownership": "COLLABORATOR",
    #                                                                         "order_by": {"field": "CREATED_AT",
    #                                                                                      "direction": "ASC"}}):
    #     print(response)

    # print("True", "OWNER")
    # for response in enterprise_client.execute(query=UserRepositories(), substitutions={"user": "jcui9",
    #                                                                         "pg_size": 5,
    #                                                                         "is_fork": True,
    #                                                                         "ownership": "OWNER",
    #                                                                         "order_by": {"field": "CREATED_AT",
    #                                                                                      "direction": "ASC"}}):
    #     print(response)
    #
    # print("True", "COLLABORATOR")
    # for response in enterprise_client.execute(query=UserRepositories(), substitutions={"user": "jcui9",
    #                                                                         "pg_size": 5,
    #                                                                         "is_fork": True,
    #                                                                         "ownership": "COLLABORATOR",
    #                                                                         "order_by": {"field": "CREATED_AT",
    #                                                                                      "direction": "ASC"}}):
    #     print(response)
    #
    # print("False", "OWNER")
    # for response in enterprise_client.execute(query=UserRepositories(), substitutions={"user": "jcui9",
    #                                                                         "pg_size": 5,
    #                                                                         "is_fork": False,
    #                                                                         "ownership": "OWNER",
    #                                                                         "order_by": {"field": "CREATED_AT",
    #                                                                                      "direction": "ASC"}}):
    #     print(response)
    #
    # print("False", "COLLABORATOR")
    # for response in enterprise_client.execute(query=UserRepositories(), substitutions={"user": "jcui9",
    #                                                                         "pg_size": 5,
    #                                                                         "is_fork": False,
    #                                                                         "ownership": "COLLABORATOR",
    #                                                                         "order_by": {"field": "CREATED_AT",
    #                                                                                      "direction": "ASC"}}):
    #     print(response)




    # for response in client.execute(query=UserContributions(),
    #                                substitutions={"user": "JialinC", "pg_size": 2, "contribution_type": "gists"}):
    #     print(response)
    # for response in client.execute(query=UserContributions(),
    #                                substitutions={"user": "JialinC", "pg_size": 2, "contribution_type": "repositoryDiscussions"}):
    #     print(response)
    # for response in enterprise_client.execute(query=UserRepositories, substitutions={"user": "jcui9", "pg_size": 2,
    #                                                                          "contribution_type": "pullRequests"}):
    #     print(response)
    # for response in enterprise_client.execute(query=UserContributions(),
    #                                substitutions={"user": "jcui9", "pg_size": 2, "contribution_type": "issues"}):
    #     print(response)
    # for response in enterprise_client.execute(query=UserContributions(),
    #                                substitutions={"user": "jcui9", "pg_size": 2, "contribution_type": "gists"}):
    #     print(response)
    # for response in enterprise_client.execute(query=UserContributions(),
    #                                substitutions={"user": "jcui9", "pg_size": 2,
    #                                               "contribution_type": "repositoryDiscussions"}):
    #     print(response)









    # test = UserComments.query
    # print(test)
    # print(test.path)
    # print(test.paginator)
    # args = {"user": "JialinC", "pg_size": 2, "comment_type": "issueComments"}
    # path = PaginatedQuery.extract_path_to_pageinfo_node(test)
    # print(path)
    # pnode = path[1]
    # print(pnode is test.fields[0].fields[1])
    # print(test)
    # test_query = test.substitute(**args)
    # print(test_query)

    # comments
    # response1 = requests.post(
    #     path1,
    #     json={'query': test_query},
    #     headers=header1
    # )
    # print(response1.json())
    #
    # while test.paginator.has_next():
    #     test_query = test.substitute(**args)
    #     print(test_query)
    #     response = requests.post(
    #         path1,
    #         json={'query': test_query},
    #         headers=header1
    #     ).json()['data']
    #     curr_node = response
    #     print(curr_node)
    #     for field_name in test.path:
    #         curr_node = curr_node[Template(field_name).substitute(**args)]
    #         print(curr_node)
    #     end_cursor = curr_node["pageInfo"]["endCursor"]
    #     print(end_cursor)
    #     has_next_page = curr_node["pageInfo"]["hasNextPage"]
    #     print(has_next_page)
    #     test.paginator.update_paginator(has_next_page, end_cursor)

    # test_query = test.substitute(**args)
    # print(test_query)
    # response = requests.post(
    #    path1,
    #    json={'query': test_query},
    #    headers=header1
    # ).json()['data']
    # print(response)
    # response = client.execute(
    #     query=UserLoginViewer(), substitutions={}
    # )
    # print(response)

    # for response in client.execute(query=UserComments(), substitutions={"user": "JialinC", "pg_size": 2, "comment_type": "commitComments"}):
    #     print(response)
    # for response in client.execute(query=UserComments(),
    #                                substitutions={"user": "JialinC", "pg_size": 2, "comment_type": "gistComments"}):
    #     print(response)
    # for response in client.execute(query=UserComments(),
    #                                substitutions={"user": "JialinC", "pg_size": 2, "comment_type": "issueComments"}):
    #     print(response)
    # for response in client.execute(query=UserComments(),
    #                                substitutions={"user": "JialinC", "pg_size": 2, "comment_type": "repositoryDiscussionComments"}):
    #     print(response)

    # for response in enterprise_client.execute(query=UserComments(), substitutions={"user": "jcui9", "pg_size": 2, "comment_type": "commitComments"}):
    #     print(response)
    # for response in enterprise_client.execute(query=UserComments(),
    #                                substitutions={"user": "jcui9", "pg_size": 2, "comment_type": "gistComments"}):
    #     print(response)
    # for response in enterprise_client.execute(query=UserComments(),
    #                                substitutions={"user": "jcui9", "pg_size": 2, "comment_type": "issueComments"}):
    #     print(response)
    # for response in enterprise_client.execute(query=UserComments(),
    #                                substitutions={"user": "jcui9", "pg_size": 2, "comment_type": "repositoryDiscussionComments"}):
    #     print(response)

    # for response in enterprise_client.execute(query=UserComments(), substitutions={"user": "jcui9", "pg_size": 2, "comment_type": "commitComments"}):
    #     print(response)

    # for response in client.execute(query=UserComments(), substitutions={"user": "JialinC", "pg_size": 2, "comment_type": "issueComments"}):
    #     print(response)





    # print(test1.name)
    # print(test1.fields)
    # print(len(test1.fields))
    # print('=====')
    # print(test1.fields[0].name)
    # print(test1.fields[0].fields)
    # print(len(test1.fields[0].fields))
    # print('=====')
    # print(test1.fields[0].fields[0])
    # print('=====')
    # print(test1.fields[0].fields[1].name)
    # print(test1.fields[0].fields[1].fields)
    # print(len(test1.fields[0].fields[1].fields))
    # print('=====')
    # print(test1.fields[0].fields[1].fields[0])
    # print('=====')
    # print(test1.fields[0].fields[1].fields[1].name)
    # print(test1.fields[0].fields[1].fields[1].fields)
    # print(len(test1.fields[0].fields[1].fields[1].fields))
    # print('=====')
    # print(test1.fields[0].fields[1].fields[2].name)
    # print(test1.fields[0].fields[1].fields[2].fields)
    # print(len(test1.fields[0].fields[1].fields[2].fields))


    # UserLogin
    # response1 = requests.post(
    #     path1,
    #     json={'query': """query {
    #               user(login: "JialinC") {
    #                 contributionsCollection(from: "2021-02-07T18:11:20Z", to: "2022-02-07T18:11:20Z") {
    #                   startedAt
    #                   endedAt
    #                   hasActivityInThePast
    #                   hasAnyContributions
    #                   hasAnyRestrictedContributions
    #                   restrictedContributionsCount
    #                   totalCommitContributions
    #                   totalIssueContributions
    #                   totalPullRequestContributions
    #                   totalPullRequestReviewContributions
    #                   totalRepositoriesWithContributedCommits
    #                   totalRepositoriesWithContributedIssues
    #                   totalRepositoriesWithContributedPullRequestReviews
    #                   totalRepositoriesWithContributedPullRequests
    #                   totalRepositoryContributions
    #                 }
    #               }
    #             }"""
    #           },
    #     headers=header1
    # )
    # print(response1.json())

    #print(UserCommits.query)
    # response2 = client.execute(
    #     query=UserCommits.query, substitutions={"user": "JialinC", "start": "2020-02-07T18:11:20Z", "end": "2021-02-07T18:11:20Z"}
    # )
    # print(response2)

    # response3 = requests.post(
    #     path2,
    #     json={'query': """query {
    #                   user(login: "jcui9") {
    #                     contributionsCollection(from: "2020-02-07T18:11:20Z", to: "2021-02-07T18:11:20Z") {
    #                       startedAt
    #                       endedAt
    #                       hasActivityInThePast
    #                       hasAnyContributions
    #                       hasAnyRestrictedContributions
    #                       restrictedContributionsCount
    #                       totalCommitContributions
    #                       totalIssueContributions
    #                       totalPullRequestContributions
    #                       totalPullRequestReviewContributions
    #                       totalRepositoriesWithContributedCommits
    #                       totalRepositoriesWithContributedIssues
    #                       totalRepositoriesWithContributedPullRequestReviews
    #                       totalRepositoriesWithContributedPullRequests
    #                       totalRepositoryContributions
    #                     }
    #                   }
    #                 }"""
    #               },
    #     headers=header2
    # )
    # print(response3.json())

    # response4 = enterprise_client.execute(
    #     query=UserCommits.query, substitutions={"user": "jcui9", "start": "2020-02-07T18:11:20Z", "end": "2021-02-07T18:11:20Z"}
    # )
    # print(response4)



    # UserLogin
    # response1 = requests.post(
    #     path1,
    #     json={'query': """query { user(login: "JialinC") {
    #                                 login name email createdAt bio company isBountyHunter isCampusExpert
    #                                 isDeveloperProgramMember isEmployee isGitHubStar isHireable isSiteAdmin
    #                                 watching { totalCount }
    #                                 starredRepositories { totalCount }
    #                                 following { totalCount }
    #                                 followers { totalCount }
    #                                 gists { totalCount }
    #                                 gistComments { totalCount }
    #                                 issueComments { totalCount }
    #                                 issues { totalCount }
    #                                 projects { totalCount }
    #                                 pullRequests { totalCount }
    #                                 repositories { totalCount }
    #                                 repositoryDiscussionComments { totalCount }
    #                                 repositoryDiscussions { totalCount }
    #                             }
    #                     }"""
    #           },
    #     headers=header1
    # )
    # print(response1.json())

    # print(UserMetrics.query)
    # response2 = client.execute(
    #     query=UserMetrics.query, substitutions={"user": "JialinC"}
    # )
    # print(response2)

    # response3 = requests.post(
    #     path2,
    #     json={'query': """query { user(login: "jcui9") {
    #                                 login name email createdAt bio company isBountyHunter isCampusExpert
    #                                 isDeveloperProgramMember isEmployee isGitHubStar isHireable isSiteAdmin
    #                                 watching { totalCount }
    #                                 starredRepositories { totalCount }
    #                                 following { totalCount }
    #                                 followers { totalCount }
    #                                 gists { totalCount }
    #                                 gistComments { totalCount }
    #                                 issueComments { totalCount }
    #                                 issues { totalCount }
    #                                 projects { totalCount }
    #                                 pullRequests { totalCount }
    #                                 repositories { totalCount }
    #                                 repositoryDiscussionComments { totalCount }
    #                                 repositoryDiscussions { totalCount }
    #                             }
    #                     }"""
    #           },
    #     headers=header2
    # )
    # print(response3.json())

    # response4 = enterprise_client.execute(
    #     query=UserMetrics.query, substitutions={"user": "jcui9"}
    # )
    # print(response4)

    # UserLoginViewer
    # response1 = requests.post(
    #     path1,
    #     json={'query': 'query { viewer { login } }'},
    #     headers=header1
    # )
    # print(response1.json())
    #
    # response2 = client.execute(
    #      query=UserLoginViewer.query, substitutions={}
    # )
    # print(response2)
    #
    # response3 = requests.post(
    #     path2,
    #     json={'query': 'query { viewer { login } }'},
    #     headers=header2
    # )
    # print(response3.json())
    #
    # response4 = enterprise_client.execute(
    #     query=UserLoginViewer.query, substitutions={}
    # )
    # print(response4)

    # UserLogin
    # response1 = requests.post(
    #     path1,
    #     json={'query': 'query { user(login: "JialinC") { login name email createdAt}}'},
    #     headers=header1
    # )
    # print(response1.json())
    #
    # # print(UserLogin.query)
    # response2 = client.execute(
    #     query=UserLogin.query, substitutions={"user": "JialinC"}
    # )
    # print(response2)
    #
    # response3 = requests.post(
    #     path2,
    #     json={'query': 'query { user(login: "jcui9") { login name email createdAt}}'},
    #     headers=header2
    # )
    # print(response3.json())
    #
    # response4 = enterprise_client.execute(
    #     query=UserLogin.query, substitutions={"user": "jcui9"}
    # )
    # print(response4)

    # response = client.execute(
    #     query=query1, substitutions={"login": "JialinC"}
    # )
    # print(response)
    # repository_links = [
    #     "https://github.com/JialinC/Multivariable-Calculus",
    #     "https://github.com/JialinC/xv6"
    # ]
    #
    # miner = RepositoryMiner(client=client)
    #
    # for repository in repository_links:
    #     miner.run(link=repository)
    #
    # miner.to_csv("starter_output.csv")
