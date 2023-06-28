import os
#from helper.helper import print_methods, print_attr
from python_github_query.github_graphql.query import QueryNodePaginator, QueryNode
from python_github_query.github_graphql.authentication import PersonalAccessTokenAuthenticator
from python_github_query.github_graphql.client import Client
from python_github_query.queries.login import UserLoginViewer, UserLogin
from python_github_query.queries.metrics import UserMetrics
from python_github_query.queries.commits import UserCommits
from python_github_query.queries.comments import UserComments

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

    print(UserComments.query)
    print(UserComments.query.path)

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
