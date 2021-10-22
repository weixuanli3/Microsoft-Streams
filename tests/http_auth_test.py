import pytest
from src.error import InputError
from src.other import clear_v1
from src.request_helper_functions import admin_user_remove_req, auth_register_req, clear_req
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