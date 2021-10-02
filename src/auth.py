# John Henderson (z5368143)
# Tomas Ostroumoff (z5312982)

# from data_store import data_store
# from error import InputError

import re

from src.data_store import data_store
from src.error import InputError


def auth_login_v1(email, password):

    """
    Returns the user id if a valid email and password pair are entered
    """

    user_data = data_store.get_data()['users']
    authentic_user = False
    # -1 should never be an actual user ID
    user_id = -1
    for users in user_data:
        if (users['emails'], users['passwords']) == (email, password):
            user_id = users['id']
            return {'auth_user_id': user_id}

    raise InputError("Password or email is incorrect")


# Assumptions: Possible max length password?
# Name cannot contain any characters like .!@#$%^&
def auth_register_v1(email, password, name_first, name_last):
    """
    This function is used to register a user. It will raise an input error
    if the email, password, name or last name are invalid. If the new_users
    infomation is corrent, it will return the new users ID {ID}. Strips all
    special characters from user name.
    """
    # Do not allow passwords of all white space
    password_is_all_spaces = password == (len(password) * ' ')
    if password_is_all_spaces:
        raise InputError("Password cannot be all white space")

    # Formating name to remove special characters
    regex = re.compile(r"[^a-zA-Z0-9-]")
    name_first = regex.sub("", name_first)
    name_last = regex.sub("", name_last)

    # name_last = re.sub(illegal_characters, '', name_last)

    # Used to check that the email is valid
    regex  = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$"
    is_valid_email = re.match(regex, email)

    # Gets a dictionary for the emails ie: 'emails' : [...]
    user_emails = data_store.get('emails')
    is_not_already_registered = not email in user_emails['emails']

    is_valid_password = len(password) >= 6 and len(password) <= 100
    is_valid_name_first = len(name_first) >= 1 and len(name_first) <= 50
    is_valid_name_last = len(name_last) >= 1 and len(name_last) <= 50

    if not (is_valid_email and is_valid_password and is_valid_name_last and
            is_valid_name_first and is_not_already_registered):
        # RAISE ERROR
        raise InputError("There was a problem with the user registration data")

    else:
        # REGISTER USER
        user_data = data_store.get_data()['users']
        new_user_id = len(user_data) + 1
        user_data.append({
            'id' : new_user_id,
            'names' : name_first,
            'name_lasts' : name_last,
            'emails' : email,
            'passwords': password,
            'handle' : generate_handle(name_first, name_last),
            'channels' : []
        })
        return {'auth_user_id': new_user_id}

#Assumption: Possible max handle? throw error if handle is over 30? 100?
def generate_handle(name_first, name_last):
    """
    Given a first and last name, it will generate a handle for the user.
    A handle is generated that is the concatenation of their casted-to-lowercase
    alphanumeric (a-z0-9) first name and last name . If the concatenation is
    longer than 20 characters, it is cut off at 20 characters. If it is too
    short than numbers are added until it is a length of 20. If it is 20 characters
    and this handle is already taken, then it may go over.
    """
    # Used just to filter out any hyphens in the name
    user_handle = re.sub(r'\W+', '', name_first + name_last)
    user_handle = user_handle[:20]
    user_handle = user_handle.lower()

    # more than 20 if the user is already there
    is_valid_handle = not user_handle in data_store.get('handle')['handle']
    i = 0
    while not is_valid_handle:
        is_valid_handle = not (user_handle + str(i)) in data_store.get('handle')['handle']
        if is_valid_handle:
            user_handle = user_handle + str(i)
        i += 1
        
    return user_handle
