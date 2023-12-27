import os
import csv
from github_query.miners.repository_contributors_contribution_miner import RepositoryContributorsContributionMiner
from github_query.github_graphql.authentication import PersonalAccessTokenAuthenticator
from github_query.github_graphql.client import Client

enterprise_client = Client(
    host="github.ncsu.edu", is_enterprise=True,
    authenticator=PersonalAccessTokenAuthenticator(token=os.environ.get("GITHUB_ENTERPRISE_PERSONAL_ACCESS_TOKEN"))
)

# enterprise_client = Client(
#     host="github.ncsu.edu", is_enterprise=True,
#     authenticator=PersonalAccessTokenAuthenticator(token="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")
# )

# path to the input file
input_dir = "E:\Jialin Research\GitHub_GraphQL\GitHub_GraphQL\python_github_query\etc\data\input\\ncsu_repository"
output_dir = "E:\Jialin Research\GitHub_GraphQL\GitHub_GraphQL\python_github_query\etc\data\output\\ncsu_repository"
for filename in os.listdir(input_dir):
    semester = filename[:-4]
    outfile1 = os.path.join(output_dir, "cmu_" + filename)
    outfile2 = os.path.join(output_dir, "ind_" + filename)
    enterprise_miner = RepositoryContributorsContributionMiner(enterprise_client)
    csv_reader = csv.reader(open(os.path.join(input_dir, filename)))
    for row in csv_reader:
        print(f"querying repo: {row[0]}")
        enterprise_miner.run(row[0])
    enterprise_miner.cumulated_contribution.to_csv(outfile1)
    enterprise_miner.individual_contribution.to_csv(outfile2)
print("mission completed:)")






# repository miner
# dirs = ['https://github.ncsu.edu/bchhabr/CSC_ECE_517_Program_2']
#
# for dir in dirs:
#     enterprise_miner.run(dir)
#
# print(enterprise_miner.cumulated_contribution)