import pytest
from src.auth import auth_register_v1, auth_login_v1
from src.admin import admin_user_remove_id
from src.other import clear_v1
from src.user import user_profile_setemail_v1, user_profile_sethandle_v1, user_profile_setname_v1, users_all_v1, user_profile_v1
from src.error import InputError

@pytest.fixture
def registered_user():
    clear_v1()
    return auth_register_v1('john.doe@unsw.edu.au', '123123', 'John', 'Doe')

"""For commented out tests, I am not sure how to make black box"""

"""
The following tests make some assumptions based on the gitlab doc!
 - id dictionary key is now called u_id.
 - users have a key called token.
"""

#################################
#        users/all/v1           #
#################################
# def test_many_registered_users(registered_user):
#     auth_register_v1('john.doe1@unsw.edu.au', '123123', 'John', 'Doe')
#     auth_register_v1('john.doe2@unsw.edu.au', '123123', 'John', 'Doe')
#     auth_register_v1('john.doe3@unsw.edu.au', '123123', 'John', 'Doe')
#     registered_user_token = registered_user['token']
#     result = users_all_v1(registered_user_token)
#     expected = {}
#     assert result == expected

def test_invalid_token():
    clear_v1()
    auth_register_v1('jane.doe@unsw.edu.au', '123123', 'jane', 'Doe')
    registered_user_token = 'HMMMMM'
    with pytest.raises(InputError):
        users_all_v1(registered_user_token)

def test_valid_test(registered_user):
    user_data = registered_user
    user_id = auth_register_v1('jane.doe@unsw.edu.au', '123123', 'jane', 'Doe')['auth_user_id']
    admin_user_remove_id(user_data['token'], user_id)
    result = users_all_v1(user_data['token'])
    expected = {
        'users':[{
            'email': 'john.doe@unsw.edu.au',
            'handle_str': 'johndoe',
            'name_first': 'John',
            'name_last': 'Doe',
            'u_id': 1
        }]
    }
    assert result == expected
#################################
#       user/profile/v1         #
#################################
def test_profile_user_not_found(registered_user):
    registered_user_token = registered_user['token']
    with pytest.raises(InputError):
        user_profile_v1(registered_user_token, 383)

def test_profile_invalid_token(registered_user):
    registered_user_id = registered_user['auth_user_id']
    with pytest.raises(InputError):
        user_profile_v1("IUdbe", registered_user_id)
# not sure how to test this at the moment
# def test_profile_valid_test(registered_user):
#     registered_user_token = registered_user['token']
#     registered_user_id = registered_user['id']
#     result = user_profile_v1(registered_user_token, registered_user_id)
#     expected = {"user_id" }
#     assert result == expected
#################################
#    user/profile/setname/v1    #
#################################
def test_setname_name_first_too_short(registered_user):
    registered_user_token = registered_user['token']
    with pytest.raises(InputError):
        user_profile_setname_v1(registered_user_token, "", "Test")

def test_setname_name_last_too_short(registered_user):
    registered_user_token = registered_user['token']
    with pytest.raises(InputError):
        user_profile_setname_v1(registered_user_token, "Test", "")

def test_setname_name_first_too_long(registered_user):
    registered_user_token = registered_user['token']
    with pytest.raises(InputError):
        user_profile_setname_v1(registered_user_token, "John", "DoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoe")

def test_setname_name_last_too_long(registered_user):
    registered_user_token = registered_user['token']
    with pytest.raises(InputError):
        user_profile_setname_v1(registered_user_token, "JohnJohnJohnJohnJohnJohnJohnJohnJohnJohnJohnJohnJohn", "Doe")
# Assumption we have - names cannot contain non-alphabetical characters and
# grammer that is not associated with names
# THE BELOW TEST IS NOT BLACKBOX!!!
def test_setname_alphanumeric(registered_user):
    registered_user_token = registered_user['token']
    user_profile_setname_v1(registered_user_token, "Mary-Ann", "!@#Doe")
    result_first_name = users_all_v1(registered_user_token)['users'][0]['name_first']
    result_last_name = users_all_v1(registered_user_token)['users'][0]['name_last']
    expected = ["Mary-Ann", "Doe"]
    assert [result_first_name, result_last_name] == expected


