'''Contains all admin related functions, such as removing users and permissions'''
from src.data_store import data_store, update_permanent_storage, get_u_id
from src.error import InputError
from src.error import AccessError

def admin_user_remove_id(token, u_id):
    
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

    # Checks if user does not exist
    user_ids = data_store.get('id')['id']
    if u_id not in user_ids:
        raise InputError('User does not exist')

    # Remove user from all channels
    all_channels = data_store.get_data()['channels']
    for channel in all_channels:
        if u_id in channel['users_id']:
            channel['users_id'].remove(u_id)

    # Find correct user
    all_users = data_store.get_data()['users']
    for user in all_users:
        if user['id'] == u_id:
            currect_user = user

    # Scan though all chats, if they are in it, replace all their messages with 'Removed user'
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
    
    global_owners = data_store.get_data()['global_owners']
    # the authorised user is not a global owner
    if get_u_id(token) not in global_owners:
        raise AccessError('You need to be a global pwner to do this')

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