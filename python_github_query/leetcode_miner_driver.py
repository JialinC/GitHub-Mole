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
# input_file = "E:\Jialin Research\GitHub_GraphQL\GitHub_GraphQL\python_github_query\etc\data\input\leetcode_input\github_2_500.csv"
# output_file = "E:\Jialin Research\GitHub_GraphQL\GitHub_GraphQL\python_github_query\etc\data\output\leetcode_output\github_2_500.csv"
# csv_reader = csv.reader(open(input_file))
# for row in csv_reader:
#     print(f"querying user: {row[0]}")
#     public_miner.run(row[0])
#public_miner.total_contributions.to_csv(output_file)

for row in ['wjlee-ling', 'Edwu29', 'baogedd']:
    print(f"querying user: row")
    public_miner.run(row)
public_miner.total_contributions.to_csv("tttt.csv")