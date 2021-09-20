# John Henderson (z5368143)
# This will test the auth python file

# TODO: write tests

import pytest

from src.auth import auth_register_v1
from src.auth import auth_login_v1
from src.error import InputError

#------------------------------------------------------------
# This block of code deals with the auth_register_v1 function 
# from auth.py

def test_register_invalid_email():
    pass

def test_register_email_already_used():
    pass

def test_register_valid_email():
    pass

# Password can only be a minimum of 6 characters
# Maximum? Possible assumpsion
def test_register_password_incorrect_length():
    pass

# First name must be between 1 and 50 characters inclusive
def test_register_first_name_incorrect_length():
    pass

# Last name must be between 1 and 50 characters inclusive
def test_register_last_name_incorrect_length():
    pass


#------------------------------------------------------------
# This block of code deals with the auth_login_v1 function 
# from auth.py

def test_email_not_registered():
    pass

# The email is a user, but has the wrong password
def test_incorrect_password():
    pass

def test_correct_password():
    pass