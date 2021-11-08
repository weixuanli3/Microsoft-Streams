'''Contains all functions related to standups'''
import datetime
from src.data_store import data_store, update_permanent_storage, get_u_id
from src.error import InputError, AccessError
from datetime import datetime
from datetime import timezone

def standup_start_v1(token, channel_id, length):
    all_tokens = data_store.get('token')['token']
    token_exists = False

    for user_tokens in all_tokens:
        if token in user_tokens:
            token_exists = True
            
    if not token_exists:
        raise AccessError("Token doesn't exist")
    
    if length < 0:
        raise InputError("Length can't be negative")
    
    channel_data = data_store.get_data()['channels']
    user_id = get_u_id(token)

    channel_exists = False
    user_in_channel = False
    
    for channel in channel_data:
        if channel_id == channel['chan_id']:
            channel_exists = True
            curr_channel = channel
            if user_id in channel['users_id']:
                user_in_channel = True

    if not channel_exists:
        raise InputError("Channel ID not valid")

    if not user_in_channel:
        raise AccessError("User isn't part of the channel")
        
    
    if curr_channel['standup']['finish_time'] < datetime.now().replace(tzinfo=timezone.utc).timestamp():
        print(datetime.now().replace(tzinfo=timezone.utc).timestamp())
        curr_channel['standup']['finish_time'] = datetime.now().replace(tzinfo=timezone.utc).timestamp() + length
        curr_channel['standup']['start_user'] = user_id
    else:
        raise InputError("A standup is already active in this channel")
    
    # message_sendlater_v1(token, channel_id, message, datetime.now().replace(tzinfo=timezone.utc).timestamp() + length)
    return {
        'time_finish': curr_channel['standup']['finish_time']
    }


# MAYBE SEND IT HERE?????
def standup_active_v1(token, channel_id):
    all_tokens = data_store.get('token')['token']
    token_exists = False

    for user_tokens in all_tokens:
        if token in user_tokens:
            token_exists = True
            
    if not token_exists:
        raise AccessError("Token doesn't exist")    
    
    channel_data = data_store.get_data()['channels']
    user_id = get_u_id(token)

    channel_exists = False
    user_in_channel = False
    
    for channel in channel_data:
        if channel_id == channel['chan_id']:
            channel_exists = True
            curr_channel = channel
            if user_id in channel['users_id']:
                user_in_channel = True

    if not channel_exists:
        raise InputError("Channel ID not valid")

    if not user_in_channel:
        raise AccessError("User isn't part of the channel")
    
    is_active = False
    time_finish = None
    print(curr_channel['standup']['finish_time'])
    print(datetime.now().replace(tzinfo=timezone.utc).timestamp())
    if curr_channel['standup']['is_active']:
        is_active = True
        time_finish = curr_channel['standup']['finish_time']
    else:
        if curr_channel['standup']['is_active']:
            # SEND MESSAGES
            message_sendlater_req(token, curr_channel['chan_id'], 
                                  message, datetime.now().replace(tzinfo=timezone.utc).timestamp() + length)
            pass
        pass      
    
    return {is_active, time_finish}

def standup_send_v1(token, channel_id, message):
    all_tokens = data_store.get('token')['token']
    token_exists = False

    for user_tokens in all_tokens:
        if token in user_tokens:
            token_exists = True
            
    if not token_exists:
        raise AccessError("Token doesn't exist")    
    
    channel_data = data_store.get_data()['channels']
    user_id = get_u_id(token)

    channel_exists = False
    user_in_channel = False
    
    for channel in channel_data:
        if channel_id == channel['chan_id']:
            channel_exists = True
            curr_channel = channel
            if user_id in channel['users_id']:
                user_in_channel = True

    if not channel_exists:
        raise InputError("Channel ID not valid")

    if not user_in_channel:
        raise AccessError("User isn't part of the channel")
    
    if len(message) > 1000:
        raise InputError("Message cannot be over 1000 characters")
    #THIS IS AN ASSUMPTION
    # if len(message) < 1:
    #     raise InputError("Message cannot be less then a single character")
    standup_active = False
    if curr_channel['standup']['is_active']:
        user_data = data_store.get_data()['users']
        standup_active = True
        for user in user_data:
            if user_id == user['id']:
                curr_channel['standup']['messages'].append(f"{user['handle']}: {message}")
                break
    
    if not standup_active:
        raise InputError("No standup currently active in channel")
    
    return {}