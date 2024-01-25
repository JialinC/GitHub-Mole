import os
import csv
from github_query.miners.student_metric_stats_miner import UserMetricStatsMiner
from github_query.github_graphql.authentication import PersonalAccessTokenAuthenticator
from github_query.github_graphql.client import Client

public_client = Client(
    host="api.github.com", is_enterprise=False,
    authenticator=PersonalAccessTokenAuthenticator(token=os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN"))
)

enterprise_client = Client(
    host="github.ncsu.edu", is_enterprise=True,
    authenticator=PersonalAccessTokenAuthenticator(token=os.environ.get("GITHUB_ENTERPRISE_PERSONAL_ACCESS_TOKEN"))
)

public_miner = UserMetricStatsMiner(public_client)
# enterprise_miner = UserMetricStatsMiner(enterprise_client)

input_file = "E:\\Jialin Research\\GitHub_GraphQL\\GitHub_GraphQL\\python_github_query\\etc\\data\\input\\test_input" \
             "\\test_accounts\\test_accounts_public.csv"

end = "2022-07-10T18:11:20Z"
csv_reader = csv.reader(open(input_file))
for row in csv_reader:
    public_miner.run(row[0], start=None, end=end)

public_miner.total_contributions.to_csv("test.csv")
with open("output_file.csv", 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for element in public_miner.exceptions:
        writer.writerow([element])
