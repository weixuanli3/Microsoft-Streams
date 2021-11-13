'''Contains message react and unreact'''
from src.data_store import data_store, update_permanent_storage, get_u_id
from src.error import InputError
from src.error import AccessError
from src.notifications import helper_reacted_add_notif

def message_react_v1(token, message_id, react_id):
    """
    Reacts to a message in a channel/DM.
    
    Args:
        token: The generated token of user sending message.
        message_id: The integer id of the message
        react_id: id of the react

    Returns:
        {}

    Raises:
        Input Error: - message_id is not a valid id in channels/dms 
                       the user is in
                     - react_id is not valid
                     - the message already contains a react with same
                       react_id from user
        Access Error:- token not valid
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
    user_id = get_u_id(token)

    message_id_valid = False
    react_id_valid = (react_id == 1)
    react_alr_exists = False

    # check if message_id refers to a valid msg within channel user is in
    # then check if the same react already exists from the user
    for channel in channel_data:
        for msg in channel['messages']:
            if msg['message_id'] == message_id and user_id in channel['users_id']:
                message_id_valid = True
                for react in msg['reacts']:
                    if react['user_id'] == user_id and react['react_id'] == react_id:
                        react_alr_exists = True

    # check if message_id refers to a valid msg within DM user is in
    # then check if the same react already exists from the user
    for dm in dm_data:
        for msg in dm['messages']:
            if msg['message_id'] == message_id:
                for members in dm['members']:
                    if user_id == members['u_id']:
                        message_id_valid = True
                    for react in msg['reacts']:
                        if react['user_id'] == user_id and react['react_id'] == react_id:
                            react_alr_exists = True

    if not message_id_valid:
        raise InputError("message_id is not valid")

    if not react_id_valid:
            raise InputError("react_id is not valid")

    if react_alr_exists:
        raise InputError("User has already reacted to message with same react")

    # adding react to message
    react = {
        'user_id' : user_id,
        'react_id' : react_id
    }

    # when message is in a channel
    for channel in channel_data:
        for msg in channel['messages']:
            if msg['message_id'] == message_id:
                msg['reacts'].append(react)
                helper_reacted_add_notif(token, msg, channel, -1)

    # when message is in a DM
    for dm in dm_data:
        for msg in dm['messages']:
            if msg['message_id'] == message_id:
                msg['reacts'].append(react)
                helper_reacted_add_notif(token, msg, -1, dm)

    update_permanent_storage()
    return {}

def message_unreact_v1(token, message_id, react_id):
    """
    Removes react to a message in a channel/DM.
    
    Args:
        token: The generated token of user sending message.
        message_id: The integer id of the message
        react_id: id of the react

    Returns:
        {}

    Raises:
        Input Error: - message_id is not a valid id in channels/dms 
                       the user is in
                     - react_id is not valid
                     - the message doesn't contains a react with same
                       react_id from user
        Access Error:- token not valid
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
    user_id = get_u_id(token)

    message_id_valid = False
    react_id_valid = (react_id == 1)
    react_alr_exists = False

    # check if message_id refers to a valid msg within channel user is in
    # then check if the same react already exists from the user
    for channel in channel_data:
        for msg in channel['messages']:
            if msg['message_id'] == message_id and user_id in channel['users_id']:
                message_id_valid = True
                for react in msg['reacts']:
                    if react['user_id'] == user_id and react['react_id'] == react_id:
                        react_alr_exists = True

    # check if message_id refers to a valid msg within DM user is in
    # then check if the same react already exists from the user
    for dm in dm_data:
        for msg in dm['messages']:
            if msg['message_id'] == message_id:
                for members in dm['members']:
                    if user_id == members['u_id']:
                        message_id_valid = True
                    for react in msg['reacts']:
                        if react['user_id'] == user_id and react['react_id'] == react_id:
                            react_alr_exists = True

    if not message_id_valid:
        raise InputError("message_id is not valid")

    if not react_id_valid:
        raise InputError("react_id is not valid")

    if not react_alr_exists:
        raise InputError("User hasn't already reacted to message with react")

    # removing react to message
    react = {
        'user_id' : user_id,
        'react_id' : react_id
    }

    # when message is in a channel
    for channel in channel_data:
        for msg in channel['messages']:
            if msg['message_id'] == message_id:
                msg['reacts'].remove(react)

    # when message is in a DM
    for dm in dm_data:
        for msg in dm['messages']:
            if msg['message_id'] == message_id:
                msg['reacts'].remove(react)

    update_permanent_storage()
    return {}