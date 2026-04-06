import requests
import os
from dotenv import load_dotenv
load_dotenv()
ADMIN_AUTH_TOKEN = os.getenv('ADMIN_AUTH_TOKEN')

ROOT = "http://localhost:3000"
THINKERS_PATH = "/thinkers"
THOUGHTS_PATH = "/thoughts"
SIGNIN_PATH = "/signin"
REGISTER_PATH = "/register"
LIKE_ACTION_ID = "/like"
COMMENT_ACTION_ID = "/comment"
def api_get(authToken="",path=""):
    """
    Get the contents of the api endpint specified in the path parameter.
    :param auth_token: The authentication token required for accessing the API.
    :param path: The path to the desired content.
    :return: Returns a JSON response body from the API.
    """
    url = ROOT+path
    response = requests.get(url,headers={"test_flag":"TRUE","auth-token":authToken})
    responseIsNull = (response.headers['Content-Length']=="0")
    if responseIsNull:
        return response.status_code, None

    return response.status_code, response.json()

def api_get_thinker(auth_token="",thinkerId=""):
    """
    Get the contents of the thinker (user) relating to the given thinkerId.
    :param auth_token: The authentication token required for accessing the API.
    :param thhinkerId: The unique _id of the thinker (user) requested.
    :return: Returns a JSON response body from the API.
    """

    path = THINKERS_PATH + "/" + thinkerId
    return api_get(auth_token,path)

def api_get_thought(auth_token,thoughtId=""):
    """
    Get the contents of the thought (post) relating to the given thoughtId.
    :param auth_token: The authentication token required for accessing the API.
    :param thoughtId: The unique _id of the thought (post) requested.
    :return: Returns a JSON response body from the API.
    """

    path = THOUGHTS_PATH + "/" + thoughtId
    return api_get(auth_token,path)

def api_get_thought_comments(auth_token,thoughtId):
    """
    Post a comment on the thought (post) relating to the given thoughtId.
    :param auth_token: The authentication token required for accessing the API.
    :param thoughtId: The unique _id of the thought (post) to be commented.
    :return: Returns a JSON response body from the API.
    """
    path = THOUGHTS_PATH + "/" + thoughtId + "/comments"
    return api_get(auth_token,path)
def _api_post(path,req_body,auth_token="",admin_secret=None):
    #Private method - root of all other post methods.
    url = ROOT+path
    response = requests.post(url,headers={"test_flag":"TRUE","auth-token":auth_token,"admin_secret":admin_secret},json=req_body)
    responseIsNull = (response.headers['Content-Length']=="0")
    if responseIsNull:
        return response.status_code, None

    return response.status_code, response.json()

def api_post_thought(title:str, description:str, detail:str, echoChamber:str, image:str,auth_token:str):
    """
    Post a thought (post) using the given data.
    :param title: Title of the thought (post).
    :param description: Short description of the thought (post)
    :param detail: The body or content of the thought (post).
    :param echoChamber: Optional groups/tags to assign to the thought (post).
    :param image: A valid url to an image related to the posted content.
    :param auth_token: The authentication token required for accessing the API.
    :return: Returns a JSON response body from the API.
    """
    request_body={
        "title":title,
        "description":description,
        "detail":detail,
        "echoChamber":echoChamber,
        "image":image
    }
    return _api_post(THOUGHTS_PATH, request_body, auth_token)



def api_like_thought(thoughtId:str,auth_token:str):
    """
    Like the thought (post) relating to the given thoughtId.
    :param thoughtId: The unique _id of the thought (post) to be liked.
    :param auth_token: The authentication token required for accessing the API.
    :return: A tuple containing the (response.code() and response.json())
    """
    url = ROOT + THOUGHTS_PATH + LIKE_ACTION_ID + "/" + thoughtId
    response = requests.patch(url,headers={"test_flag":"TRUE","auth-token":auth_token})
    responseIsNull = (response.headers['Content-Length']=="0")

    if responseIsNull:
        return response.status_code, None

    return response.status_code, response.json()

