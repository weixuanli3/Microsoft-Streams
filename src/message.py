'''Contains all functions related to sending, editing and deleting messages'''
from src.data_store import data_store, update_permanent_storage, get_u_id
from src.user import update_workspace_stats, update_user_stats
from src.error import InputError
from src.error import AccessError
from src.notifications import helper_tagged_add_notif
from datetime import datetime
import datetime as dt

def message_send_v1(token, channel_id, message):
    """
    Sends a message in a channel.
    
    Send a message from the authorised user to the channel specified by channel_id. 
    Note: Each message should have its own unique ID, i.e. no messages should share 
    an ID with another message, even if that other message is in a different channel.

    Args:
        token: The generated token of user sending message.
        channel_id: The integer id of the channel the user is
        sending the message in.
        message: The string of the message the user wants to send.

    Returns:
        {'message_id' : message_id}

    Raises:
        Input Error: - The channel id does not exist
                     - Length of message not valid

        Access Error: - The token does not exist
                      - The token is not part of the channel.
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
    msgs = data_store.get_data()['msgs']
    user_id = get_u_id(token)

    channel_exists = False
    user_in_channel = False
    message_len_valid = (len(message) >= 1 and len(message) <= 1000)

    # check if the channel exists and if the user is in the channel
    for channel in channel_data:
        if channel_id == channel['chan_id']:
            channel_exists = True
            if user_id in channel['users_id']:
                user_in_channel = True

    if not channel_exists:
        raise InputError("Channel ID not valid")

    if not user_in_channel:
        raise AccessError("User isn't part of the channel")

    if not message_len_valid:
        raise InputError("Length of message is not valid")

    # creating message_id and timestamp
    message_id = len(msgs) + 1
    time = datetime.now()
    timestamp = int(datetime.timestamp(time))

    message = {
        'message_id' : message_id,
        'u_id' : user_id,
        'message' : message,
        'time_created' : timestamp,
        'reacts' : [],
        'is_pinned' : False
    }

    # adding message to channel_data
    for channel in channel_data:
        if channel['chan_id'] == channel_id:
            channel['messages'].append(message)
            parsed_channel = channel

    # updating msgs
    msgs.append(message_id)

    helper_tagged_add_notif(token, message, parsed_channel, -1)
    update_workspace_stats("messages_exist", True)
    update_user_stats(user_id, "messages_sent", True)
    update_permanent_storage()
    return {'message_id' : message_id}

def message_edit_v1(token, message_id, message):
    """
    Edits a message in a channel
    
    Given a message, update its text with new text. 
    If the new message is an empty string, the message is deleted.

    Args:
        token: The generated token of user editing the message.
        message_id: The integer id of the message the user is
        editing.
        message: The string of the message the user wants to change
        the original message to.

    Returns:
        An empty dictionary

    Raises:
        Input Error: - The message_id does not exist
                     - Length of message not valid

        Access Error: - The token does not exist
                      - User doesn't have owner permission
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
    user_has_perm = False
    message_len_valid = (len(message) <= 1000)

    # check if message_id refers to a valid msg within channel user is in
    # then check if user sent the msg or has perms in channel
    for channel in channel_data:
        for msg in channel['messages']:
            if msg['message_id'] == message_id and user_id in channel['users_id']:
                message_id_valid = True
                sent_by_user = (msg['u_id'] == user_id)
                user_is_owner = user_id in channel['owner_id']
                user_has_glob_perms = get_u_id(token) in global_data and get_u_id(token) in channel['users_id']
                user_has_perm = sent_by_user or user_is_owner or user_has_glob_perms

    # check if message_id refers to a valid msg within DM user is in
    for dm in dm_data:
        for msg in dm['messages']:
            if msg['message_id'] == message_id:
                for members in dm['members']:
                    if user_id == members['u_id']:
                        message_id_valid = True
                        if msg['u_id'] == user_id or user_id == dm['owner']:
                            user_has_perm = True

    if not message_id_valid:
        raise InputError("message_id is not valid")

    if not user_has_perm:
        raise AccessError("User does not have owner permission and can't edit message")

    if not message_len_valid:
        raise InputError("Length of message is not valid")

    parsed_channel = -1
    parsed_dm = -1    
    
    # editing msg in channel
    for channel in channel_data:
        for msg in channel['messages']:
            if msg['message_id'] == message_id:
                parsed_msg = msg
                parsed_channel = channel
                if len(message) == 0:
                    channel['messages'].remove(msg)
                else:
                    msg['message'] = message

    # editing msg in DM
    for dm in dm_data:
        for msg in dm['messages']:
            if msg['message_id'] == message_id:
                parsed_msg = msg
                parsed_dm = dm
                if len(message) == 0:
                    dm['messages'].remove(msg)
                else:
                    msg['message'] = message

    update_permanent_storage()
    
    helper_tagged_add_notif(token, parsed_msg, parsed_channel, parsed_dm)
    
    return {}

