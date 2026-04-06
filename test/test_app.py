import unittest
from enum import Enum
from app import *
from datetime import datetime
import sys
class AppTestCase(unittest.TestCase):
    mary = {}
    nick = {}
    olga = {}

    class Mary(Enum):
        USERNAME = "mary"
        EMAIL = "mary@gmail.com"
        FIRST_NAME = "mary"
        LAST_NAME = "birckbeck"
        PASSWORD = "password"

    class Nick(Enum):
        USERNAME = "nick"
        EMAIL = "nick@gmail.com"
        FIRST_NAME = "nick"
        LAST_NAME = "uni"
        PASSWORD = "password"

    class Olga(Enum):
        USERNAME = "olga"
        EMAIL = "olga@gmail.com"
        FIRST_NAME = "olga"
        LAST_NAME = "london"
        PASSWORD = "password"

    @classmethod
    def setUp(self):

        self.mary = api_register(self.Mary.USERNAME.value,self.Mary.EMAIL.value,self.Mary.FIRST_NAME.value,
                                 self.Mary.LAST_NAME.value,self.Mary.PASSWORD.value)[1]


        self.nick = api_register(self.Nick.USERNAME.value,self.Nick.EMAIL.value,self.Nick.FIRST_NAME.value,
                                 self.Nick.LAST_NAME.value,self.Nick.PASSWORD.value)[1]

        self.olga = api_register(self.Olga.USERNAME.value,self.Olga.EMAIL.value,self.Olga.FIRST_NAME.value,
                                 self.Olga.LAST_NAME.value,self.Olga.PASSWORD.value)[1]

    @classmethod
    def tearDown(self):
        api_delete_all_thinkers()
        api_delete_all_thoughts()

    def test_TC1a_registration_mary(self):
        """|01|TC01|TC01-Mary|Olga, Nick and Mary register in the application and access the API.|
        Test passes if the user has successfully registered and accessed the api if their user data has been loaded to the test-case object.|"""
        self.assertEqual(self.Mary.USERNAME.value, self.mary["username"],"TC1 hihi")


    def test_TC1b_api_access(self):
        """|02|TC01|TC01|Test user can access the api(root, access free).|
        Test passes if the user can successfully access the landing page. No authentication required as no resources are accessed.|"""
        responseCode, message = api_get()
        self.assertEqual(responseCode, 200)


    def test_TC1a_registration_nick(self):
        """|03|TC01|TC01-Nick|Olga, Nick and Mary register in the application and access the API.|
        Test passes if the user has successfully registered and accessed the api if their user data has been loaded to the test-case object.|"""
        self.assertEqual(self.Nick.USERNAME.value, self.nick["username"])


    def test_TC1a_registration_olga(self):
        """|04|TC01|TC01-Olga|Olga, Nick and Mary register in the application and access the API.|
        Test passes if the user has successfully registered and accessed the api if their user data has been loaded to the test-case object.|"""
        self.assertEqual(self.Olga.USERNAME.value, self.olga["username"])

    def test_TC2_token_receival_mary(self):
        """|05|TC02|TC02-Mary|Olga, Nick and Mary will use the oAuth v2 authorisation service to get their tokens.|
        Test passes if user can use their registration data to obtain an oAuth token.|"""
        responseCode, authJSON = api_signin(self.Mary.USERNAME.value,self.Mary.PASSWORD.value)
        auth_token = authJSON["auth-token"]
        self.assertEqual(responseCode, 200)
        self.assertIsNotNone(auth_token)

    def test_TC2_token_receival_nick(self):
        """|06|TC02|TC02-Nick|Olga, Nick and Mary will use the oAuth v2 authorisation service to get their tokens.|
        Test passes if user can use their registration data to obtain an oAuth token.|"""
        responseCode, authJSON = api_signin(self.Nick.USERNAME.value,self.Nick.PASSWORD.value)
        auth_token = authJSON["auth-token"]
        self.assertEqual(responseCode, 200)
        self.assertIsNotNone(auth_token)

    def test_TC2_token_receival_olga(self):
        """|07|TC02|TC02-Olga|Olga, Nick and Mary will use the oAuth v2 authorisation service to get their tokens.|
        Test passes if user can use their registration data to obtain an oAuth token.|"""
        responseCode, authJSON = api_signin(self.Olga.USERNAME.value,self.Olga.PASSWORD.value)
        auth_token = authJSON["auth-token"]
        self.assertEqual(responseCode, 200)
        self.assertIsNotNone(auth_token)

    def test_TC3_api_call_no_auth(self):
        """|08|TC03|TC03|Olga calls the API (any endpoint) without using a token.
        This call should be unsuccessful as the user is unauthorised.|
        Test passes if a response code not equal to 200 is returned.|"""
        responseCode, message = api_get_thinker()
        self.assertNotEqual(responseCode, 200)

    def post_using_token(self,user:Enum):

        responseCodeSignin, authJSON = api_signin(user.USERNAME.value,user.PASSWORD.value)

        auth_token = authJSON["auth-token"]
        request_keys = ["title", "description", "detail", "echoChamber", "image","auth_token"]
        request_values = ["test_title",
                          "test_description_"+user.USERNAME.value,"test_comment_"+user.USERNAME.value,
                          "test_chamber_"+user.USERNAME.value,"http://goodurlby"+user.USERNAME.value+".com",auth_token]

        request_body = {}
        for key in request_keys:
            for value in request_values:
                request_body[key] = value
                request_values.remove(value)
                break

        return api_post_thought(**request_body), request_body


    def test_TC4_olga_post_with_token(self):
        """|09|TC04|TC04-Olga|Olga posts a text using her token.|
        Test passes if the contents of the request body and the response body match.|"""
        response, request =  self.post_using_token(self.Olga)
        responseCode, postedThought = response
        request_title, request_description, request_detail, request_echoChamber, request_image, request_token = request.values()

        self.assertEqual(responseCode, 200)
        self.assertEqual(postedThought["title"], request_title)
        self.assertEqual(postedThought["description"], request_description)
        self.assertEqual(postedThought["detail"], request_detail)
        self.assertEqual(postedThought["echoChamber"], request_echoChamber)
        self.assertEqual(postedThought["image"], request_image)

    def test_TC5_nick_post_with_token(self):
        """|10|TC05|TC05-Nick|Nick posts a text using her token.|
        Test passes if the contents of the request body and the response body match.|"""
        response, request =  self.post_using_token(self.Nick)
        responseCode, postedThought = response
        request_title, request_description, request_detail, request_echoChamber, request_image, request_token = request.values()

        self.assertEqual(responseCode, 200)
        self.assertEqual(postedThought["title"], request_title)
        self.assertEqual(postedThought["description"], request_description)
        self.assertEqual(postedThought["detail"], request_detail)
        self.assertEqual(postedThought["echoChamber"], request_echoChamber)
        self.assertEqual(postedThought["image"], request_image)

    def test_TC6_mary_post_with_token(self):
        """|11|TC06|TC06-Mary|Mary posts a text using her token.|
        Test passes if the contents of the request body and the response body match.|"""
        response, request =  self.post_using_token(self.Mary)
        responseCode, postedThought = response
        request_title, request_description, request_detail, request_echoChamber, request_image, request_token = request.values()

        self.assertEqual(responseCode, 200)
        self.assertEqual(postedThought["title"], request_title)
        self.assertEqual(postedThought["description"], request_description)
        self.assertEqual(postedThought["detail"], request_detail)
        self.assertEqual(postedThought["echoChamber"], request_echoChamber)
        self.assertEqual(postedThought["image"], request_image)


    def miniwall_is_reverse_chronological(self,auth_token):
        responseCode, miniWall = api_get_thought(auth_token=auth_token)
        format = "%Y-%m-%dT%H:%M:%S.%fZ"
        timestampsStr = [comment["timestamp"] for comment in miniWall]
        datetimes =[datetime.strptime(timestamp,format) for timestamp in timestampsStr]

        sortedDatetimes = sorted(datetimes,reverse=True)

        return (datetimes == sortedDatetimes) #list and sorted list are eqaul if wall is reversechrono

    def reach_state_to_TC6(self):
        #Coursework brief specifies that mary posts last however I will her post first so
        # that we can demonstrate TC15. If Mary posts last, her post will always show up first on the wall
        #regardless of the amount of likes it has.
        self.post_using_token(self.Mary)
        self.post_using_token(self.Nick)
        self.post_using_token(self.Olga)


    def test_TC7_nick_get_is_reverse_chronological(self):
        """|12|TC07|TC07-Nick| Nick and Olga browse available posts in reverse chronological order in the MiniWall;
        there should be three posts available.| Test passes if a sorted list of the posts included in the api response 
        is in chronological order.|"""
        self.reach_state_to_TC6() #Nick, Mary and Olga will post a thought

        responseCodeSignin, authJSON = api_signin(self.Nick.USERNAME.value,self.Nick.PASSWORD.value)
        auth_token = authJSON["auth-token"]
        wallIsReverseChronological = self.miniwall_is_reverse_chronological(auth_token)
        self.assertTrue(wallIsReverseChronological)


    def test_TC7_olga_get_is_reverse_chronological(self):
        """|13|TC07|TC07-Olga| Nick and Olga browse available posts in reverse chronological order in the MiniWall;
        there should be three posts available.| Test passes if a sorted list of the posts included in the api response
        is in chronological order.|"""
        self.reach_state_to_TC6() #Nick, Mary and Olga will post a thought

        responseCodeSignin, authJSON = api_signin(self.Olga.USERNAME.value,self.Olga.PASSWORD.value)
        auth_token = authJSON["auth-token"]
        wallIsReverseChronological = self.miniwall_is_reverse_chronological(auth_token)
        self.assertTrue(wallIsReverseChronological)

    def get_test_case_comment(self,user_API_Id:str,user:Enum):
        auth_token = api_signin(user.USERNAME.value,user.PASSWORD.value)[1]["auth-token"]
        allThoughts = api_get_thought(auth_token)[1]
        userThoughtInLIst = [thought for thought in allThoughts if (thought["thinker"] == user_API_Id)]
        userThought = userThoughtInLIst[0]
        return userThought

    def reach_state_to_TC8(self):
        self.reach_state_to_TC6()
        nickAuth_token = api_signin(self.Nick.USERNAME.value,self.Nick.PASSWORD.value)[1]["auth-token"]
        olgaAuth_token = api_signin(self.Olga.USERNAME.value,self.Olga.PASSWORD.value)[1]["auth-token"]

        maryThought = self.get_test_case_comment(self.mary["_id"], self.Mary)
        maryThoughtId = maryThought["_id"]

        nickComment1 = api_comment_thought(maryThoughtId,"Test1",nickAuth_token) #Nick comments1
        olgaComment1 = api_comment_thought(maryThoughtId,"Test2",olgaAuth_token) #Olga comments1
        nickComment2 = api_comment_thought(maryThoughtId,"Test3",nickAuth_token) #Nick comments2
        olgaComment2 = api_comment_thought(maryThoughtId,"Test4",olgaAuth_token) #Olga comments2

        response = {
            "nickComment1":nickComment1,"olgaComment1":olgaComment1,
            "nickComment2":nickComment2,"olgaComment2":olgaComment2
        }

        return response

    def test_TC8_nick_olga_comment_marry_post(self):
        """|13|TC08|TC08| Nick and Olga comment Mary’s post in a round-robin fashion (one after the other).|
        Test passes if the response data matches the request data. Additionally, all response codes must be coded 200.|"""
        stateTC8 = self.reach_state_to_TC8()
        nickComment1, olgaComment1, nickComment2, olgaComment2 = stateTC8["nickComment1"], stateTC8["olgaComment1"],stateTC8["nickComment2"], stateTC8["olgaComment2"]
        statusOk = (nickComment1[0]==nickComment2[0]==olgaComment1[0]==olgaComment2[0]==200)
        modifiedOk = (nickComment1[1]["modifiedCount"]==nickComment2[1]["modifiedCount"]==olgaComment1[1]["modifiedCount"]==olgaComment2[1]["modifiedCount"]==1)
        acknowledgedTrue = (nickComment1[1]["acknowledged"]==nickComment2[1]["acknowledged"]==olgaComment1[1]["acknowledged"]==olgaComment2[1]["acknowledged"]==True)
        self.assertTrue(statusOk)
        self.assertTrue(modifiedOk)
        self.assertTrue(acknowledgedTrue)



    def test_TC9_marry_comment_marry_post(self):
        """|14|TC09|TC09-Mary| Mary comments her post. This call should be unsuccessful; an owner cannot comment owned posts.|
        Test passes if response code is 403|"""
        self.reach_state_to_TC8()
        marryAuth_token = api_signin(self.Mary.USERNAME.value,self.Mary.PASSWORD.value)[1]["auth-token"]
        maryThought = self.get_test_case_comment(self.mary["_id"], self.Mary)
        maryThoughtId = maryThought["_id"]

        responseCode, responseBody = api_comment_thought(maryThoughtId,"Test1",marryAuth_token)
        self.assertEqual(403,responseCode)

    def test_TC10_mary_get_is_reverse_chronological(self):
        """|15|TC10|TC10-Mary| Mary can see posts in reverse chronological order (newest posts are on the top as there are no likes yet).|
        Test passes if a sorted (by datetime) list of the comments in the response are in reverse chronological order.|"""
        self.reach_state_to_TC8()
        responseCodeSignin, authJSON = api_signin(self.Mary.USERNAME.value,self.Mary.PASSWORD.value)
        auth_token = authJSON["auth-token"]
        wallIsReverseChronological = self.miniwall_is_reverse_chronological(auth_token)
        self.assertTrue(wallIsReverseChronological)

    def test_TC11_mary_get_comments_on_mary_post(self):
        """|16|TC11|TC11-Mary| Mary can see the comments for her posts.|
        Test passes the comment data in the response body match that of the comments sent by Nick and Olga.|"""
        stateTC8 = self.reach_state_to_TC8()
        maryAuth_token = api_signin(self.Mary.USERNAME.value,self.Mary.PASSWORD.value)[1]["auth-token"]
        maryThought = self.get_test_case_comment(self.mary["_id"], self.Mary)
        maryThoughtId = maryThought["_id"]

        responseCode, responseCommentsMaryThought = api_get_thought_comments(maryAuth_token,maryThoughtId)
        commentsMaryThought = responseCommentsMaryThought["comments"]
        numberCommentsSent = len(stateTC8)
        numberCommentsReceived = len(commentsMaryThought)

        self.assertEqual(numberCommentsSent,numberCommentsReceived)

    def reach_state_to_TC12(self):
        self.reach_state_to_TC8()

        nickAuth_token = api_signin(self.Nick.USERNAME.value,self.Nick.PASSWORD.value)[1]["auth-token"]
        olgaAuth_token = api_signin(self.Olga.USERNAME.value,self.Olga.PASSWORD.value)[1]["auth-token"]

        maryThought = self.get_test_case_comment(self.mary["_id"], self.Mary)
        maryThoughtId = maryThought["_id"]

        nickResponse = api_like_thought(maryThoughtId,nickAuth_token)
        olgaResponse = api_like_thought(maryThoughtId,olgaAuth_token)

        return {"nickResponse":nickResponse,"olgaResponse":olgaResponse}

    def test_TC12_nick_olga_like_mary_thought(self):
        """|17|TC12|TC12| Nick and Olga like Mary’s posts.|
        Test passes the number of likes on liked comment is 2.|"""
        stateTC12 = self.reach_state_to_TC12()
        nickResponse, olgaResponse = stateTC12["nickResponse"], stateTC12["olgaResponse"]
        nickResponseCode, nickResponseBody = nickResponse
        olgaResponseCode, olgaResponseBody = olgaResponse

        maryThought = self.get_test_case_comment(self.mary["_id"],self.Mary)
        maryThoughtLikes = maryThought["score"]

        statusOk = (nickResponseCode==olgaResponseCode==200)
        modifiedOk = (nickResponseBody["modifiedCount"]==olgaResponseBody["modifiedCount"]==1)
        acknowledgedTrue = (nickResponseBody["acknowledged"]==olgaResponseBody["acknowledged"]==True)

        self.assertTrue(statusOk)
        self.assertTrue(modifiedOk)
        self.assertTrue(acknowledgedTrue)
        self.assertEqual(2,maryThoughtLikes)


    def test_TC13_mary_likes_own_post(self):
        """|18|TC13|TC13-Mary| Mary likes her posts. This call should be unsuccessful; an owner cannot like their posts.|
        Test passes response code is 403|"""
        self.reach_state_to_TC12()
        maryAuth_token = api_signin(self.Mary.USERNAME.value,self.Mary.PASSWORD.value)[1]["auth-token"]
        maryThought = self.get_test_case_comment(self.mary["_id"], self.Mary)
        maryThoughtId = maryThought["_id"]
        likeResponse = api_like_thought(maryThoughtId,maryAuth_token)
        responseCode, responseBody = likeResponse
        self.assertEqual(403,responseCode)

    def test_TC14_mary_sees_likes_own_post(self):
        """|19|TC14|TC14-Mary| Mary can see that there are two likes in her posts.|
        Test passes if the number of likes on the comment in the response body is 2|"""
        self.reach_state_to_TC12()
        maryThought = self.get_test_case_comment(self.mary["_id"], self.Mary)
        maryThoughtLikes = maryThought["score"]
        self.assertEqual(2,maryThoughtLikes)

    def test_TC15_nick_sees_posts_marys_on_top(self):
        """|20|TC15|TC15-Nick| Nick can see the list of posts, since Mary’s post has two likes it is shown at the top,
         even though her comment is the oldest|
        Test passes if the first post in a sorted list of comments in the response body matches the _id of Mary's post."""
        self.reach_state_to_TC12()
        maryComment = self.get_test_case_comment(self.mary["_id"],self.Mary)
        maryCommentId = maryComment["_id"]

        responseCodeSignin, authJSON = api_signin(self.Nick.USERNAME.value,self.Nick.PASSWORD.value)
        auth_token = authJSON["auth-token"]
        responseCode, nicksViewOfminiWall = api_get_thought(auth_token)
        nicksVieOfminiWallFirstPost = nicksViewOfminiWall[0]
        nicksVieOfminiWallFirstPostId = nicksVieOfminiWallFirstPost["_id"]
        self.assertEqual(maryCommentId,nicksVieOfminiWallFirstPostId)





#Template for test report credited to: https://stackoverflow.com/questions/5360833/how-do-i-run-multiple-classes-in-a-single-test-suite-in-python-using-unit-testin
def main(out = sys.stderr, verbosity = 2):
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    unittest.TextTestRunner(out, verbosity = verbosity).run(suite)

if __name__ == '__main__':
    #Tip for running the tests (has to be command line) python3 test_app.py
    with open('test_reports/testing.out', 'w') as f:
        main(f)

