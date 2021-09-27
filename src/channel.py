from src.data_store import data_store
from src.error import InputError
from src.error import AccessError

def channel_invite_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_details_v1(auth_user_id, channel_id):
        # check if the user exists 
        # MAYBE NOT NECESSARY!!!!!
    '''
    user_data = data_store.get_data()['users']
    user_exists = False
    for user in user_data:
        if auth_user_id == {user['id']}:
            user_exists = True
            
    if not user_exists:
        raise InputError("User doesn't exist")
    
    '''
    
    Return_Dictionary = {
        'channel_name' : '',
        'public_status' : True,
        'owner_members' : [],
        'all_members' : [],
    }
    
    owner_ids = []
    member_ids = []
    
    #check if the channel exists
    channel_data = data_store.get_data()['channels']
    channel_exists = False
    
    for channel in channel_data:
        if channel_id == {channel['chan_id']}:
            channel_exists = True
            Return_Dictionary['channel_name'] = channel['name']
            Return_Dictionary['public_status'] = channel['is_public']
            member_ids = channel['users_id']
            owner_ids = channel['owner_id']
    
    if not channel_exists:
        raise InputError("Channel ID not valid")
    
    user_valid_member = False
    
    # check if the user is aready in the channel
    for channel in channel_data:
        if auth_user_id == {channel['users_id']}:
            user_valid_member = True
    
    if not user_valid_member:
        raise AccessError("User not a member of the channel")
    
    # Add the owener_ids and member_ids to the return dictionary
    # NOT SURE IF THIS IS THE CORRECT SYNTAX TO ADD TO DICTIONARIES 
    # also shiocking time complexity if that matters at all hopefully not though
    user_data = data_store.get_data()['users']
    user_exists = False
    for user in user_data:
        for id in owner_ids:
            if id == {user['id']}:
                Return_Dictionary['owner_members'].append(user)
        for id1 in user_data:
            if id1 == {user['id']}:
                Return_Dictionary['all_members'].append(user)
                
    
    return Return_Dictionary
    
    '''  
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
    '''

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
            raise InputError("User already member of channel")
    
    
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
