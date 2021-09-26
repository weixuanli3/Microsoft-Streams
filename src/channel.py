from src.data_store import data_store
from src.error import InputError
from src.error import AccessError

def channel_invite_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_details_v1(auth_user_id, channel_id):
    return {
        'name': 'Hayden',
        'owner_members': [
            {
                'u_id': 1,
                'email': 'example@gmail.com',
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
                'handle_str': 'haydenjacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'email': 'example@gmail.com',
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
                'handle_str': 'haydenjacobs',
            }
        ],
    }

def channel_messages_v1(auth_user_id, channel_id, start):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
    }

def channel_join_v1(auth_user_id, channel_id):
    # The more efficient way would be to loop through the channels and users once then
    # if the channels and user exists remember what index they were at to access them directly later,
    # however I currently do not know how to access parts of the dictionary directly
    
    # check if the user exists
    user_data = data_store.get_data()['users']
    user_exists = False
    for user in user_data:
        if auth_user_id == {user['id']}:
            user_exists = True
    
    if not user_exists:
        raise InputError("User doesn't exist")
    
    #check if the channel exists
    channel_data = data_store.get_data()['channels']
    channel_exists = False
    
    for channel in channel_data:
        if channel_id == {channel['chan_id']}:
            channel_exists = True
    
    if not channel_exists:
        raise InputError("Channel doesn't exist")
    
    # check if the channel is private
    # IMPORTANT still need to check if the user is a global owner
    # but I do not think that global ownership is implemented in iteration 1
    for channel in channel_data:
        if (channel['chan_id']) == (channel_id):
            if not (channel['is_public']):
                raise AccessError("Channel is not public")
            
    # check if the user is aready in the channel
    for channel in channel_data:
        if auth_user_id == {channel['users_id']}:
            channel_exists = True
    
    
    # Add user_id to the channel
    for channel in channel_data:
        if (channel['chan_id']) == (channel_id):
            channel['users_id'].append(auth_user_id) 
            
    # Add channel_id to the user
    for user in user_data:
        if (user['id']) == (auth_user_id):
            user['channels'].append(channel_id) 
    
    return {
    }
