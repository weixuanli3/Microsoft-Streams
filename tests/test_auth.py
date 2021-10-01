# John Henderson (z5368143)
# This will test the auth.py file

# TODO Make blackbox

from src.other import clear_v1
from src.data_store import Datastore
import pytest

from src.auth import auth_register_v1, generate_handle 
from src.auth import auth_login_v1
from src.error import InputError
from src.data_store import data_store

#------------------------------------------------------------
# This block of code deals with the auth_register_v1 function 
# from auth.py

# This will be the second user as the first user is the example Admin user
def test_register_valid_email():
    clear_v1()
    assert auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe") == {'auth_user_id': 1}

def test_register_empty_email():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1("","password","John","Doe")

def test_register_email_already_used():
    clear_v1()
    auth_register_v1("john.doe1@unsw.edu.au","password","John","Doe")

    # Regerstering a second account with the same email
    with pytest.raises(InputError):
        auth_register_v1("john.doe1@unsw.edu.au","password","John","Doe")

def test_register_invalid_email():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1("john.doe.unsw.edu.au","password","John","Doe")

# Password can only be a minimum of 6 characters
def test_register_password_incorrect_length():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1("john.doe3@unsw.edu.au","12345","John","Doe")

def test_register_no_password():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1("john.doe3@unsw.edu.au","","John","Doe")

    # TODO: Possible max password?
    #with pytest.raises(InputError):
    #   auth_register_v1("john.doe@aunsw.edu.au","1234566789abcdefghijklmnopqrstuvwxyz","John","Doe")

# First name must be between 1 and 50 characters inclusive
def test_register_first_name_incorrect_length():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1("john.doe4@unsw.edu.au","password","","Doe")

    with pytest.raises(InputError):
        auth_register_v1("john.doe5@unsw.edu.au","password","JohnJohnJohnJohnJohnJohnJohnJohnJohnJohnJohnJohnJohn","Doe")

# Last name must be between 1 and 50 characters inclusive
def test_register_last_name_incorrect_length():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1("john.doe6@unsw.edu.au","password","John","")

    with pytest.raises(InputError):
        auth_register_v1("john.doe7@unsw.edu.au","password","John","DoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoe")


def test_register_password_all_spaces():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1("john.doe8@unsw.edu.au","      ","John","Doe")

#------------------------------------------------------------
# This tests generating handles

def test_corrent_handle():
    clear_v1()
    auth_register_v1("john.doe8@unsw.edu.au","password","John","Doe")
    assert 'johndoe01234567891011' in data_store.get('handle')['handle']

def test_symbles_handle():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1("john.doe9@unsw.edu.au","password","/.,/.","/.,/.,@#")

def test_corrent_handle_with_hyphen():
    clear_v1()
    auth_register_v1("john.doe8@unsw.edu.au","password","John-Doe","Doe")
    assert 'John-Doe' in data_store.get('names')['names']
    assert 'johndoedoe0123456789' in data_store.get('handle')['handle']

def test_handle_over_twenty():
    clear_v1()
    auth_register_v1("john.doe8@unsw.edu.au","password","John","Doe")
    auth_register_v1("john.doe9@unsw.edu.au","password","John","Doe")
    auth_register_v1("john.doe7@unsw.edu.au","password","John","Doe")
    assert 'johndoe01234567891011' in data_store.get('handle')['handle']
    assert 'johndoe0123456789101112' in data_store.get('handle')['handle']
    assert 'johndoe012345678910111213' in data_store.get('handle')['handle']

#------------------------------------------------------------
# Log in
# This block of code deals with the auth_login_v1 function 
# from auth.py

def test_email_not_registered():
    clear_v1()
    with pytest.raises(InputError):
        auth_login_v1("john.doe10@unsw.edu.au","password")

def test_email_empty():
    clear_v1()
    auth_register_v1("john.doe11@unsw.edu.au","password","John","Doe")
    with pytest.raises(InputError):
        auth_login_v1("","password")

# The email is a user, but has the wrong password
def test_incorrect_password():
    clear_v1()
    auth_register_v1("john.doe12@unsw.edu.au","password","John","Doe")
    with pytest.raises(InputError):
        auth_login_v1("john.doe12@unsw.edu.au","password123")

def test_correct_password():
    clear_v1()
    auth_register_v1("john.doe13@unsw.edu.au","password","John","Doe")
    assert auth_login_v1("john.doe13@unsw.edu.au","password") == {'auth_user_id': 1}

def test_bad_login_then_good_login():
    clear_v1()
    assert auth_register_v1("john.doe@unsw.edu.au","password","John","Doe") == {'auth_user_id': 1}

    # Should not work
    with pytest.raises(InputError):
        auth_login_v1("john.doe@unsw.edu.au","password1")

    # Should return corrent login user ID
    assert auth_login_v1("john.doe@unsw.edu.au","password") == {'auth_user_id': 1}
    
def test_password_empty():
    clear_v1()
    auth_register_v1("john.doe12@unsw.edu.au","password","John","Doe")
    with pytest.raises(InputError):
        auth_login_v1("john.doe12@unsw.edu.au","")

def test_pass_different_user():
    clear_v1()
    auth_register_v1("john.doe1@unsw.edu.au","password1","John","Doe")
    auth_register_v1("john.doe2@unsw.edu.au","password2","John","Doe")
    with pytest.raises(InputError):
        auth_login_v1("john.doe1@unsw.edu.au", "password2")
        
def no_users():
    clear_v1()
    with pytest.raises(InputError):
        auth_login_v1("john.doe1@unsw.edu.au", "password2")