def message_senddm_v1(token, dm_id, message):
    """
    ESends a message in a dm.
    
    Send a message from authorised_user to the DM specified by dm_id. 
    Note: Each message should have it's own unique ID, i.e. no messages 
    should share an ID with another message, even if that other message 
    is in a different channel or DM.

    Args:
        token: The generated token of user sending the message.
        dm_id: The integer id of the dm the user is sending
        the message in.
        message: The string of the message the user wants to send.

    Returns:
        {'message_id' : message_id}

    Raises:
        Input Error: - The dm_id does not exist
                     - Length of message not valid

        Access Error: - The token does not exist
                      - User not part of DM
    """
    # Check if a token is valid
    all_tokens = data_store.get('token')['token']
    token_exists = False

    for user_tokens in all_tokens:
        if token in user_tokens:
            token_exists = True

    if not token_exists:
        raise AccessError("Token doesn't exist")

    dm_data = data_store.get_data()['DMs']
    msgs = data_store.get_data()['msgs']
    user_id = get_u_id(token)

    dm_exists = False
    user_in_dm = False
    message_len_valid = (len(message) >= 1 and len(message) <= 1000)

    # check if the dm exists and if the user is in the dm
    for dm in dm_data:
        if dm_id == dm['dm_id']:
            dm_exists = True
            for members in dm['members']:
                if user_id == members['u_id']:
                    user_in_dm = True

    if not dm_exists:
        raise InputError("DM ID not valid")

    if not user_in_dm:
        raise AccessError("User isn't part of the DM")

    if not message_len_valid:
        raise InputError("Length of message is not valid")

    # creating message_id and timestamp
    message_id = len(msgs) + 1
    time = datetime.now()
    timestamp = int(datetime.timestamp(time))

    message = {
        'message_id' : message_id,
        'u_id' : user_id,
        'message' : message,
        'time_created' : timestamp,
        'reacts' : [],
        'is_pinned' : False
    }

    # adding message to dm_data
    for dm in dm_data:
        if dm['dm_id'] == dm_id:
            dm['messages'].append(message)
            parsed_dm = dm

    # updating msgs
    msgs.append(message_id)
    
    helper_tagged_add_notif(token, message, -1, parsed_dm)
    update_workspace_stats("messages_exist", True)
    update_user_stats(user_id, "messages_sent", True)
    update_permanent_storage()
    return {'message_id' : message_id}
    
