import os
from datetime import datetime
import time
import csv
from github_query.miners.student_metric_stats_miner import UserMetricStatsMiner
from github_query.github_graphql.authentication import PersonalAccessTokenAuthenticator
from github_query.github_graphql.client import Client

# the start and end time for each semester
start = "2023-10-08T00:00:00Z"
token = "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" # os.environ.get("GITHUB_ENTERPRISE_PERSONAL_ACCESS_TOKEN")
enterprise_client = Client(
    host="github.ncsu.edu", is_enterprise=True,
    authenticator=PersonalAccessTokenAuthenticator(token=token)
)

file_name = 'p4_fall_2023.csv'
input = 'E:\Jialin Research\GitHub_GraphQL\GitHub_GraphQL\python_github_query\etc\data\input\students_input\p4_fall_2023.csv'  # Specify the directory path
out_dir = 'E:\Jialin Research\GitHub_GraphQL\GitHub_GraphQL\python_github_query\etc\data\output\students_output'
# for filename in os.listdir(directory):
outfile = os.path.join(out_dir, file_name)
enterprise_miner = UserMetricStatsMiner(enterprise_client)
csv_reader = csv.reader(open(input))
for row in csv_reader:
    print(f"querying user: {row[0]}")
    enterprise_miner.run(row[0], end=start)
enterprise_miner.total_contributions.to_csv(outfile)
print("mission completed:)")
