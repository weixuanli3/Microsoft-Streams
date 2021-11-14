'''Contains extra functions, channel_kick and dm_kick'''
from src.data_store import data_store, update_permanent_storage, get_u_id

from src.user import update_user_stats
from src.error import InputError
from src.error import AccessError

def channel_kick_v1(token, channel_id, user_id):
    """
    The specified user gets kicked from the channel

    Args:
        token: The generated token of user kicking the individual.
        channel_id: The integer id of the channel where the kicking takes place
        user_id: The user_id of the user getting kicked

    Returns:
        An empty dictionary.

    Raises:
        Input Error: - the channel id inputted does not exist
                     - the user is not part of channel

        Access Error: - The token does not exist
                      - token not part of the channel
                      - token doesn't have permission in channel

    """    
    user_data = data_store.get_data()['users']
    channel_data = data_store.get_data()['channels']
    global_data = data_store.get_data()['global_owners']

    # checking token
    valid_token = False
    for user in user_data:
        if token in user['token']:
            valid_token = True

    if not valid_token:
        raise AccessError("Invalid Token")

    # turn token into user_id
    auth_user_id = get_u_id(token)

    user_id_valid = False

    # checking user_id
    for user in user_data:
        if user_id == user['id']:
            user_id_valid = True

    if not user_id_valid:
        raise InputError("user_id is not valid")

    # checking for errors
    channel_exists = False
    token_in_channel = False
    user_in_channel = False
    token_has_perm = False

    for channel in channel_data:
        if channel_id == channel['chan_id']:
            channel_exists = True
            if auth_user_id in channel['users_id']:
                token_in_channel = True
            if user_id in channel['users_id']:
                user_in_channel = True
            token_is_owner = auth_user_id in channel['owner_id']
            token_has_glob_perms = auth_user_id in global_data and auth_user_id in channel['users_id']
            token_has_perm = token_is_owner or token_has_glob_perms

    if not channel_exists:
        raise InputError("Channel doesn't exist")
    
    if not token_in_channel:
        raise AccessError("User that is kicking is not part of the channel")

    if not user_in_channel:
        raise InputError("User that is being kicked is not part of the channel")

    if not token_has_perm:
        raise AccessError("User that is kicking does not have permission to kick")

    # remove the channel from the user
    for user in user_data:
        if user['id'] == user_id:
            user['channels'].remove(channel_id)

    # remove the user from the channel
    channel_data[channel_id - 1]['users_id'].remove(user_id)

    if user_id in channel_data[channel_id - 1]['owner_id']:
        channel_data[channel_id - 1]['owner_id'].remove(user_id)

    update_user_stats(user_id, "channels_joined", False)
    update_permanent_storage()

    return {}

def dm_kick_v1(token, dm_id, user_id):
    """
    The specified user gets kicked from the dm

    Args:
        token: The generated token of user kicking the individual.
        dm_id: The integer id of the channel where the kicking takes place
        user_id: The user_id of the user getting kicked

    Returns:
        An empty dictionary.

    Raises:
        Input Error: - the dm id inputted does not exist
                     - the user is not part of dm

        Access Error: - The token does not exist
                      - token not part of the dm
                      - token doesn't have permission in dm

    """    
    user_data = data_store.get_data()['users']
    dm_data = data_store.get_data()['DMs']
    global_data = data_store.get_data()['global_owners']

    # checking token
    valid_token = False
    for user in user_data:
        if token in user['token']:
            valid_token = True

    if not valid_token:
        raise AccessError("Invalid Token")

    # turn token into user_id
    auth_user_id = get_u_id(token)

    user_id_valid = False

    # checking user_id
    for user in user_data:
        if user_id == user['id']:
            user_id_valid = True

    if not user_id_valid:
        raise InputError("user_id is not valid")

    # checking for errors
    dm_exists = False
    token_in_dm = False
    user_in_dm = False
    token_has_perm = False

    for dm in dm_data:
        if dm_id == dm['dm_id']:
            dm_exists = True
            for dm_member in dm['members']:
                if auth_user_id == dm_member['u_id']:
                    token_in_dm = True
                if user_id == dm_member['u_id']:
                    user_in_dm = True
            if auth_user_id == dm['owner']:
                user_in_dm = True
                token_has_perm = True

    if not dm_exists:
        raise InputError("DM doesn't exist")
    
    if not token_in_dm:
        raise AccessError("User that is kicking is not part of the DM")

    if not user_in_dm:
        raise InputError("User that is being kicked is not part of the DM")

    if not token_has_perm:
        raise AccessError("User that is kicking does not have permission to kick")

    # removing user from dm
    for dm in dm_data:
        if dm_id == dm['dm_id']:
            for dm_member in dm['members']:
                if user_id == dm_member['u_id']:
                    dm['members'].remove(dm_member)

    update_user_stats(user_id, "dms_joined", False)
    update_permanent_storage()

    return {}