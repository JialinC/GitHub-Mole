import os
from datetime import datetime
import time
import csv
from github_query.miners.student_metric_stats_miner import UserMetricStatsMiner
from github_query.github_graphql.authentication import PersonalAccessTokenAuthenticator
from github_query.github_graphql.client import Client

# the start and end time for each semester
semester_start = {'fall_2011': "2011-08-17T00:00:00Z", 'fall_2012': "2012-08-16T00:00:00Z",
                  'fall_2013': "2013-08-21T00:00:00Z", 'fall_2014': "2014-08-20T00:00:00Z",
                  'fall_2015': "2015-08-19T00:35:00Z", 'fall_2016': "2016-08-17T00:00:00Z",
                  'fall_2017': "2017-08-16T00:00:00Z", 'fall_2018': "2018-08-22T00:00:00Z",
                  'fall_2019': "2019-08-21T00:00:00Z", 'fall_2020': "2020-08-10T00:00:00Z",
                  'fall_2021': "2021-08-16T00:00:00Z", 'fall_2022': "2022-08-16T00:00:00Z",
                  'spring_2013': "2013-01-07T00:00:00Z", 'spring_2014': "2014-01-06T00:00:00Z",
                  'spring_2015': "2015-01-07T00:00:00Z", 'spring_2016': "2016-01-06T00:00:00Z",
                  'spring_2017': "2017-01-09T00:00:00Z", 'spring_2018': "2018-01-08T00:00:00Z",
                  'spring_2019': "2019-01-07T00:00:00Z", 'spring_2020': "2020-01-06T00:00:00Z",
                  'spring_2021': "2021-01-19T00:00:00Z", 'spring_2022': "2022-01-10T00:00:00Z",
                  'spring_2023': "2023-01-09T00:00:00Z",
                  'summer_2012': "2012-05-21T00:00:00Z"}

semester_end = {'fall_2011': "2011-12-15T00:00:00Z", 'fall_2012': "2012-12-15T00:00:00Z",
                'fall_2013': "2013-12-18T00:00:00Z", 'fall_2014': "2014-12-17T00:00:00Z",
                'fall_2015': "2015-12-17T00:35:00Z", 'fall_2016': "2016-12-15T00:00:00Z",
                'fall_2017': "2017-12-14T00:00:00Z", 'fall_2018': "2018-12-19T00:00:00Z",
                'fall_2019': "2019-12-10T00:00:00Z", 'fall_2020': "2020-11-25T00:00:00Z",
                'fall_2021': "2021-12-08T00:00:00Z", 'fall_2022': "2022-12-16T00:00:00Z",
                'spring_2013': "2013-05-10T00:00:00Z", 'spring_2014': "2014-05-07T00:00:00Z",
                'spring_2015': "2015-05-08T00:00:00Z", 'spring_2016': "2016-05-06T00:00:00Z",
                'spring_2017': "2017-05-11T00:00:00Z", 'spring_2018': "2018-05-10T00:00:00Z",
                'spring_2019': "2019-05-08T00:00:00Z", 'spring_2020': "2020-05-06T00:00:00Z",
                'spring_2021': "2021-05-10T00:00:00Z", 'spring_2022': "2022-05-04T00:00:00Z",
                'spring_2023': "2023-05-05T00:00:00Z",
                'summer_2012': "2012-08-02T00:00:00Z"}

public_client = Client(
    host="api.github.com", is_enterprise=False,
    authenticator=PersonalAccessTokenAuthenticator(token=os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN"))
)

directory = 'E:\Jialin Research\GitHub_GraphQL\GitHub_GraphQL\python_github_query\etc\data\input\students_input'  # Specify the directory path
out_dir = 'E:\Jialin Research\GitHub_GraphQL\GitHub_GraphQL\python_github_query\etc\data\output\students_output'
# for filename in os.listdir(directory):
for filename in ['fall_2017.csv']:
    semester = filename[:-4]
    outfile = os.path.join(out_dir, filename)
    start = semester_start[semester]
    end = semester_end[semester]
    public_miner = UserMetricStatsMiner(public_client)
    csv_reader = csv.reader(open(os.path.join(directory, filename)))
    for row in csv_reader:
        print(f"querying user: {row[0]}")
        public_miner.run(row[0], end=start)
    public_miner.total_contributions.to_csv(outfile)
print("mission completed:)")

# for filename in ['fall_2015.csv']:
#     outfile += "leftover"