def api_comment_thought(thoughtId:str, comment:str,auth_token:str):
    """
    Comment on the thought (post) relating to the given thoughtId.
    :param thoughtId: The unique _id of the thought (post) to be commented on.
    :param comment: The contents to be posted as a comment.
    :param auth_token: The authentication token required for accessing the API.
    :return: A tuple containing the (response.code() and response.json())
    """
    url = ROOT + THOUGHTS_PATH + COMMENT_ACTION_ID + "/" + thoughtId
    request_body = {"comment":comment}
    response = requests.patch(url,headers={"test_flag":"TRUE","auth-token":auth_token}, json=request_body)
    responseIsNull = (response.headers['Content-Length']=="0")

    if responseIsNull:
        return response.status_code, None

    return response.status_code, response.json()

def api_register(username:str,
                 email:str,
                 firstName:str,
                 lastName:str,
                 password:str,
                 echoChambers=["General"],
                 admin_secret=None
                 ):
    """
    Register a new user with the provided information.

    :param username: The desired username for the new user.
    :param email: The email address of the new user.
    :param firstName: The first name of the new user.
    :param lastName: The last name of the new user.
    :param password: The password for the new user.
    :param echoChambers: Optional groups/tags to assign to the user.
    :param admin_secret: (Optional) Admin key. If given and correct, user will be created with admin privileges.
    :return: A dictionary containing the response data from the API request.
    """
    request_body = {
        "username":username,
        "email":email,
        "firstName":firstName,
        "lastName":lastName,
        "password":password,
        "echoChambers":echoChambers
    }


    return _api_post(REGISTER_PATH, request_body, admin_secret=admin_secret)

def api_signin(username:str,password:str):
    """
    Sign in using the provided username and password.
    :param username: The username or email of the user attempting to sign in.
    :param password: the password associated with the provided user account.
    :return: A dictionary containing the response data from the API request. If successful, the response will contain an API auth-token.
    """

    request_body = {"username":username,"password":password}
    return _api_post(SIGNIN_PATH, request_body)

def _api_delete(auth_token:str,path="",admin_secret=None):
    #Private method - stem of other delete methodss
    url = ROOT + path
    response = requests.delete(url,headers={"test_flag":"TRUE","auth-token":auth_token,"admin_secret":admin_secret})
    responseIsNull = (response.headers['Content-Length']=="0")
    if responseIsNull:
        return response.status_code, None

    return response.status_code, response.json()

def api_delete_thought(thoughtId:str,auth_token:str):
    """
    Delete the thought (post) associated with the given thoughtId. Unless, the requester has admin privileges, users are only
    authorised to delete their own thoughts.
    :param thoughtId: The unique _id of the thought (post) to be deleted.
    :param auth_token: The authentication token required for accessing the API.
    :return: Returns a JSON response body from the API.
    """
    path = THOUGHTS_PATH + "/" + thoughtId
    return _api_delete(auth_token, path)

def api_delete_thinker(thinkerId:str,auth_token:str):
    """
    Delete the thinker (user) associated with the given thinkerId. Unless, the requester has admin privileges, users are only
    authorised to delete their own accounts.
    :param thinkerId: The unique _id of the thinker (user) who should be deleted.
    :param auth_token: The authentication token required for accessing the API.
    :return: Returns a JSON response body from the API.
    """
    path = THINKERS_PATH + "/" + thinkerId
    return _api_delete(auth_token, path)

def api_delete_all_thinkers():
    """
    Administrative function to delete all users in the currently connected database.
    The admin user making the request will not be deleted. Requires the user to have an admin role.
    :return: Returns a JSON response body from the API.
    """
    return _api_delete(ADMIN_AUTH_TOKEN, THINKERS_PATH)

def api_delete_all_thoughts():
    """
    Administrative function to delete all posts in the currently connected database. Requires the user to have an admin role.
    :return: Returns a JSON response body from the API.
    """
    return _api_delete(ADMIN_AUTH_TOKEN, THOUGHTS_PATH)

"""
print(api_register(
    "admin",
    "administrator@gmail.com",
    "Administrator",
    "Testing",
    "testing123",
    admin_secret=input("enter admin credentials. Alternatively enter return to skip")
))

print(api_signin(
    "admin",
    "testing123"
))
"""