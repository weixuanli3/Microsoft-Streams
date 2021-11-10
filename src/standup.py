'''Contains all functions related to standups'''
from src.data_store import data_store, update_permanent_storage, get_u_id
from src.user import update_workspace_stats, update_user_stats
from src.error import InputError, AccessError
from datetime import datetime
import datetime as dt
from datetime import timezone
import threading
import time

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
    
    curr_time = dt.datetime.timestamp(dt.datetime.now())
    print(curr_channel['standup']['is_active'])
    if not curr_channel['standup']['is_active']:
        curr_channel['standup']['finish_time'] = dt.datetime.timestamp(dt.datetime.now() + dt.timedelta(seconds=length))
        curr_channel['standup']['start_user'] = user_id
        curr_channel['standup']['is_active'] = True
        print(curr_channel['standup']['is_active'])

        # creating message_id
        msgs = data_store.get_data()['msgs']
        message_id = len(msgs) + 1

        # updating msgs
        msgs.append(message_id)

        def job(curr_channel, curr_time):
            print("meow1")
            message_data = {
                'message_id' : message_id,
                'u_id' : user_id,
                'message' : curr_channel['standup']['messages'], #curr_channel['standup']['messages']
                'time_created' : int(curr_time),
                'reacts' : [],
                'is_pinned' : False
            }

            curr_channel['standup']['is_active'] = False
            curr_channel['messages'].append(message_data)

            # # adding message to channel_data
            # for channel in channel_data:
            #     if channel['chan_id'] == channel_id:
            #         channel['messages'].append(message_data)

            update_workspace_stats('messages_exist', True)
            update_user_stats(user_id, 'messages_sent', True)

        # delaying the message
        # delay = length
        print(length)
        t = threading.Timer(length, job, args=(curr_channel, curr_time))
        t.start()

        update_permanent_storage()

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
    print(dt.datetime.timestamp(dt.datetime.now()))
    if curr_channel['standup']['is_active']:
        is_active = True
        time_finish = curr_channel['standup']['finish_time']
    else:
        # if curr_channel['standup']['is_active']:
        #     # SEND MESSAGES
        #     message_sendlater_req(to/ken, curr_channel['chan_id'], 
        #                           """curr_channel['standup']['messages']""", dt.datetime.timestamp(dt.datetime.now())
        #     pass
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
    print(curr_channel['standup']['is_active'])
    print(dt.datetime.timestamp(dt.datetime.now()))
    if curr_channel['standup']['is_active']:
        user_data = data_store.get_data()['users']
        standup_active = True
        print("woof1")
        for user in user_data:
            print("woof2")
            if user_id == user['id']:
                print("woof3")
                if curr_channel['standup']['messages'] == "":
                    print("woof4")
                    curr_channel['standup']['messages'] + (f"{user['handle']}: {message}")
                else:
                    curr_channel['standup']['messages'] + (f"\n{user['handle']}: {message}")
                print(curr_channel['standup']['messages'])
                break
    
    if not standup_active:
        raise InputError("No standup currently active in channel")
    
    return {}