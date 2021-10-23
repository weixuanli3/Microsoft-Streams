import pytest
import requests
import json
from src.error import AccessError, InputError
from other_functions.request_helper_functions import *
from src.config import url

@pytest.fixture
def registered_user():
    clear_req()
    return auth_register_req('john.doe@unsw.edu.au', '123123', 'John', 'Doe')

"""
The following tests make some assumptions based on the gitlab doc!
 - id dictionary key is now called u_id.
 - users have a key called token.
"""

#################################
#        users/all/req           #
#################################
def test_invalid_token():
    clear_req()
    auth_register_req('jane.doe@unsw.edu.au', '123123', 'jane', 'Doe')
    registered_user_token = 'HMMMMM'
    assert users_all_req(registered_user_token)['code'] == AccessError.code

# def test_valid_test(registered_user):
#     token = registered_user['token']
#     user_id = auth_register_req('jane.doe@unsw.edu.au', '123123', 'jane', 'Doe')['auth_user_id']
#     admin_user_remove_req(token, user_id)
#     result = users_all_req(token)
#     expected = {
#         'users':[{
#             'email': 'john.doe@unsw.edu.au',
#             'handle_str': 'johndoe',
#             'name_first': 'John',
#             'name_last': 'Doe',
#             'u_id': 1
#         }]
#     }
#     assert result == expected
#################################
#       user/profile/req        #
#################################
def test_profile_user_not_found(registered_user):
    registered_user_token = registered_user['token']
    assert user_profile_req(registered_user_token, 383)['code'] == InputError.code

def test_profile_invalid_token(registered_user):
    registered_user_id = registered_user['auth_user_id']
    assert user_profile_req("IUdbe", registered_user_id)['code'] == AccessError.code
# not sure how to test this at the moment
# def test_profile_valid_test(registered_user):
#     registered_user_token = registered_user['token']
#     registered_user_id = registered_user['id']
#     result = user_profile_req(registered_user_token, registered_user_id)
#     expected = {"user_id" }
#     assert result == expected
#################################
#    user/profile/setname/req    #
#################################
def test_setname_name_first_too_short(registered_user):
    registered_user_token = registered_user['token']
    assert user_profile_setname_req(registered_user_token, "", "Test")['code'] == InputError.code

def test_setname_name_last_too_short(registered_user):
    registered_user_token = registered_user['token']
    assert user_profile_setname_req(registered_user_token, "Test", "")['code'] == InputError.code

def test_setname_name_first_too_long(registered_user):
    registered_user_token = registered_user['token']
    assert user_profile_setname_req(registered_user_token, "John", "DoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoe")['code'] == InputError.code

def test_setname_name_last_too_long(registered_user):
    registered_user_token = registered_user['token']
    assert user_profile_setname_req(registered_user_token, "JohnJohnJohnJohnJohnJohnJohnJohnJohnJohnJohnJohnJohn", "Doe")['code'] == InputError.code
# Assumption we have - names cannot contain non-alphabetical characters and
# grammer that is not associated with names
# THE BELOW TEST IS NOT BLACKBOX!!!
def test_setname_alphanumeric(registered_user):
    registered_user_token = registered_user['token']
    user_profile_setname_req(registered_user_token, "Mary-Ann", "!@#Doe")
    result_first_name = users_all_req(registered_user_token)['users'][0]['name_first']
    result_last_name = users_all_req(registered_user_token)['users'][0]['name_last']
    expected = ["Mary-Ann", "Doe"]
    assert [result_first_name, result_last_name] == expected


def test_setname_invlid_token(registered_user):
    assert user_profile_setname_req("dOEID", "Janet", "Doe")['code'] == AccessError.code

def test_setname_valid_test(registered_user):
    auth_register_req('jane.doe@unsw.edu.au', '123123', 'jane', 'Doe')
    registered_user_token = registered_user['token']
    registered_user_id = registered_user['auth_user_id']
    returned = user_profile_setname_req(registered_user_token, "Janet", "Doe")
    assert returned == {}
    result_first_name = user_profile_req(registered_user_token, registered_user_id)['name_first']
    result_last_name = user_profile_req(registered_user_token, registered_user_id)['name_last']
    expected = ["Janet", "Doe"]
    assert [result_first_name, result_last_name] == expected
#################################
#     user/profile/setemail/    #
#################################
def test_setmail_email_not_valid(registered_user):
    registered_user_token = registered_user['token']
    assert user_profile_setemail_req(registered_user_token, "john.doe.unsw.edu.au")['code'] == InputError.code

def test_setmail_email_already_used(registered_user):
    registered_user_token = registered_user['token']
    auth_register_req('john.doe1@unsw.edu.au', '123123', 'John', 'Doe')
    assert user_profile_setemail_req(registered_user_token, "john.doe1@unsw.edu.au")['code'] == InputError.code

def test_setmail_invlid_token(registered_user):
    assert user_profile_setemail_req("EFSE", "john.doe1@unsw.edu.au")['code'] == AccessError.code

def test_setmail_valid_test(registered_user):
    auth_register_req('jane.doe@unsw.edu.au', '123123', 'jane', 'Doe')
    registered_user_token = registered_user['token']
    registered_user_id = registered_user['auth_user_id']
    returned = user_profile_setemail_req(registered_user_token, "janet.doe@unsw.ed.au")
    assert returned == {}
    result = user_profile_req(registered_user_token, registered_user_id)['email']
    expected = "janet.doe@unsw.ed.au"
    assert result == expected
#################################
#   user/profile/sethandle/req   #
#################################
def test_sethandle_handle_too_short(registered_user):
    registered_user_token = registered_user['token']
    assert user_profile_sethandle_req(registered_user_token, "12")['code'] == InputError.code

def test_sethandle_handle_too_long(registered_user):
    registered_user_token = registered_user['token']
    assert user_profile_sethandle_req(registered_user_token, "123456789101112131415")['code'] == InputError.code

def test_sethandle_none_alphanumeric(registered_user):
    registered_user_token = registered_user['token']
  
    assert user_profile_sethandle_req(registered_user_token, "johnDoe#@")['code'] == InputError.code
def test_sethandle_handle_already_used(registered_user):
    registered_user2_token = auth_register_req('john.doe1@unsw.edu.au', '123123', 'John', 'Doe')['token']
    # Make sure that user1 has the handle "johndoe". This is done to keep the test blackbox
    assert user_profile_sethandle_req(registered_user2_token, "johndoe")['code'] == InputError.code

def test_sethandle_invlid_token(registered_user):
    assert user_profile_sethandle_req("EFSE", "johnDoe12")['code'] == AccessError.code

def test_sethandle_valid_test(registered_user):
    auth_register_req('jane.doe@unsw.edu.au', '123123', 'jane', 'Doe')
    registered_user_token = registered_user['token']
    registered_user_id = registered_user['auth_user_id']
    returned = user_profile_sethandle_req(registered_user_token, "johnDoe")
    assert returned == {}
    result = user_profile_req(registered_user_token, registered_user_id)['handle_str']
    expected = "johnDoe"
    assert result == expected
    clear_req()
