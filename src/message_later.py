'''Contains all functions related to sending, editing and deleting messages'''
from src.data_store import data_store, update_permanent_storage, get_u_id
from src.error import InputError
from src.error import AccessError
from threading import Timer

def message_sendlater_v1(token, channel_id, message, time_sent):
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
    msgs = data_store.get_data()['msgs']
    user_id = get_u_id(token)

    channel_exists = False
    user_in_channel = False
    message_len_valid = (len(message) >= 1 and len(message) <= 1000)
    time_valid = (datetime.timestamp(datetime.now()) < time_sent)

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

    def job():
        # creating message_id
        message_id = len(msgs) + 1

        message = {
            'message_id' : message_id,
            'u_id' : user_id,
            'message' : message,
            'time_created' : time_sent,
            'reacts' : [],
            'is_pinned' : False
        }

        # adding message to channel_data
        for channel in channel_data:
            if channel['chan_id'] == channel_id:
                channel['messages'].append(message)

        # updating msgs
        msgs.append(message_id)

        update_permanent_storage()

    
    return {'message_id' : message_id}