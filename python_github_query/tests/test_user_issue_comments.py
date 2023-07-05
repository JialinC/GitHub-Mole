import pytest
from python_github_query.queries.user_issue_comments import UserIssueComments


@pytest.mark.usefixtures("graphql_client")
class TestUserIssueComments:
    def test_user_issue_comments_public(self):
        expected_data1 = {'user': {'login': 'JialinC', 'issueComments': {'totalCount': 10, 'nodes': [{
            'body': 'Oh, I think I actually do not have specific case. In my understanding, I\nthink the go test command is for pkg, so I basically just compile and run\nthe game of life instead of treating it like pkg.\n\nOn Mon, Aug 24, 2020 at 10:35 PM Rahul Yedida <notifications@github.com>\nwrote:\n\n> J, could you point to where the test cases for Go are? Specifically, do\n> you have cases like blinker?\n>\n> —\n> You are receiving this because you authored the thread.\n> Reply to this email directly, view it on GitHub\n> <https://github.com/yrahul3910/se-hw2/pull/6#issuecomment-679466974>, or\n> unsubscribe\n> <https://github.com/notifications/unsubscribe-auth/AJGDROM6FWRKOEEUC2GAM33SCMPPHANCNFSM4QKEE46Q>\n> .\n>\n',
            'createdAt': '2020-08-25T02:57:12Z'},
            {
                'body': 'So, you want me to treat game of life as a pkg then use "go test"? I think\nin the .yml what I did is just "go run".\n\nOn Mon, Aug 24, 2020 at 10:56 PM Jialin Cui <cjl742952519@gmail.com> wrote:\n\n> Oh, I think I actually do not have specific case. In my understanding, I\n> think the go test command is for pkg, so I basically just compile and run\n> the game of life instead of treating it like pkg.\n>\n> On Mon, Aug 24, 2020 at 10:35 PM Rahul Yedida <notifications@github.com>\n> wrote:\n>\n>> J, could you point to where the test cases for Go are? Specifically, do\n>> you have cases like blinker?\n>>\n>> —\n>> You are receiving this because you authored the thread.\n>> Reply to this email directly, view it on GitHub\n>> <https://github.com/yrahul3910/se-hw2/pull/6#issuecomment-679466974>, or\n>> unsubscribe\n>> <https://github.com/notifications/unsubscribe-auth/AJGDROM6FWRKOEEUC2GAM33SCMPPHANCNFSM4QKEE46Q>\n>> .\n>>\n>\n',
                'createdAt': '2020-08-25T02:58:52Z'}],
                                                                         'pageInfo': {
                                                                             'endCursor': 'Y3Vyc29yOnYyOpHOKIAB2Q==',
                                                                             'hasNextPage': True}}}}
        expected_data2 = {'user': {'login': 'JialinC', 'issueComments': {'totalCount': 10, 'nodes': [{
            'body': 'Implemented create channel if channel not exist.\r\nAfter detected changes in the postman collection, the code will check whether a channel for this collection has already existed or not. If the channel existed, then the bot post the message there. If the channel does not exist then we create a new one for that collection and post the message in the new channel.',
            'createdAt': '2020-10-13T03:45:35Z'},
            {
                'body': '@smdupor Hi Steven, I find the place where the <tag id = "snake_case"> is generated. So there is a class/model called TagPrompt in app/models/tag_prompt.rb, where each tag is generated as:\r\n\r\nelement_id = answer.id.to_s + \'_\' + self.id.to_s\r\ncontrol_id = "tag_prompt_" + element_id\r\n\r\nThis model also generated other tags in this format, I could of course try to refactor this model, but since it is a model existing there not only for the issue that we are working on but also potentially used by others, do you think we should still refactor this? Thanks. ',
                'createdAt': '2021-03-09T02:33:32Z'}],
                                                                         'pageInfo': {
                                                                             'endCursor': 'Y3Vyc29yOnYyOpHOL0iTFw==',
                                                                             'hasNextPage': True}}}}

        count = 0
        for response in self.client.execute(query=UserIssueComments(),
                                            substitutions={"user": "JialinC", "pg_size": 2}):
            if count == 0:
                assert response == expected_data1
            elif count == 1:
                assert response == expected_data2
            else:
                break
            count += 1

    def test_user_issue_comments_enterprise(self):
        expected_data1 = {'user': {'login': 'jcui9', 'issueComments': {'totalCount': 8, 'nodes': [{
            'body': 'Complete all the levels in the following “Main” topics of the Git Tutorial (1) Introduction Sequence, (2) Ramping Up, (3) Moving Work Around, (4) A Mixed Bag',
            'createdAt': '2021-01-29T22:07:22Z'},
            {'body': 'Done as required',
             'createdAt': '2021-01-30T02:18:49Z'}],
                                                                       'pageInfo': {
                                                                           'endCursor': 'Y3Vyc29yOnYyOpHOAAEccw==',
                                                                           'hasNextPage': True}}}}
        expected_data2 = {'user': {'login': 'jcui9', 'issueComments': {'totalCount': 8, 'nodes': [
            {'body': 'Done as required', 'createdAt': '2021-01-30T02:19:14Z'},
            {'body': 'Done in the README', 'createdAt': '2021-01-30T02:19:38Z'}],
                                                                       'pageInfo': {
                                                                           'endCursor': 'Y3Vyc29yOnYyOpHOAAEcdQ==',
                                                                           'hasNextPage': True}}}}

        count = 0
        for response in self.enterprise_client.execute(query=UserIssueComments(),
                                                       substitutions={"user": "jcui9", "pg_size": 2}):
            if count == 0:
                assert response == expected_data1
            elif count == 1:
                assert response == expected_data2
            else:
                break
            count += 1
