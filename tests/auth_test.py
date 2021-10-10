'''Contains tests for auth.py'''

import pytest

from src.other import clear_v1
from src.auth import auth_register_v1
from src.auth import auth_login_v1
from src.error import InputError

#------------------------------------------------------------
# This block of code deals with the auth_register_v1 function
# from auth.py

# This should not raise any errors
def test_auth_register_valid_email():
    clear_v1()
    auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")

def test_auth_register_empty_email():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1("","password","John","Doe")

def test_auth_register_email_already_used():
    clear_v1()
    auth_register_v1("john.doe1@unsw.edu.au","password","John","Doe")

    # Regerstering a second account with the same email
    with pytest.raises(InputError):
        auth_register_v1("john.doe1@unsw.edu.au","password","John","Doe")

def test_auth_register_invalid_email():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1("john.doe.unsw.edu.au","password","John","Doe")

# Password can only be a minimum of 6 characters
def test_auth_register_password_incorrect_length():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1("john.doe3@unsw.edu.au","12345","John","Doe")

def test_auth_register_no_password():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1("john.doe3@unsw.edu.au","","John","Doe")

# First name must be between 1 and 50 characters inclusive
def test_auth_register_first_name_incorrect_length():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1("john.doe4@unsw.edu.au","password","","Doe")

    with pytest.raises(InputError):
        auth_register_v1("john.doe5@unsw.edu.au","password","JohnJohnJohnJohnJohnJohnJohnJohnJohnJohnJohnJohnJohn","Doe")

# Last name must be between 1 and 50 characters inclusive
def test_auth_register_last_name_incorrect_length():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1("john.doe6@unsw.edu.au","password","John","")

    with pytest.raises(InputError):
        auth_register_v1("john.doe7@unsw.edu.au","password","John","DoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoe")


def test_auth_register_password_all_spaces():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1("john.doe8@unsw.edu.au","      ","John","Doe")

def test_auth_register_first_name_special_characters():
    clear_v1()
    auth_register_v1("john.doe8@unsw.edu.au","password","J%^o&*h#(n#","Doe")

def test_auth_register_last_name_special_characters():
    clear_v1()
    auth_register_v1("john.doe8@unsw.edu.au","password","John","$#D^^o%^&^%$e")

#------------------------------------------------------------
# This tests generating handles NOT BLACKBOX

# def test_corrent_handle():
#     clear_v1()
#     auth_register_v1("john.doe8@unsw.edu.au","password","John","Doe")
#     assert 'johndoe' in data_store.get('handle')['handle']

# def test_symbles_handle():
#     clear_v1()
#     with pytest.raises(InputError):
#         auth_register_v1("john.doe9@unsw.edu.au","password","/.,/.","/.,/.,@#")

# def test_corrent_handle_with_hyphen():
#     clear_v1()
#     auth_register_v1("john.doe8@unsw.edu.au","password","John-Doe","Doe")
#     assert 'John-Doe' in data_store.get('names')['names']
#     assert 'johndoedoe' in data_store.get('handle')['handle']

# def test_handle_multiple_users():
#     clear_v1()
#     auth_register_v1("john.doe8@unsw.edu.au","password","John","Doe")
#     auth_register_v1("john.doe9@unsw.edu.au","password","John","Doe")
#     auth_register_v1("john.doe7@unsw.edu.au","password","John","Doe")
#     assert 'johndoe' in data_store.get('handle')['handle']
#     assert 'johndoe0' in data_store.get('handle')['handle']
#     assert 'johndoe1' in data_store.get('handle')['handle']

# def test_handle_over_twenty():
#     clear_v1()
#     auth_register_v1("john.doe8@unsw.edu.au","password","Johnnathannnn","Dorathy")
#     auth_register_v1("john.doe9@unsw.edu.au","password","Johnnathannnn","Dorathy")
#     assert 'johnnathannnndorathy' in data_store.get('handle')['handle']
#     assert 'johnnathannnndorathy0' in data_store.get('handle')['handle']

#------------------------------------------------------------
# Log in
# This block of code deals with the auth_login_v1 function
# from auth.py

def test_auth_login_email_not_registered():
    clear_v1()
    with pytest.raises(InputError):
        auth_login_v1("john.doe10@unsw.edu.au","password")

def test_auth_login_email_empty():
    clear_v1()
    auth_register_v1("john.doe11@unsw.edu.au","password","John","Doe")
    with pytest.raises(InputError):
        auth_login_v1("","password")

# The email is a user, but has the wrong password
def test_auth_login_incorrect_password():
    clear_v1()
    auth_register_v1("john.doe12@unsw.edu.au","password","John","Doe")
    with pytest.raises(InputError):
        auth_login_v1("john.doe12@unsw.edu.au","password123")

def test_auth_login_correct_password():
    clear_v1()
    user_id = auth_register_v1("john.doe13@unsw.edu.au","password","John","Doe")
    assert auth_login_v1("john.doe13@unsw.edu.au","password") == user_id

def test_auth_login_bad_login_good_login():
    clear_v1()
    user_id = auth_register_v1("john.doe@unsw.edu.au","password","John","Doe")

    # Should not work
    with pytest.raises(InputError):
        auth_login_v1("john.doe@unsw.edu.au","password1")

    # Should return corrent login user ID
    assert auth_login_v1("john.doe@unsw.edu.au","password") == user_id

def test_auth_login_password_empty():
    clear_v1()
    auth_register_v1("john.doe12@unsw.edu.au","password","John","Doe")
    with pytest.raises(InputError):
        auth_login_v1("john.doe12@unsw.edu.au","")

def test_auth_login_pass_different_user():
    clear_v1()
    auth_register_v1("john.doe1@unsw.edu.au","password1","John","Doe")
    auth_register_v1("john.doe2@unsw.edu.au","password2","John","Doe")
    with pytest.raises(InputError):
        auth_login_v1("john.doe1@unsw.edu.au", "password2")
        
#------------------------------------------------------------
# Log out
# This block of code deals with the auth_logout_v1 function
# from auth.py

# def test_invalid_token():
#     auth_register_v1("john.doe12@unsw.edu.au","password","John","Doe")
#     token = auth_login_v1("john.doe12@unsw.edu.au","password")[0]
#     assert auth_logout_v1(923564) == {}
    
# def test_empty_token():
#     auth_register_v1("john.doe12@unsw.edu.au","password","John","Doe")
#     token = auth_login_v1("john.doe12@unsw.edu.au","password")[0]
#     assert auth_logout_v1() == {}

# def test_valid_token():
#     auth_register_v1("john.doe12@unsw.edu.au","password","John","Doe")
#     token = auth_login_v1("john.doe12@unsw.edu.au","password")[0]
#     assert auth_logout_v1(token) == {}

