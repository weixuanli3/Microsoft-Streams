import pytest
from src.error import InputError
from src.other import clear_v1
from other_functions.request_helper_functions import admin_user_remove_req, auth_login_req, auth_logout_req, auth_register_req, clear_req
from src.data_store import data_store

#------------------------------------------------------------
# This block of code deals with the auth_register_v1 function
# from auth.py

# This should not raise any errors
def test_auth_register_valid_email():
    clear_req()
    auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")

def test_auth_register_empty_email():
    clear_req()
    register_test = auth_register_req("","password","John","Doe")
    assert register_test['code'] == InputError.code

def test_auth_register_email_already_used():
    clear_req()
    auth_register_req("john.doe1@unsw.edu.au","password","John","Doe")

    # Regerstering a second account with the same email
    register_test = auth_register_req("john.doe1@unsw.edu.au","password","John","Doe")
    assert register_test['code'] == InputError.code

def test_auth_register_invalid_email():
    clear_req()
    register_test = auth_register_req("john.doe.unsw.edu.au","password","John","Doe")
    assert register_test['code'] == InputError.code

# Password can only be a minimum of 6 characters
def test_auth_register_password_incorrect_length():
    clear_req()
    register_test = auth_register_req("john.doe3@unsw.edu.au","12345","John","Doe")
    assert register_test['code'] == InputError.code

def test_auth_register_no_password():
    clear_req()
    register_test = auth_register_req("john.doe3@unsw.edu.au","","John","Doe")    
    assert register_test['code'] == InputError.code

# First name must be between 1 and 50 characters inclusive
def test_auth_register_first_name_incorrect_length():
    clear_req()

    register_test = auth_register_req("john.doe4@unsw.edu.au","password","","Doe")
    assert register_test['code'] == InputError.code

    register_test = auth_register_req("john.doe5@unsw.edu.au","password","JohnJohnJohnJohnJohnJohnJohnJohnJohnJohnJohnJohnJohn","Doe")
    assert register_test['code'] == InputError.code

# Last name must be between 1 and 50 characters inclusive
def test_auth_register_last_name_incorrect_length():
    clear_req()
    register_test = auth_register_req("john.doe6@unsw.edu.au","password","John","")
    assert register_test['code'] == InputError.code

    register_test = auth_register_req("john.doe7@unsw.edu.au","password","John","DoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoe")
    assert register_test['code'] == InputError.code


def test_auth_register_password_all_spaces():
    clear_req()
    register_test = auth_register_req("john.doe8@unsw.edu.au","      ","John","Doe")
    assert register_test['code'] == InputError.code

def test_auth_register_first_name_special_characters():
    clear_req()
    auth_register_req("john.doe8@unsw.edu.au","password","J%^o&*h#(n#","Doe")

def test_auth_register_last_name_special_characters():
    clear_req()
    auth_register_req("john.doe8@unsw.edu.au","password","John","Doe")

# Cannot test for exact in blackbox, but can test if it throws an error
def test_longer_handle():
    clear_req()

    auth_register_req("john.doe@unsw.edu.au","password","John","Doe")
    auth_register_req("john.do2@unsw.edu.au","password","John","Doe")
    auth_register_req("john.do3@unsw.edu.au","password","John","Doe")

#------------------------------------------------------------
# Log in
# This block of code deals with the auth_login_v1 function
# from auth.py

def test_auth_login_email_not_registered():
    clear_req()
    register_test = auth_login_req("john.doe10@unsw.edu.au","password")
    assert register_test['code'] == InputError.code

def test_auth_login_email_empty():
    clear_req()
    auth_register_req("john.doe11@unsw.edu.au","password","John","Doe")
    register_test = auth_login_req("","password")
    assert register_test['code'] == InputError.code

# The email is a user, but has the wrong password
def test_auth_login_incorrect_password():
    clear_req()
    auth_register_req("john.doe12@unsw.edu.au","password","John","Doe")
    register_test = auth_login_req("john.doe12@unsw.edu.au","password123")
    assert register_test['code'] == InputError.code

def test_auth_login_correct_password():
    clear_req()
    user_id = auth_register_req("john.doe13@unsw.edu.au","password","John","Doe")['auth_user_id']
    assert auth_login_req("john.doe13@unsw.edu.au","password")['auth_user_id'] == user_id

def test_auth_login_bad_login_good_login():
    clear_req()
    user_id = auth_register_req("john.doe@unsw.edu.au","password","John","Doe")['auth_user_id']
    print(user_id)
    # Should not work
    register_test = auth_login_req("john.doe@unsw.edu.au","password1")
    assert register_test['code'] == InputError.code

    # Should return corrent login user ID
    assert auth_login_req("john.doe@unsw.edu.au","password")["auth_user_id"] == user_id

def test_auth_login_password_empty():
    clear_req()
    auth_register_req("john.doe12@unsw.edu.au","password","John","Doe")
    register_test = auth_login_req("john.doe12@unsw.edu.au","")
    assert register_test['code'] == InputError.code

def test_auth_login_pass_different_user():
    clear_req()
    auth_register_req("john.doe1@unsw.edu.au","password1","John","Doe")
    auth_register_req("john.doe2@unsw.edu.au","password2","John","Doe")
    register_test = auth_login_req("john.doe1@unsw.edu.au", "password2")
    assert register_test['code'] == InputError.code    

#------------------------------------------------------------
# Log out
# This block of code deals with the auth_logout_v1 function
# from auth.py

# POSSIBLE ASSUMPTION RASIE INPUT ERROR?
def test_invalid_token():
    clear_req()
    auth_register_req("john.doe12@unsw.edu.au","password","John","Doe")
    auth_login_req("john.doe12@unsw.edu.au","password")['token']
    
    register_test = auth_logout_req(923564)
    assert register_test['code'] == InputError.code    

# CANNOT CALL FUNCTION WITHOUT PROPER INPUT, ERROR NOT ON SERVER SIDE   
# def test_empty_token():
#     clear_v1()
#     auth_register_v1("john.doe12@unsw.edu.au","password","John","Doe")
#     token = auth_login_v1("john.doe12@unsw.edu.au","password")['token']
#     with pytest.raises(InputError): 
#       auth_logout_v1()

def test_valid_token():
    clear_req()
    auth_register_req("john.doe12@unsw.edu.au","password","John","Doe")
    token = auth_login_req("john.doe12@unsw.edu.au","password")['token']
    assert auth_logout_req(token) == {}
    clear_req()
