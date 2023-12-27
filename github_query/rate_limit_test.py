import os
import re
import csv
from github_query.github_graphql.authentication import PersonalAccessTokenAuthenticator
from github_query.github_graphql.client import Client
from github_query.queries.time_range_contributions.user_contributions_collection import UserContributionsCollection
from github_query.queries.utils.query_cost import QueryCost
import github_query.util.helper as helper

public_client = Client(
    host="api.github.com", is_enterprise=False,
    authenticator=PersonalAccessTokenAuthenticator(token=os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN"))
)

enterprise_client = Client(
    host="github.ncsu.edu", is_enterprise=True,
    authenticator=PersonalAccessTokenAuthenticator(token=os.environ.get("GITHUB_ENTERPRISE_PERSONAL_ACCESS_TOKEN"))
)
string = UserContributionsCollection().substitute(**{"user": "JialinC", "start": "2020-02-07T18:11:20Z", "end": "2021-02-07T18:11:20Z"}).__str__()
match = re.search(r'query\s*{(?P<content>.+)}', string)
print(match.group('content'))
print(QueryCost(match.group('content')))

response = public_client.execute(query=QueryCost(match.group('content')), substitutions={"dryrun": True})

print(response)

tf, resetat = helper.have_rate_limit(public_client,UserContributionsCollection(),{"user": "JialinC", "start": "2020-02-07T18:11:20Z", "end": "2021-02-07T18:11:20Z"})
print(tf,resetat)