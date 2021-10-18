'''Contains functions to register new users and login'''

import re
import jwt

from src.data_store import data_store
from src.error import InputError

# from data_store import data_store
# from error import InputError

################################
#    Main functions for auth   #
################################

"""
Returns the user id if a valid email and password pair are entered

Args:
    email: the email of the user
    password: the password of the user

Returns:
    user_id

Raises:
    Input Error: - password or email is incorrect

"""


def auth_login_v1(email, password):
    """Returns ID and a valid token"""

    user_data = data_store.get_data()['users']
    # -1 should never be an actual user ID
    for users in user_data:
        if (users['emails'], users['passwords']) == (email, password):
            user_id = users['id']

            token = generate_token(users)
            users['token'].append(token)

            return {
                'token': token,
                'auth_user_id': user_id
            }

    raise InputError("Password or email is incorrect")


"""
This function is used to register a user.  If the new_users
infomation is corrent, it will return the new users ID {ID}. Strips all
special characters from user name_first and name_last then combines them
    to create a handle.

Args:
    email: the email of the user
    password: the password of the user
    name_first: the first name of the user
    name_last: the last name of the user

Returns:
    user_id

Raises:
    Input Error: - email invalid.
                    - password invalid.
                    - name_first invalid.
                    - name_last invalid.

"""


def auth_register_v1(email, password, name_first, name_last):
    """Registers a new user and enters them into the database. Returns ID and token"""

    # Do not allow passwords of all white space
    password_is_all_spaces = password == (len(password) * ' ')
    if password_is_all_spaces:
        raise InputError("Password cannot be all white space")

    # Formating name to remove special characters
    regex = re.compile(r"[^a-zA-Z0-9-]")
    name_first = regex.sub("", name_first)
    name_last = regex.sub("", name_last)

    # Used to check that the email is valid
    regex = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$"
    is_valid_email = re.match(regex, email)

    # Gets a dictionary for the emails ie: 'emails' : [...]
    user_emails = data_store.get('emails')
    is_not_already_registered = not email in user_emails['emails']

    # Check remaining conditions
    is_valid_password = len(password) >= 6 and len(password) <= 100
    is_valid_name_first = len(name_first) >= 1 and len(name_first) <= 50
    is_valid_name_last = len(name_last) >= 1 and len(name_last) <= 50

    # Check all conditions to see that a user is valid
    if (is_valid_email and is_valid_password and is_valid_name_last and
            is_valid_name_first and is_not_already_registered):

        # REGISTER USER
        user_data = data_store.get_data()['users']
        new_user_id = len(user_data) + 1

        new_user = {
            'id': new_user_id,
            'names': name_first,
            'name_lasts': name_last,
            'emails': email,
            'passwords': password,
            'handle': generate_handle(name_first, name_last),
            'channels': [],
            'token' : []
        }

        token = generate_token(new_user)
        new_user['token'].append(token)

        user_data.append(new_user)

        # Adds the first user as a global user
        global_users = data_store.get_data()['global_owners']
        if len(global_users) == 0:
            global_users.append(new_user_id)

        return {
            'token': token,
            'auth_user_id': new_user_id
        }

    # RAISE ERROR
    raise InputError("There was a problem with the user registration data")


def auth_logout_v1(token):
    """logs the user out. Removes their token from the data base"""

    user_data = data_store.get_data()['users']
    for user in user_data:
        if token in user['token']:
            user['token'].remove(token)
            return {}
    raise InputError('Could not find token')

################################
#   Helper functions for auth  #
################################


"""
Given a first and last name, it will generate a handle for the user.

A handle is generated that is the concatenation of their casted-to-lowercase
alphanumeric (a-z0-9) first name and last name. If the concatenation is
longer than 20 characters, it is cut off at 20 characters. If it is too
short than numbers are added until it is a length of 20. If it is 20 characters
and this handle is already taken, then it may go over.

Arguments: - name_first: first name of the user
            - name_last: last name of the user

"""


def generate_handle(name_first, name_last):
    """Given a users first and last name, generate a handle"""

    # Used just to filter out any hyphens in the name
    user_handle = re.sub(r'\W+', '', name_first + name_last)
    user_handle = user_handle[:20]
    user_handle = user_handle.lower()

    # more than 20 if the user is already there
    is_valid_handle = not user_handle in data_store.get('handle')['handle']
    i = 0
    while not is_valid_handle:
        is_valid_handle = not user_handle + \
            str(i) in data_store.get('handle')['handle']
        if is_valid_handle:
            user_handle = user_handle + str(i)
        i += 1

    return user_handle


def generate_token(user):
    """Uses JWT to generate token based on user information"""

    SECRET = "IAmNotSureReally"

    payload = {
        "u_id" : user['id'],
        "User_session" : len(user['token']) + 1
    }

    token = str(
        jwt.encode(
            payload,
            SECRET,
            algorithm='HS256'
        )
    )

    return token
