import os

from github_graphql.authentication import PersonalAccessTokenAuthenticator
from github_graphql.client import Client
from miners.repositories import RepositoryMiner

if __name__ == '__main__':
    client = Client(
        host="api.github.com", is_enterprise=False,
        authenticator=PersonalAccessTokenAuthenticator(token=os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN"))
    )

    repository_links = [
        "https://github.com/JialinC/Multivariable-Calculus",
        "https://github.com/JialinC/xv6"
    ]

    miner = RepositoryMiner(client=client)

    for repository in repository_links:
        miner.run(link=repository)

    miner.to_csv("starter_output.csv")
