from src.data_store import data_store
from src.error import InputError
from src.error import AccessError

def channel_invite_v1(auth_user_id, channel_id, u_id):
    channel_data = data_store.get_data()['channels']
    user_data = data_store.get_data()['users']
    #check if the channel exists
    channel_exists = False

    for channel in channel_data:
        if channel_id == channel['chan_id']:
            channel_exists = True

    if not channel_exists:
        raise InputError("Channel ID not valid")

    # check if the u_id refers to a valid user
    user_valid = False

    for user in user_data:
        if u_id == user['id']:
            user_valid = True

    if not user_valid:
        raise InputError("user id does not refer to a valid user")

    # check if the u_id refers to a user not aready in the channel
    user_valid_member = True

    for channel in channel_data:
        if u_id in channel['users_id']:
            user_valid_member = False

    if not user_valid_member:
        raise InputError("User is already a member of the channel")

    # check if auth_user refers to a user not in channel
    auth_user_valid = False

    for channel in channel_data:
        if auth_user_id in channel['users_id']:
            auth_user_valid = True

    if not auth_user_valid:
        raise AccessError("Auth user id does not refer to a valid user")

    # adding user to channel
    channel_join_v1(u_id, channel_id)

    return {}

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

    return_dictionary = {
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
        if channel_id == channel['chan_id']:
            channel_exists = True
            return_dictionary['channel_name'] = channel['name']
            return_dictionary['public_status'] = channel['is_public']
            member_ids = channel['users_id']
            owner_ids = channel['owner_id']
            

    if not channel_exists:
        raise InputError("Channel ID not valid")

    user_valid_member = False

    # check if the user is aready in the channel
    for channel in channel_data:
        if auth_user_id in channel['users_id']:
            user_valid_member = True

    if not user_valid_member:
        raise AccessError("User not a member of the channel")

    # Add the owener_ids and member_ids to the return dictionary
    # NOT SURE IF THIS IS THE CORRECT SYNTAX TO ADD TO DICTIONARIES
    # also shiocking time complexity if that matters at all hopefully not though
    user_data = data_store.get_data()['users']
    user_exists = False
    
    for user in user_data:
        if owner_ids == user['id']:
            user_exists = True
            return_dictionary['owner_members'].append({
            'u_id': user['id'],
            'email': user['emails'],
            'name_first': user['names'],
            'name_last': user['name_lasts'],
            'handle_str': user['handle'],
        })
        if user['id'] in member_ids:
            return_dictionary['all_members'].append({
            'u_id': user['id'],
            'email': user['emails'],
            'name_first': user['names'],
            'name_last': user['name_lasts'],
            'handle_str': user['handle'],
        })
            
    # for user in user_data:
    #     for id in owner_ids:
    #         print("The type is : ", type(user['id']))
    #         if id == user['id']:
    #             return_dictionary['owner_members'].append(user)
        # for id1 in user_data:
        #     if id1 == user['id']:
        #         return_dictionary['all_members'].append(user)

    
    return return_dictionary

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
    
    return_dictionary = {
        'messages': [],
    }

    # check if the user exists
    user_data = data_store.get_data()['users']
    user_exists = False
    for user in user_data:
        if auth_user_id == user['id']:
            user_exists = True

    if not user_exists:
        raise InputError("User doesn't exist")
    
    #check if the channel exists
    channel_data = data_store.get_data()['channels']
    channel_exists = False

    for channel in channel_data:
        if channel_id == channel['chan_id']:
            channel_exists = True

    if not channel_exists:
        raise InputError("Channel doesn't exist")
    
    # check if the user is aready in the channel
    user_valid_member = False
    
    for channel in channel_data:
        if auth_user_id in channel['users_id']:
            user_valid_member = True

    if not user_valid_member:
        raise AccessError("User not a member of the channel")
    
    '''
    messages is a list of strings, everytime a new message is sent, .append the
    string to messages. When function is called, call messages.reverse() so that most
    recent message has index of 0, specified by the requirements. 
    '''

    channel_data = data_store.get_data()['channels']

    msg = []

    for channel in channel_data:
        if channel_id == channel['chan_id']:
            msg.append(channel['messages'])
    
    msg = msg.reverse() # Reversed so that newest message has index of 0
    
    if not msg:
        if start != 0:
            raise InputError("Start is greater than the total number of messages in the channel") 
    elif start > len(msg) - 1:
        raise InputError("Start is greater than the total number of messages in the channel") 
    
    if len(msg) < (start + 50): # If there are e.g. 50 messages and start = 30, can only return 20, end = -1
        return_messages = msg[start:-1]
        end = -1
    else: # If there are e.g. 100 messages and start = 30, returns 30 up to 80, end = 80
        return_messages = msg[start:start + 50]
        end = start + 50
    
    return_dictionary['messages'].append(return_messages)
    return_dictionary['start'] = start
    return_dictionary['end'] = end
    
    return return_dictionary
    # {
    #     'messages': [
    #         {
    #             'message_id': 1,
    #             'u_id': 1,
    #             'message': 'Hello world',
    #             'time_created': 1582426789,
    #         }
    #     ],
    #     'start': 0,
    #     'end': 50,
    # }

def channel_join_v1(auth_user_id, channel_id):
    # The more efficient way would be to loop through the channels and users once then
    # if the channels and user exists remember what index they were at to access them directly
    # later, however I currently do not know how to access parts of the dictionary directly

    # check if the user exists
    user_data = data_store.get_data()['users']
    user_exists = False
    for user in user_data:
        if auth_user_id == user['id']:
            user_exists = True

    if not user_exists:
        raise InputError("User doesn't exist")

    #check if the channel exists
    channel_data = data_store.get_data()['channels']
    channel_exists = False

    for channel in channel_data:
        if channel_id == channel['chan_id']:
            channel_exists = True

    if not channel_exists:
        raise InputError("Channel doesn't exist")

    # check if the channel is private
    # IMPORTANT still need to check if the user is a global owner
    # but I do not think that global ownership is implemented in iteration 1
    for channel in channel_data:
        if (channel['chan_id']) == (channel_id):
            if not channel['is_public']:
                raise AccessError("Channel is not public")

    # check if the user is aready in the channel
    for channel in channel_data:
        if auth_user_id in channel['users_id'] and channel_id == channel['chan_id']:
            raise InputError("User already member of channel")

    # Add user_id to the channel
    for channel in channel_data:
        if (channel['chan_id']) == (channel_id):
            channel['users_id'].append(auth_user_id)

    # Add channel_id to the user
    for user in user_data:
        if (user['id']) == (auth_user_id):
            user['channels'].append(channel_id)

    return {}
