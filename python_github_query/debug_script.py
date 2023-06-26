import os
#from helper.helper import print_methods, print_attr
from github_graphql.authentication import PersonalAccessTokenAuthenticator
from github_graphql.client import Client
from queries.login import UserLoginViewer, UserLogin
from github_graphql.query import Query, QueryNode
from miners.repositories import RepositoryMiner
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
    # UserLoginViewer
    response1 = requests.post(
        path1,
        json={'query': 'query { viewer { login } }'},
        headers=header1
    )
    print(response1.json())

    response2 = client.execute(
         query=UserLoginViewer.query, substitutions={}
    )
    print(response2)
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
    #
    # # UserLogin
    # response1 = requests.post(
    #     path1,
    #     json={'query': 'query { user(login: "JialinC") { login name email createdAt}}'},
    #     headers=header1
    # )
    # print(response1.json())

    # response2 = client.execute(
    #     query=UserLoginViewer.query, substitutions={}
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