def message_remove_v1(token, message_id):
    """
    Given a message_id for a message, this message is removed from the channel/DM

    Args:
        token: The generated token of user removing the message.
        message_id: The integer id of the message the user is
        removing.


    Returns:
        An empty dictionary

    Raises:
        Input Error: - The message_id does not exist

        Access Error: - The token does not exist
                      - User doesn't have owner permission
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
    user_has_perm = False

    # check if message_id refers to a valid msg within channel user is in
    # then check if user sent the msg or has perms in channel
    for channel in channel_data:
        for msg in channel['messages']:
            if msg['message_id'] == message_id and user_id in channel['users_id']:
                message_id_valid = True
                sent_by_user = (msg['u_id'] == user_id)
                user_is_owner = user_id in channel['owner_id']
                user_has_glob_perms = get_u_id(token) in global_data and get_u_id(token) in channel['users_id']
                user_has_perm = sent_by_user or user_is_owner or user_has_glob_perms

    # check if message_id refers to a valid msg within DM user is in
    for dm in dm_data:
        for msg in dm['messages']:
            if msg['message_id'] == message_id:
                for members in dm['members']:
                    if user_id == members['u_id']:
                        message_id_valid = True
                        if msg['u_id'] == user_id or user_id == dm['owner']:
                            user_has_perm = True

    if not message_id_valid:
        raise InputError("message_id is not valid")

    if not user_has_perm:
        raise AccessError("User does not have owner permission and can't remove message")

    # removing msg in channel
    for channel in channel_data:
        for msg in channel['messages']:
            if msg['message_id'] == message_id:
                channel['messages'].remove(msg)
                update_workspace_stats("messages_exist", False)
                update_permanent_storage()

    # removing msg in DM
    for dm in dm_data:
        for msg in dm['messages']:
            if msg['message_id'] == message_id:
                dm['messages'].remove(msg)
                update_workspace_stats("messages_exist", False)
                update_permanent_storage()

    return {}

def message_share_v1(token, og_message_id, message, channel_id, dm_id):
    
    user_data = data_store.get_data()['users']
    dm_data = data_store.get_data()['DMs']
    channel_data = data_store.get_data()['channels']
    
    #Check if user token is valid
    valid_token = False
    for user in user_data:
        if token in user['token']:
            valid_token = True

    if not valid_token:
        raise AccessError("Invalid Token")
    
    user_id = get_u_id(token)
    
    #Check if og_message is in a valid channel or dm the user is in
    #Check dm
    valid_message_id_dm = False
    for dm in dm_data:
        for members in dm['members']:
            if user_id == members['u_id']:
                for msg in dm['messages']:
                    if og_message_id == msg['message_id']:
                        valid_message_id_dm = True
                        #Find og_message from id
                        og_message = msg['message']
    
    #Check channels
    valid_message_id_channel = False
    for channel in channel_data:
        if user_id in channel['users_id']:
            for msg in channel['messages']:
                if og_message_id == msg['message_id']:
                    valid_message_id_channel = True
                    #Find og_message from id
                    og_message = msg['message']
    
    if not valid_message_id_channel and not valid_message_id_dm:
        raise InputError("og_message_id does not refer to a valid message within a channel/DM that the authorised user has joined")
    
    #Check if length of message is greater than 1000
    if len(message) > 1000:
        raise InputError("length of message is more than 1000 characters")
    
    #Check if message is a string
    if not isinstance(message, str):
        raise InputError("Message is not a string")
    
    #Check channel/dm ID pair contains a -1
    if channel_id != -1:
        if dm_id != -1:
            #Neither ids are -1
            raise InputError("Neither channel_id nor dm_id are -1")
    elif channel_id == -1:
        if dm_id == -1:
            #Both ids are -1
            raise InputError("Both channel_id and dm_id are invalid")
    
    #If channel_id is not -1
    if channel_id != -1:
    
        channel_exists = False
        user_in_channel = False
        
        #Check if the channel exists and if the user is in the channel
        for channel in channel_data:
            if channel_id == channel['chan_id']:
                channel_exists = True
                if user_id in channel['users_id']:
                    user_in_channel = True
                    #Share to channel
                    shared_message_id = message_send_v1(token, channel_id, f"'Original Message': {og_message}, 'User message': {message}")['message_id']
                    return {"shared_message_id": shared_message_id}

        if not channel_exists:
            raise InputError("Channel ID not valid")

        if not user_in_channel:
            raise AccessError("User isn't part of the channel")

    #If dm_id is not -1
    if dm_id != -1:
        
        dm_exists = False
        user_in_dm = False
        
        #Check if the dm exists and if the user is in the dm
        for dm in dm_data:
            if dm_id == dm['dm_id']:
                dm_exists = True
                for members in dm['members']:
                    if user_id == members['u_id']:
                        user_in_dm = True
                        #Share to dm
                        shared_message_id = message_senddm_v1(token, dm_id, f"'Original Message': {og_message}, 'User message': {message}")['message_id']
                        return {"shared_message_id": shared_message_id}

        if not dm_exists:
            raise InputError("DM ID not valid")

        if not user_in_dm:
            raise AccessError("User isn't part of the DM")