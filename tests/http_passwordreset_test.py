'''Contains http tests for passwordreset function in auth.py'''

import pytest
import requests
import json
from src.error import AccessError, InputError
from other_functions.request_helper_functions import *
from src.data_store import data_store
from src.config import url

@pytest.fixture
def setup():
    clear_req()
    return auth_register_req("john.doe1@unsw.edu.au","password","John","Doe")

#------------------------------------------------------------
# This block of code deals with the auth_passwordreset_request_req function

# nothing should happen when email is invalid or valid
def test_request_email(setup):
    assert auth_passwordreset_request_req("john.doe1@unsw.edu.au") == {}
    assert auth_passwordreset_request_req("roy.lin@unsw.edu.au") == {}

#------------------------------------------------------------
# This block of code deals with the auth_password_reset_req function

# whitebox test
def test_reset_valid(setup):
    user = setup
    reset_code = ''

    user_data = data_store.get_data()['users']
    for users in user_data:
        if users['id'] == user['auth_user_id']:
            reset_code = users['reset_code']

    auth_passwordreset_reset_req(reset_code, "newpassword")

def test_reset_code_invalid():
    clear_req()
    auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")
    assert auth_passwordreset_reset_req(123832, "password123")['code'] == InputError.code

def test_reset_password_invalid():
    clear_req()
    assert auth_passwordreset_reset_req(1, "")['code'] == InputError.code
