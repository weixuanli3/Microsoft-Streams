'''Contains all functions related to sending, editing and deleting messages'''
from src.data_store import data_store, update_permanent_storage, get_u_id
from src.user import update_workspace_stats, update_user_stats
from src.error import InputError
from src.error import AccessError
from datetime import datetime
import threading

def message_sendlater_v1(token, channel_id, message, time_sent):
    """
    Sends a message in a channel at a specified time.
    
    Send a message from the authorised user to the channel specified by channel_id. 
    Note: Each message should have its own unique ID, i.e. no messages should share 
    an ID with another message, even if that other message is in a different channel.

    Args:
        token: The generated token of user sending message.
        channel_id: The integer id of the channel the user is
        sending the message in.
        message: The string of the message the user wants to send.
        time_sent: time for the message to be sent

    Returns:
        {'message_id' : message_id}

    Raises:
        Input Error: - The channel id does not exist
                     - Length of message not valid
                     - Time sent is a time in the past

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
    user_id = get_u_id(token)
    now = datetime.timestamp(datetime.now())

    channel_exists = False
    user_in_channel = False
    message_len_valid = (len(message) >= 1 and len(message) <= 1000)
    time_valid = (now < time_sent)

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

    if not time_valid:
        raise InputError("Time for the message to be sent is in the past")

    # creating message_id
    msgs = data_store.get_data()['msgs']
    message_id = len(msgs) + 1

    # updating msgs
    msgs.append(message_id)

    def job():
        message_data = {
            'message_id' : message_id,
            'u_id' : user_id,
            'message' : message,
            'time_created' : int(time_sent),
            'reacts' : [],
            'is_pinned' : False
        }

        # adding message to channel_data
        for channel in channel_data:
            if channel['chan_id'] == channel_id:
                channel['messages'].append(message_data)

        update_workspace_stats('messages_exist', True)
        update_user_stats(user_id, 'messages_sent', True)
        update_permanent_storage()

    # delaying the message
    delay = int(time_sent) - int(now)
    t = threading.Timer(delay, job)
    t.start()

    update_permanent_storage()
    return {'message_id' : message_id}

def message_sendlaterdm_v1(token, dm_id, message, time_sent):
    """
    Sends a message in a dm at a specified time.
    
    Send a message from the authorised user to the dm specified by dm_id. 
    Note: Each message should have its own unique ID, i.e. no messages should share 
    an ID with another message, even if that other message is in a different dm.

    Args:
        token: The generated token of user sending message.
        dm_id: The integer id of the dm the user is
        sending the message in.
        message: The string of the message the user wants to send.
        time_sent: time for the message to be sent

    Returns:
        {'message_id' : message_id}

    Raises:
        Input Error: - The dm id does not exist
                     - Length of message not valid
                     - Time sent is a time in the past

        Access Error: - The token does not exist
                      - The token is not part of the dm.
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
    user_id = get_u_id(token)
    now = datetime.timestamp(datetime.now())

    dm_exists = False
    user_in_dm = False
    message_len_valid = (len(message) >= 1 and len(message) <= 1000)
    time_valid = (now < time_sent)

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
        raise AccessError("User isn't part of the channel")

    if not message_len_valid:
        raise InputError("Length of message is not valid")

    if not time_valid:
        raise InputError("Time for the message to be sent is in the past")

    # creating message_id
    msgs = data_store.get_data()['msgs']
    message_id = len(msgs) + 1

    # updating msgs
    msgs.append(message_id)

    def job():
        message_data = {
            'message_id' : message_id,
            'u_id' : user_id,
            'message' : message,
            'time_created' : int(time_sent),
            'reacts' : [],
            'is_pinned' : False
        }

        # adding message to dm_data
        for dm in dm_data:
            if dm['dm_id'] == dm_id:
                dm['messages'].append(message_data)

        update_workspace_stats('messages_exist', True)
        update_user_stats(user_id, 'messages_sent', True)
        update_permanent_storage()

    # delaying the message
    delay = int(time_sent) - int(now)
    t = threading.Timer(delay, job)
    t.start()

    update_permanent_storage()
    return {'message_id' : message_id}