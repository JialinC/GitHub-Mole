import json
import re
from collections import defaultdict

import pandas as pd

from github_graphql.client import Client
from queries.repository_graph import RepositoryGraph


class RepositoryMiner:
    """
    Helps mining repository data.
    """
    def __init__(self, client: Client):
        self._client = client
        self.data = []

    def run(self, link: str):
        """
        Collect data for a repository using a link.
        Args:
            link: Link to the repository
        """
        owner, repository = RepositoryMiner.get_owner_and_name(link)

        query = RepositoryGraph().query

        response = self._client.execute(
            query=query, substitutions={"user": owner, "repository": repository}
        )

        contributor_stats = self._client.rest.get(f"/repos/{owner}/{repository}/stats/contributors")

        data = RepositoryGraph.flatten_result(response)
        data["repository_contribution_stats"] = self._aggregate_contributor_stats(contributor_stats)

        self.data.append(data)

    @staticmethod
    def get_owner_and_name(link: str):
        """
        Parse the URL and identifies the author login and the repository name.
        Args:
            link: Link to parse

        Returns:
            Author login and repository name
        """
        pattern = (
            r"(?P<protocols>(git\+)?(?P<protocol>https))://(?P<domain>.+?)(?P<port>:[0-9]+)?"
            r"(?P<pathname>/(?P<owner>[^/]+?)/"
            r"(?P<groups_path>.*?)?(?(groups_path)/)?(?P<repo>[^/]+?)(?:(\.git)?(/)?)"
            r"(?P<path_raw>(/blob/|/-/tree/).+)?)$"
        )

        compiled_pattern = re.compile(pattern)
        match = compiled_pattern.match(link)

        assert match is not None, f"Link '{link}' is invalid"

        return match.group("owner"), match.group("repo")

    def to_csv(self, path: str):
        """
        Writes teh collected data to a CSV.
        Args:
            path: Path of the output CSV
        """
        df = pd.DataFrame(self.data)

        for column in df.columns:
            if isinstance(df[column][0], dict) or isinstance(df[column][0], list):
                df[column] = df[column].apply(json.dumps)

        df.to_csv(path)

    @staticmethod
    def _aggregate_contributor_stats(response: dict):
        """
        Utility to aggregate raw data from contribution stats.
        Args:
            response: Raw contribution stats

        Returns:
            Aggregated contribution stats
        """
        def dict_agg(data: list):
            dict_ = defaultdict(int)

            keys = {
                "a": "additions",
                "d": "deletions",
                "c": "commits"
            }

            for _row in data:
                for key, value in _row.items():
                    if key in keys:
                        dict_[keys[key]] += value

            return dict(dict_)

        return {
            data["author"]["login"]: dict_agg(data["weeks"])
            for data in response
        }
