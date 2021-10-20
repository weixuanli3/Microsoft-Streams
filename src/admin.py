'''Contains all admin related functions, such as removing users and permissions'''
from src.data_store import data_store, get_u_id
from src.error import InputError
from src.error import AccessError

# from data_store import data_store, get_u_id
# from error import InputError
# from error import AccessError
# from auth import auth_register_v1
# from other import clear_v1

def admin_user_remove_id(token, u_id):

    global_users = data_store.get_data()['global_owners']

    if len(global_users) == 1 and u_id in global_users:
        raise AccessError('You cannot remove the only global user')

    user_ids = data_store.get('id')['id']
    if u_id not in user_ids:
        raise InputError('User does not exist')

    # Changes the user info
    all_users = data_store.get_data()['users']
    for user in all_users:
        if user['id'] == u_id:

            print("Removing",user['names'])

            user['names'] = 'Removed'
            user['name_lasts'] = 'user'
            user['channels'] = []
            user['is_removed'] = True
            user['token'] = []

    # Remove user from all channels
    all_channels = data_store.get_data()['channels']
    for channel in all_channels:
        if u_id in channel['users_id']:
            channel['users_id'].remove(u_id)

    all_dms = data_store.get_data()['DMs']
    # Scan though all chats, if they are in it, replace all their messages with 'Removed user'
    for chat in all_dms:
        if u_id in chat['members']:
            # chat['members'].remove(u_id)
            messages = chat['messages']

            for message in messages:
                if message['u_id'] == u_id:
                    message['message'] = 'Removed user'

    return {}

    
def admin_userpermission_change_v1(token, u_id, permission_id):
    # permission_id is invalid
    if permission_id not in [1,2]:
        raise InputError('Invalid permission ID')

    # u_id does not refer to a valid user
    all_u_ids = data_store.get('id')['id']
    if u_id not in all_u_ids:
        raise InputError('Not valid ID')

    # Check a token is valid
    all_tokens = data_store.get('token')['token']
    token_exists = False
    for user_tokens in all_tokens:
        if token in user_tokens:
            token_exists = True

    if not token_exists:
        raise InputError

    # u_id refers to a user who is the only global owner and they are being demoted to a user
    global_owners = data_store.get_data()['global_owners']
    if len(global_owners) == 1 and u_id in global_owners and permission_id == 2:
        raise InputError('You are removing the only global user')
    
    # the authorised user is not a global owner
    if get_u_id(token) not in global_owners:
        raise AccessError('You need to be a global pwner to do this')

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

    return {}