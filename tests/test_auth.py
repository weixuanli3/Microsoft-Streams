# John Henderson (z5368143)
# This will test the auth python file

"""
TODO:
Check that when a test is successful that it returns the correct user ID.
Check over tests to make sure they are correct.
"""

import pytest

from src.auth import auth_register_v1
from src.auth import auth_login_v1
from src.error import InputError

#------------------------------------------------------------
# This block of code deals with the auth_register_v1 function 
# from auth.py

def test_register_invalid_email():
    with pytest.raises(InputError):
        auth_register_v1("john.doe.unsw.edu.au","password","John","Doe")

def test_register_email_already_used():

    auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")

    # Regerstering a second account with the same email
    with pytest.raises(InputError):
        auth_register_v1("john.doe@unsw.edu.au","password","John","Doe")

# TODO: Check it returns the correct ID?
def test_register_valid_email():
    auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")

# Password can only be a minimum of 6 characters
# Maximum? Possible assumpsion
def test_register_password_incorrect_length():
    with pytest.raises(InputError):
        auth_register_v1("john.doe@aunsw.edu.au","123","John","Doe")

    # TODO: Possible max password
    with pytest.raises(InputError):
        auth_register_v1("john.doe@aunsw.edu.au","1234566789abcdefghijklmnopqrstuvwxyz","John","Doe")

# First name must be between 1 and 50 characters inclusive
def test_register_first_name_incorrect_length():
    with pytest.raises(InputError):
        auth_register_v1("john.doe@aunsw.edu.au","password","","Doe")

    with pytest.raises(InputError):
        auth_register_v1("john.doe@aunsw.edu.au","password","JohnJohnJohnJohnJohnJohnJohnJohnJohnJohnJohnJohnJohn","Doe")

# Last name must be between 1 and 50 characters inclusive
def test_register_last_name_incorrect_length():
    with pytest.raises(InputError):
        auth_register_v1("john.doe@aunsw.edu.au","password","John","")

    with pytest.raises(InputError):
        auth_register_v1("john.doe@aunsw.edu.au","password","John","DoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoe")



#------------------------------------------------------------
# This block of code deals with the auth_login_v1 function 
# from auth.py

def test_email_not_registered():
    with pytest.raises(InputError):
        auth_login_v1("john.doe@aunsw.edu.au","password","John","Doe")


# The email is a user, but has the wrong password
def test_incorrect_password():
    auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")
    with pytest.raises(InputError):
        auth_login_v1("john.doe@aunsw.edu.au","password","John","Doe")

# TODO: Check it returns the correct ID?
def test_correct_password():
    auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")
    auth_login_v1("john.doe@aunsw.edu.au","password","John","Doe")