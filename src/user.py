'''Contains all functions that relate to the user profile'''
from src.data_store import data_store, update_permanent_storage
from src.error import InputError, AccessError
import re

def users_all_v1(token):
    """
    Returns a list of all users and their associated details.

    Args:
        token: The generated token of user getting all user's details.

    Returns:
        [{
                'u_id': user['id'],
                'email': user['emails'],
                'name_first': user['names'],
                'name_last': user['name_lasts'],
                'handle_str': user['handle']
            }]

    Raises:

        Access Error: - The token does not exist
    """
    # Check if the user has been removed first
    # If they have, dont display
    user_data = data_store.get_data()['users']

    valid_token = False
    for user in user_data:
        if token in user['token']:
            valid_token = True

    if not valid_token:
        raise AccessError("Invalid Token")

    user_dict = {'users': []}
    for user in user_data:
        if user['is_removed'] == False:
            user_dict['users'].append({
                'u_id': user['id'],
                'email': user['emails'],
                'name_first': user['names'],
                'name_last': user['name_lasts'],
                'handle_str': user['handle']
            })
    return user_dict
    #Return type {users}

def user_profile_v1(token, u_id):
    """
    For a valid user, returns information about their user_id, email, 
    first name, last name, and handle

    Args:
        token: The generated token of user getting a user's details.

    Returns:
        {
                'u_id': user['id'],
                'email': user['emails'],
                'name_first': user['names'],
                'name_last': user['name_lasts'],
                'handle_str': user['handle']
            }

    Raises:
        Input Error: - u_id does not exist

        Access Error: - The token does not exist
    """
    user_data = data_store.get_data()['users']

    valid_token = False
    for user in user_data:
        if token in user['token']:
            valid_token = True

    if not valid_token:
        raise AccessError("Invalid Token")

    user_exists = False
    for user in user_data:
        if user['id'] == u_id:
            user_exists = True
            requested_user = {
                'u_id': user['id'],
                'email': user['emails'],
                'name_first': user['names'],
                'name_last': user['name_lasts'],
                'handle_str': user['handle']
            }
    
    if not user_exists:
        raise InputError("User id does not refer to a valid user")
    
    return {'user': requested_user}
    #Return type {user}
    
def user_profile_setname_v1(token, name_first, name_last):
    """
    Update the authorised user's first and last name

    Args:
        token: The generated token of user changing their name.

    Returns:
        An empty dictionary

    Raises:
        Input Error: - Name not correct length

        Access Error: - The token does not exist
    """
    user_data = data_store.get_data()['users']
    valid_token = False
    for user in user_data:
        if token in user['token']:
            valid_token = True

    if not valid_token:
        raise AccessError("Invalid Token")    
    
    first_name_valid = (len(name_first) in range(1, 51))
    second_name_valid = (len(name_last) in range(1, 51))
    if not first_name_valid or not second_name_valid:
        raise InputError("Name is not of correct length")

    # Update the name
    # ASSUMPTION: Names cannot have characters not used in names
    # Formating name to remove special characters
    regex = re.compile(r"[^a-zA-Z0-9-]")
    name_first = regex.sub("", name_first)
    name_last = regex.sub("", name_last)

    for user in user_data:
        if token in user['token']:
            user['names'] = name_first
            user['name_lasts'] = name_last
    update_permanent_storage()
    return {}
    #Return type {}
    
def user_profile_setemail_v1(token, email):
    """
    Update the authorised user's email address

    Args:
        token: The generated token of user changing their email.

    Returns:
        An empty dictionary

    Raises:
        Input Error: - Invalid email

        Access Error: - The token does not exist
    """
    user_data = data_store.get_data()['users']
    valid_token = False
    for user in user_data:
        if token in user['token']:
            valid_token = True

    if not valid_token:
        raise AccessError("Invalid Token")
    # Used to check that the email is valid
    regex  = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$"
    is_valid_email = re.match(regex, email)

    # Gets a dictionary for the emails ie: 'emails' : [...]
    user_emails = data_store.get('emails')
    is_not_already_registered = not email in user_emails['emails']

    if is_valid_email and is_not_already_registered:
        for user in user_data:
            if token in user['token']:
                user['emails'] = email
    else:
        raise InputError("Invalid email input")
    update_permanent_storage()
    return {}
    #Return type {}

def user_profile_sethandle_v1(token, handle_str):
    """
    Update the authorised user's handle (i.e. display name)

    Args:
        token: The generated token of user changing their handle.

    Returns:
        An empty dictionary

    Raises:
        Input Error: - Invalid length of handle
                     - Handle can't contain non-alphanumeric characters
                     - Handle already taken

        Access Error: - The token does not exist
    """
    user_data = data_store.get_data()['users']
    valid_token = False
    for user in user_data:
        if token in user['token']:
            valid_token = True

    if not valid_token:
        raise AccessError("Invalid Token")

    if len(handle_str) not in range(3, 21):
        raise InputError("Invalid length of handle_str")
    
    is_not_alpha_numeric = any(not i.isalnum() for i in handle_str)
    if is_not_alpha_numeric:
        raise InputError("Handle cannot contain non-alphanumeric characters")

    for user in user_data:
        if user['handle'] == handle_str:
            raise InputError("Handle already taken")
    
    for user in user_data:
        if token in user['token']:
            user['handle'] = handle_str
    update_permanent_storage()
    return {}
    #Return type {}