def test_setname_invlid_token(registered_user):
    with pytest.raises(InputError):
        user_profile_setname_v1("dOEID", "Janet", "Doe")

def test_setname_valid_test(registered_user):
    auth_register_v1('jane.doe@unsw.edu.au', '123123', 'jane', 'Doe')
    registered_user_token = registered_user['token']
    registered_user_id = registered_user['auth_user_id']
    returned = user_profile_setname_v1(registered_user_token, "Janet", "Doe")
    assert returned == {}
    result_first_name = user_profile_v1(registered_user_token, registered_user_id)['name_first']
    result_last_name = user_profile_v1(registered_user_token, registered_user_id)['name_last']
    expected = ["Janet", "Doe"]
    assert [result_first_name, result_last_name] == expected
#################################
#     user/profile/setemail/    #
#################################
def test_setmail_email_not_valid(registered_user):
    registered_user_token = registered_user['token']
    with pytest.raises(InputError):
        user_profile_setemail_v1(registered_user_token, "john.doe.unsw.edu.au")

def test_setmail_email_already_used(registered_user):
    registered_user_token = registered_user['token']
    auth_register_v1('john.doe1@unsw.edu.au', '123123', 'John', 'Doe')
    with pytest.raises(InputError):
        user_profile_setemail_v1(registered_user_token, "john.doe1@unsw.edu.au")

def test_setmail_invlid_token(registered_user):
    with pytest.raises(InputError):
        user_profile_setemail_v1("EFSE", "john.doe1@unsw.edu.au")

def test_setmail_valid_test(registered_user):
    auth_register_v1('jane.doe@unsw.edu.au', '123123', 'jane', 'Doe')
    registered_user_token = registered_user['token']
    registered_user_id = registered_user['auth_user_id']
    returned = user_profile_setemail_v1(registered_user_token, "janet.doe@unsw.ed.au")
    assert returned == {}
    result = user_profile_v1(registered_user_token, registered_user_id)['email']
    expected = "janet.doe@unsw.ed.au"
    assert result == expected
#################################
#   user/profile/sethandle/v1   #
#################################
def test_sethandle_handle_too_short(registered_user):
    registered_user_token = registered_user['token']
    with pytest.raises(InputError):
        user_profile_sethandle_v1(registered_user_token, "12")

def test_sethandle_handle_too_long(registered_user):
    registered_user_token = registered_user['token']
    with pytest.raises(InputError):
        user_profile_sethandle_v1(registered_user_token, "123456789101112131415")

def test_sethandle_none_alphanumeric(registered_user):
    registered_user_token = registered_user['token']
  
    with pytest.raises(InputError):
        user_profile_sethandle_v1(registered_user_token, "johnDoe#@")
def test_sethandle_handle_already_used(registered_user):
    registered_user2_token = auth_register_v1('john.doe1@unsw.edu.au', '123123', 'John', 'Doe')['token']
    # Make sure that user1 has the handle "johndoe". This is done to keep the test blackbox
    with pytest.raises(InputError):
        user_profile_sethandle_v1(registered_user2_token, "johndoe")

def test_sethandle_invlid_token(registered_user):
    with pytest.raises(InputError):
        user_profile_sethandle_v1("EFSE", "johnDoe12")

def test_sethandle_valid_test(registered_user):
    auth_register_v1('jane.doe@unsw.edu.au', '123123', 'jane', 'Doe')
    registered_user_token = registered_user['token']
    registered_user_id = registered_user['auth_user_id']
    returned = user_profile_sethandle_v1(registered_user_token, "johnDoe")
    assert returned == {}
    result = user_profile_v1(registered_user_token, registered_user_id)['handle_str']
    expected = "johnDoe"
    assert result == expected
    clear_v1()
