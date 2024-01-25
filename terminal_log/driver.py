import os
import csv
from github_query.github_graphql.authentication import PersonalAccessTokenAuthenticator
from github_query.github_graphql.client import Client
from github_query.miners.repository_contributors_contribution_miner import RepositoryContributorsContributionMiner

public_client = Client(
    host="api.github.com", is_enterprise=False,
    authenticator=PersonalAccessTokenAuthenticator(token=os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN"))
)

enterprise_client = Client(
    host="github.ncsu.edu", is_enterprise=True,
    authenticator=PersonalAccessTokenAuthenticator(token=os.environ.get("GITHUB_ENTERPRISE_PERSONAL_ACCESS_TOKEN"))
)

public_miner = RepositoryContributorsContributionMiner(public_client)
enterprise_miner = RepositoryContributorsContributionMiner(enterprise_client)

input_file = "E:\\Jialin Research\\GitHub_GraphQL\\GitHub_GraphQL\\python_github_query\\etc\\data\\input\\test_input" \
             "\\test_repositories\\test_repositories_public.csv "

csv_reader = csv.reader(open(input_file))
for row in csv_reader:
    public_miner.run(row[0])

print(public_miner.cumulated_contribution)
print(public_miner.individual_contribution)

# the start and end time for each semester
s_start = {'Fall 2011':"2011-08-17T00:00:00Z", 'Fall 2012':"2012-08-16T00:00:00Z",
            'Fall 2013':"2013-08-21T00:00:00Z", 'Fall 2014':"2014-08-20T00:00:00Z",
            'Fall 2015':"2015-08-19T00:35:00Z", 'Fall 2016':"2016-08-17T00:00:00Z",
            'Fall 2017':"2017-08-16T00:00:00Z", 'Fall 2018':"2018-08-22T00:00:00Z",
            'Fall 2019':"2019-08-21T00:00:00Z", 'Fall 2020':"2020-08-10T00:00:00Z",
            'Fall 2021':"2021-08-16T00:00:00Z", 'Fall 2022':"2022-08-16T00:00:00Z",
            'Spring 2013':"2013-01-07T00:00:00Z", 'Spring 2014':"2014-01-06T00:00:00Z",
            'Spring 2015':"2015-01-07T00:00:00Z", 'Spring 2016':"2016-01-06T00:00:00Z",
            'Spring 2017':"2017-01-09T00:00:00Z", 'Spring 2018':"2018-01-08T00:00:00Z",
            'Spring 2019':"2019-01-07T00:00:00Z", 'Spring 2020':"2020-01-06T00:00:00Z",
            'Spring 2021':"2021-01-19T00:00:00Z", 'Spring 2022':"2022-01-10T00:00:00Z",
            'Spring 2023':"2023-01-09T00:00:00Z",
            'Summer 2012':"2012-05-21T00:00:00Z"}

s_end = {'Fall 2011':"2011-12-15T00:00:00Z", 'Fall 2012':"2012-12-15T00:00:00Z",
            'Fall 2013':"2013-12-18T00:00:00Z", 'Fall 2014':"2014-12-17T00:00:00Z",
            'Fall 2015':"2015-12-17T00:35:00Z", 'Fall 2016':"2016-12-15T00:00:00Z",
            'Fall 2017':"2017-12-14T00:00:00Z", 'Fall 2018':"2018-12-19T00:00:00Z",
            'Fall 2019':"2019-12-10T00:00:00Z", 'Fall 2020':"2020-11-25T00:00:00Z",
            'Fall 2021':"2021-12-08T00:00:00Z", 'Fall 2022':"2022-12-16T00:00:00Z",
            'Spring 2013':"2013-05-10T00:00:00Z", 'Spring 2014':"2014-05-07T00:00:00Z",
            'Spring 2015':"2015-05-08T00:00:00Z", 'Spring 2016':"2016-05-06T00:00:00Z",
            'Spring 2017':"2017-05-11T00:00:00Z", 'Spring 2018':"2018-05-10T00:00:00Z",
            'Spring 2019':"2019-05-08T00:00:00Z", 'Spring 2020':"2020-05-06T00:00:00Z",
            'Spring 2021':"2021-05-10T00:00:00Z", 'Spring 2022':"2022-05-04T00:00:00Z",
            'Spring 2023':"2023-05-05T00:00:00Z",
            'Summer 2012':"2012-08-02T00:00:00Z"}

header_row = ("GitHub",
              "creationDate",
              "endDate",
              "lifeSpan",
              "RestrictedContributionsCount",
              "CommitContributions",
              "totalIssueContributions",
              "totalPullRequestContributions",
              "totalPullRequestReviewContributions",
              "gists",
              "repositoryDiscussions",
              "commitComments",
              "issueComments",
              "gistComments",
              "repositoryDiscussionComments",
              "totalRepositoryContributions",
              "repoACount", "forkACount", "stargazerACount", "Awatchers", "repoASize", "AlanguageInfo",
              "repoBCount", "forkBCount", "stargazerBCount", "Bwatchers", "repoBSize", "BlanguageInfo",
              "repoCCount", "forkCCount", "stargazerCCount", "Cwatchers", "repoCSize", "ClanguageInfo",
              "repoDCount", "forkDCount", "stargazerDCount", "Dwatchers", "repoDSize", "DlanguageInfo"
                    )







# Original dictionary
original_dict = {'old_key1': 'value1', 'old_key2': 'value2', 'old_key3': 'value3'}

# Create a new dictionary with updated keys
updated_dict = {new_key: original_dict[old_key] for old_key, new_key in [('old_key1', 'new_key1'), ('old_key2', 'new_key2'), ('old_key3', 'new_key3')]}

sdshao
wangdavid84
jdfsdbfadnotexist
