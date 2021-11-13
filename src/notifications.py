''' Contains functions for getting notifications'''
from src.data_store import data_store, update_permanent_storage, get_u_id
from src.error import InputError, AccessError
from datetime import datetime
import copy

def notifications_get_v1(token):
    
    user_data = data_store.get_data()['users']
    
    #Check if user token is valid
    valid_token = False
    for user in user_data:
        if token in user['token']:
            valid_token = True
            curr_user = user

    if not valid_token:
        raise AccessError("Invalid Token")
    
    notif_list = copy.deepcopy(curr_user['notifications'])
    
    notif_list.reverse()
    
    if len(notif_list) > 20:
        notif_list = notif_list[0:20]
    
    return {'notifications': notif_list}
    
    # return {
    #     "notifications": [
    #         {
    #             "channel_id": 1,
    #             "dm_id": -1,
    #             "notification_message": "bruh tagged you in bruh: asdfasdf"
    #         }
    #     ]
    # }

def helper_tagged_add_notif(token, message, channel, dm):
    
    user_data = data_store.get_data()['users']
    
    tag_handle = find_handle(get_u_id(token))
    
    # Check channel
    if dm == -1:
        for user in user_data:
            user_handle = find_handle(user['id'])
            if f'@{user_handle}' in message['message']:
                
                #Check length of message
                if len(message['message']) <= 20:
                            notif_msg = message['message'][:]
                else:
                    #If message is more than 20 return first 20
                    notif_msg = message['message'][0:20]
                
                user['notifications'].append({
                    'channel_id': channel['chan_id'],
                    'dm_id': -1,
                    'notification_message': f"{tag_handle} tagged you in {channel['name']}: {notif_msg}",
                })
    
    #Check dm
    if channel == -1:
        for user in user_data:
            user_handle = find_handle(user['id'])
            if f'@{user_handle}' in message['message']:
                
                #Check length of message
                if len(message['message']) <= 20:
                            notif_msg = message['message'][:-1]
                else:
                    #If message is more than 20 return first 20
                    notif_msg = message['message'][0:20]
                
                user['notifications'].append({
                    'channel_id': -1,
                    'dm_id': dm['dm_id'],
                    'notification_message': f"{tag_handle} tagged you in {dm['name']}: {notif_msg}",
                })

    return{}

def helper_added_add_notif(token, channel, dm, u_id, u_ids):
    
    user_data = data_store.get_data()['users']

    tag_handle = find_handle(get_u_id(token))
    
    #Check channel
    if dm == -1:
        for user in user_data:
            if u_id == user['id']:
                user['notifications'].append({
                    'channel_id': channel['chan_id'],
                    'dm_id': -1,
                    'notification_message': f"{tag_handle} added you to {channel['name']}",
                })
            
    #Check dm
    if channel == -1:
        for u_id in u_ids:
            for user in user_data:
                if u_id == user['id']:
                    user['notifications'].append({
                        'channel_id': -1,
                        'dm_id': dm['dm_id'],
                        'notification_message': f"{tag_handle} added you to {dm['name']}",
                    })

def helper_reacted_add_notif(token, message, channel, dm):
    
    user_data = data_store.get_data()['users']

    tag_handle = find_handle(get_u_id(token))
    
    #Check channel
    if dm == -1:
        for user in user_data:
            user_handle = find_handle(user['id'])
            user['notifications'].append({
                'channel_id': channel['chan_id'],
                'dm_id': -1,
                'notification_message': f"{tag_handle} reacted to your message in {channel['name']}",
            })
        
    #Check dm
    if channel == -1:
        for user in user_data:
            user_handle = find_handle(user['id'])
            user['notifications'].append({
                'channel_id': -1,
                'dm_id': dm['dm_id'],
                'notification_message': f"{tag_handle} reacted to your message in {dm['name']}",
            })

def find_handle(u_id):
    
    user_data = data_store.get_data()['users']
    
    for user in user_data:
        if u_id == user['id']:
           return user['handle']