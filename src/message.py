'''Contains all functions related to sending, editing and deleting messages'''
from src.data_store import data_store, get_u_id, update_permanent_storage
from src.error import InputError
from src.error import AccessError
from datetime import datetime

def message_send_v1(token, channel_id, message):
    channel_data = data_store.get_data()['channels']
    user_id = get_u_id(token)

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

    # checking if the length of message is valid
    if not (len(message) >= 1 and len(message) <= 1000):
        raise InputError("Length of message is not valid")

    # creating message_id and timestamp
    message_id = 1
    time = datetime.now()
    timestamp = int(datetime.timestamp(time))

    message = {'message_id' : message_id, 'u_id' : user_id, 'message' : message, 'time_created' : timestamp}

    # adding message to channel_data
    for channel in channel_data:
        if channel['chan_id'] == channel_id:
            channel['messages'].append(message)

    update_permanent_storage()

    return message_id

def message_edit_v1(token, message_id, message):
    
    return {}
    
def message_senddm_v1(token, dm_id, message):
    
    return message_id
    
def message_remove_v1(token, dm_id):
    
    return {}    
