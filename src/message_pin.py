'''Contains message pin and unpin'''
from src.data_store import data_store, update_permanent_storage, get_u_id
from src.error import InputError
from src.error import AccessError

def message_pin_v1(token, message_id):
    """
    Marks a message as pinned in a channel/DM.
    
    Args:
        token: The generated token of user sending message.
        message_id: The integer id of the message

    Returns:
        {}

    Raises:
        Input Error: - message_id is not a valid id in channels/dms 
                       the user is in
                     - the message already pinned
        Access Error:- token not valid
                     - user does not have perms in channel/dm
    """
    # Check if a token is valid
    all_tokens = data_store.get('token')['token']
    token_exists = False

    for user_tokens in all_tokens:
        if token in user_tokens:
            token_exists = True

    if not token_exists:
        raise AccessError("Token doesn't exist")

    channel_data = data_store.get_data()['channels']
    dm_data = data_store.get_data()['DMs']
    global_data = data_store.get_data()['global_owners']
    user_id = get_u_id(token)

    message_id_valid = False
    message_pinned = False
    user_has_perm = False

    # check if message_id refers to a valid msg within channel user is in
    # then check if the use has perms and if the message is pinned
    for channel in channel_data:
        for msg in channel['messages']:
            if msg['message_id'] == message_id and user_id in channel['users_id']:
                message_id_valid = True
                message_pinned = msg['is_pinned']
                user_is_owner = user_id in channel['owner_id']
                user_has_glob_perms = get_u_id(token) in global_data and get_u_id(token) in channel['users_id']
                user_has_perm = user_is_owner or user_has_glob_perms

    # check if message_id refers to a valid msg within DM user is in
    # then check if the use has perms and if the message is pinned
    for dm in dm_data:
        for msg in dm['messages']:
            if msg['message_id'] == message_id:
                for members in dm['members']:
                    if user_id == members['u_id']:
                        message_id_valid = True
                        message_pinned = msg['is_pinned']
                        if user_id == dm['owner']:
                            user_has_perm = True

    if not message_id_valid:
        raise InputError("message_id is not valid")

    if message_pinned:
        raise InputError("Message is already pinned")

    if not user_has_perm:
        raise AccessError("User doesn't have permission to pin message")

    # when message is in a channel
    for channel in channel_data:
        for msg in channel['messages']:
            if msg['message_id'] == message_id:
                msg['is_pinned'] = True

    # when message is in a DM
    for dm in dm_data:
        for msg in dm['messages']:
            if msg['message_id'] == message_id:
                msg['is_pinned'] = True

    update_permanent_storage()
    return {}

def message_unpin_v1(token, message_id):
    """
    Marks a message as unpinned in a channel/DM.
    
    Args:
        token: The generated token of user sending message.
        message_id: The integer id of the message

    Returns:
        {}

    Raises:
        Input Error: - message_id is not a valid id in channels/dms 
                       the user is in
                     - the message not pinned
        Access Error:- token not valid
                     - user does not have perms in channel/dm
    """
    # Check if a token is valid
    all_tokens = data_store.get('token')['token']
    token_exists = False

    for user_tokens in all_tokens:
        if token in user_tokens:
            token_exists = True

    if not token_exists:
        raise AccessError("Token doesn't exist")

    channel_data = data_store.get_data()['channels']
    dm_data = data_store.get_data()['DMs']
    global_data = data_store.get_data()['global_owners']
    user_id = get_u_id(token)

    message_id_valid = False
    message_pinned = False
    user_has_perm = False

    # check if message_id refers to a valid msg within channel user is in
    # then check if the use has perms and if the message is pinned
    for channel in channel_data:
        for msg in channel['messages']:
            if msg['message_id'] == message_id and user_id in channel['users_id']:
                message_id_valid = True
                message_pinned = msg['is_pinned']
                user_is_owner = user_id in channel['owner_id']
                user_has_glob_perms = get_u_id(token) in global_data and get_u_id(token) in channel['users_id']
                user_has_perm = user_is_owner or user_has_glob_perms

    # check if message_id refers to a valid msg within DM user is in
    # then check if the use has perms and if the message is pinned
    for dm in dm_data:
        for msg in dm['messages']:
            if msg['message_id'] == message_id:
                for members in dm['members']:
                    if user_id == members['u_id']:
                        message_id_valid = True
                        message_pinned = msg['is_pinned']
                        if user_id == dm['owner']:
                            user_has_perm = True

    if not message_id_valid:
        raise InputError("message_id is not valid")

    if not message_pinned:
        raise InputError("Message is not already pinned")

    if not user_has_perm:
        raise AccessError("User doesn't have permission to pin message")

    # when message is in a channel
    for channel in channel_data:
        for msg in channel['messages']:
            if msg['message_id'] == message_id:
                msg['is_pinned'] = False

    # when message is in a DM
    for dm in dm_data:
        for msg in dm['messages']:
            if msg['message_id'] == message_id:
                msg['is_pinned'] = False

    update_permanent_storage()
    return {}
