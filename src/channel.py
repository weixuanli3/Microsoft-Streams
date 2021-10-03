from src.data_store import data_store
from src.error import InputError
from src.error import AccessError

# Invite a user to a channel that the current user is in
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
        if u_id in channel['users_id'] and channel_id == channel['chan_id']:
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

    # Add user_id to the channel
    for channel in channel_data:
        if (channel['chan_id']) == (channel_id):
            channel['users_id'].append(u_id)

    # Add channel_id to the user
    for user in user_data:
        if (user['id']) == (u_id):
            user['channels'].append(channel_id)

    return {}

# Returns a dictionary with the details of the specified channel
# if the user is part of said channel
def channel_details_v1(auth_user_id, channel_id):
    """
    This function is used to show the details of a channel the user is in.
    It will raise an input error if the user is not in the channel or the 
    channel does not exist. Assuming no errors are raised the function will
    return a dictionary with:         
    'name' : '',
    'public_status' : True,
    'owner_members' : [],
    'all_members' : [],
    
    and the owner_members and all_memebers are lists with dictionaries: 
            'u_id': user['id'],
            'email': user['emails'],
            'name_first': user['names'],
            'name_last': user['name_lasts'],
            'handle_str': user['handle'],
    """
    
    
    # check of the user exists
    user_data = data_store.get_data()['users']
    user_exists = False
    for user in user_data:
        if auth_user_id == user['id']:
            user_exists = True

    if not user_exists:
        raise AccessError("User doesn't exist")


    return_dictionary = {
        'name' : '',
        'is_public' : True,
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
            return_dictionary['name'] = channel['name']
            return_dictionary['is_public'] = channel['is_public']
            member_ids = channel['users_id']
            owner_ids = channel['owner_id']


    if not channel_exists:
        raise InputError("Channel ID not valid")

    user_valid_member = False

    # check if the user is in the channel
    for channel in channel_data:
        if auth_user_id in channel['users_id']:
            user_valid_member = True

    if not user_valid_member:
        raise AccessError("User not a member of the channel")

    # Add the owner_ids and member_ids to the return dictionary
    user_data = data_store.get_data()['users']

    for user in user_data:
        if user['id'] in owner_ids:
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
# Return 50 messages (or the end of the messages) in a dictionary
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
        raise AccessError("User doesn't exist")

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

    # If there are e.g. 50 messages and start = 30, can only return 20, end = -1
    if len(msg) < (start + 50):
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

# Add a user to a channel
def channel_join_v1(auth_user_id, channel_id):
    """
    This funciton makes a specified user a part of a channel. It will raise
    an input error if the user or channel ids inputted do not exist or
    the user is already in the channel. It wil raise an access error if
    the channel is not a global owner and tries to join a private channel.
    If no errors are raised it will add the user to the channel's 'user_ids'
    key's list and the channels to the user's 'channels' key's list.
    It returns an empty dictionary.
    """

    # check if the user exists
    user_data = data_store.get_data()['users']
    user_exists = False
    for user in user_data:
        if auth_user_id == user['id']:
            user_exists = True

    if not user_exists:
        raise AccessError("User doesn't exist")
    
    #check if the user is a global 
    global_data = data_store.get_data()['global_owners']
    is_global_owner = False
    
    if auth_user_id in global_data:
        is_global_owner = True
    

    #check if the channel exists
    channel_data = data_store.get_data()['channels']
    channel_exists = False

    for channel in channel_data:
        if channel_id == channel['chan_id']:
            channel_exists = True
            
            # check if the user is aready in the channel
            if auth_user_id in channel['users_id']:
                raise InputError("User already member of channel")
            
            #check if the channel is private
            
            if not channel['is_public'] and not is_global_owner:
                raise AccessError("Channel is not public")        

    if not channel_exists:
        raise InputError("Channel doesn't exist")

    # Add user_id to the channel
    for channel in channel_data:
        if (channel['chan_id']) == (channel_id):
            channel['users_id'].append(auth_user_id)

    # Add channel_id to the user
    for user in user_data:
        if (user['id']) == (auth_user_id):
            user['channels'].append(channel_id)

    return {}
