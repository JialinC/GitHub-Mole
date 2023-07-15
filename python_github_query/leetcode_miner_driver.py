import os
import csv
from python_github_query.miners.leetcode_user_miner import LeetcodeUserMiner
from python_github_query.github_graphql.authentication import PersonalAccessTokenAuthenticator
from python_github_query.github_graphql.client import Client

public_client = Client(
    host="api.github.com", is_enterprise=False,
    authenticator=PersonalAccessTokenAuthenticator(token=os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN"))
)

public_miner = LeetcodeUserMiner(public_client)
# path to the input file
input_file = "path/to/your/input/file"

csv_reader = csv.reader(open(input_file))
for row in csv_reader:
    print(f"querying user: {row[0]}")
    public_miner.run(row[0])

public_miner.total_contributions.to_csv("query_output.csv")
with open("exceptions.csv", 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for element in public_miner.exceptions:
        writer.writerow([element])
