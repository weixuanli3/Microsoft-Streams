'''Contains all admin related functions, such as removing users and permissions'''
from src.data_store import data_store, update_permanent_storage, get_u_id
from src.error import InputError
from src.error import AccessError

def admin_user_remove_id(token, u_id):
    """
    Remove a user from the Streams
    
    Given a user by their u_id, remove them from the Streams. 
    This means they should be removed from all channels/DMs, 
    and will not be included in the list of users returned by users/all. 
    Streams owners can remove other Streams owners (including the original first owner). 
    Once users are removed, the contents of the messages they sent will be replaced by 'Removed user'. 
    Their profile must still be retrievable with user/profile, however name_first should be 'Removed' 
    and name_last should be 'user'. The user's email and handle should be reusable.

    Args:
        token: The generated token of user removing a user.
        u_id: integer value id of the user being removed

    Returns:
        An empty dictionary

    Raises:
        Input Error: - Cannot remove only global user.
                     - u_id doesn't exist

        Access Error: - The token does not exist
                      - token doesn't belong to a global user
    """    
    # Check a token is valid
    all_tokens = data_store.get('token')['token']
    token_exists = False
    for user_tokens in all_tokens:
        if token in user_tokens:
            token_exists = True

    if not token_exists:
        raise AccessError

    global_users = data_store.get_data()['global_owners']

    # Removing only global user
    if len(global_users) == 1 and u_id in global_users:
        raise InputError('You cannot remove the only global user')

    # Check token belong to a global user
    if get_u_id(token) not in global_users:
        raise AccessError('You need to be a global owner to do that')

    # Checks if user does not exist
    user_ids = data_store.get('id')['id']
    if u_id not in user_ids:
        raise InputError('User does not exist')

    # Remove user from all channels
    all_channels = data_store.get_data()['channels']
    for channel in all_channels:
        if u_id in channel['users_id']:
            channel['users_id'].remove(u_id)

            # Removes all messages from channels:
            all_messages = channel['messages']

            for messages in all_messages:
                if messages['u_id'] == u_id:
                    messages['message'] = 'Removed user'            
            
        # If the user is the owner
        if u_id in channel['owner_id']:
            channel['owner_id'].remove(u_id)

    # Find correct user
    all_users = data_store.get_data()['users']
    for user in all_users:
        if user['id'] == u_id:
            currect_user = user

    # Scan though all DMs, if they are in it, replace all their messages with 'Removed user'
    all_dms = data_store.get_data()['DMs']
    for chat in all_dms:
        for users in chat['members']:
            if u_id == users['u_id'] :
                chat['members'].remove({
                    'u_id': currect_user['id'],
                    'email': currect_user['emails'],
                    'name_first': currect_user['names'],
                    'name_last': currect_user['name_lasts'],
                    'handle_str': currect_user['handle']
                    }
                )
                messages = chat['messages']

                for message in messages:
                    if message['u_id'] == u_id:
                        message['message'] = 'Removed user'

    # Changes the user info
    # print("Removing",user['names'])

    currect_user['names'] = 'Removed'
    currect_user['name_lasts'] = 'user'
    currect_user['channels'] = []
    currect_user['is_removed'] = True
    currect_user['token'] = []
    update_permanent_storage()
    return {}

    
def admin_userpermission_change_v1(token, u_id, permission_id):
    """
    Changes a user's permissions
    
    Given a user by their user ID, set their permissions to new 
    permissions described by permission_id.

    Args:
        token: The generated token of user changing a user's
        permissions.
        u_id: integer value id of the userwhose permissions
        are being changed.

    Returns:
        An empty dictionary

    Raises:
        Input Error: - Invalid permission id.
                     - u_id doesn't exist
                     - changing global user to a gloabl user
                     - changing a user to a user

        Access Error: - The token does not exist
                      - token doesn't belong to a global user
                      - changing permission of only global user
    """
    # Check a token is valid
    all_tokens = data_store.get('token')['token']
    token_exists = False
    for user_tokens in all_tokens:
        if token in user_tokens:
            token_exists = True

    if not token_exists:
        raise AccessError
    
    # permission_id is invalid
    if permission_id not in [1,2]:
        raise InputError('Invalid permission ID')

    # u_id does not refer to a valid user
    all_u_ids = data_store.get('id')['id']
    if u_id not in all_u_ids:
        raise InputError('Not valid ID')
    
    # the authorised user is not a global owner
    global_owners = data_store.get_data()['global_owners']
    if get_u_id(token) not in global_owners:
        raise AccessError('You need to be a global owner to do this')

    # u_id refers to a user who is the only global owner and they are being demoted to a user
    if len(global_owners) == 1 and u_id in global_owners and permission_id == 2:
        raise InputError('You are removing the only global user')

    # Change permissions
    if permission_id == 1:
        if u_id not in global_owners:
            global_owners.append(u_id)
        else:
            raise InputError('You are changing a global user to global user')
    else:
        if u_id in global_owners:
            global_owners.remove(u_id)
        else:
            raise InputError('You are changing a user to a user')

    update_permanent_storage()
    return {}