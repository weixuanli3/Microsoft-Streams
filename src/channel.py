'''Conatins functions to invite to channel, joins channel, return channel messages and return channel details'''
import copy
from src.config import url
from src.data_store import data_store, update_permanent_storage, get_u_id
from src.user import update_user_stats
from src.error import InputError
from src.error import AccessError
from src.notifications import helper_added_add_notif

# Invite a user to a channel that the current user is in
def channel_invite_v1(token, channel_id, u_id):
    """
    Invites a user into the a channel that the current user is in.

    Joins the specified user to the specified channel that
    the auth_user is a part of.

    Args:
        token: The generated token of user inviting the other user to the channel.
        channel_id: The integer id of the channel that auth_user wants to invite
        the other user to.
        u_id: The integer id of the user being invited to the channel.

    Returns:
        An empty dictionary.

    Raises:
        Input Error: - The channel id does not exist
                     - u_id already in the channel
                     - u_id does not exist

        Access Error: - The token does not exist
                      - The token is not part of the channel.
    """


    channel_data = data_store.get_data()['channels']
    user_data = data_store.get_data()['users']

    
    valid_token = False
    for user in user_data:
        if token in user['token']:
            valid_token = True

    if not valid_token:
        raise AccessError("Invalid Token")
    
    auth_user_id = get_u_id(token)

    # check if the auth user exists and u_id exists
    # auth_user_exists = False
    user_valid = False
    for user in user_data:
        # if auth_user_id == user['id']:
        #     auth_user_exists = True
        if u_id == user['id']:
            user_valid = True

    # if not auth_user_exists:
    #     raise AccessError("User doesn't exist")

    if not user_valid:
        raise InputError("user id does not refer to a valid user")


    channel_exists = False
    auth_user_in_channel = False
    user_valid_member = True
    # auth_user_valid = False

    for channel in channel_data:
        # check if the channel exists and if the auth_user is in the channel
        if channel_id == channel['chan_id']:
            channel_exists = True
            curr_channel = channel
            if auth_user_id in channel['users_id']:
                auth_user_in_channel = True
        # check if the u_id refers to a user not aready in the channel
        if u_id in channel['users_id'] and channel_id == channel['chan_id']:
            user_valid_member = False
        # check if auth_user refers to a user not in channel
        # if auth_user_id in channel['users_id']:
        #     auth_user_valid = True

    if not channel_exists:
        raise InputError("Channel ID not valid")

    if not auth_user_in_channel:
        raise AccessError("User isn't part of the channel")

    if not user_valid_member:
        raise InputError("User is already a member of the channel")

    # if not auth_user_valid:
    #     raise AccessError("Auth user id does not refer to a valid user")

    # Add user_id to the channel
    curr_channel['users_id'].append(u_id)

    # Add channel_id to the user
    for user in user_data:
        if (user['id']) == (u_id):
            user['channels'].append(channel_id)
            
    helper_added_add_notif(token, curr_channel, -1, u_id, None)
    update_user_stats(u_id, "channels_joined", True)
    update_permanent_storage()
    return {}

# Returns a dictionary with the details of the specified channel
# if the user is part of said channel
def channel_details_v1(token, channel_id):
    """
    Returns the details of the specified channel.

    Accesses the data within the specified channel and returns a
    dictionary with said details.

    Args:
        token: The integer id of user displaying the channel details.
        channel_id: The integer id of the channel that the user wants to get
        the details of.

    Returns:
        'name' : '',
        'public_status' : True,
        'owner_members' : [],
        'all_members' : [],

        and the owner_members and all_memebers are lists with dictionaries:
            'u_id': user['id'],
            'email': user['emails'],
            'name_first': user['names'],
            'name_last': user['name_lasts'],
            'handle_str': user['handle']

    Raises:
        Input Error: - The channel id does not exist

        Access Error: - The token does not exist
                      - The token is not part of the channel.

    """

    user_data = data_store.get_data()['users']
    
    # Check if the user exists and token is valid
    valid_token = False
    for user in user_data:
        if token in user['token']:
            valid_token = True

    if not valid_token:
        raise AccessError("Invalid Token")

    auth_user_id = get_u_id(token)

    return_dictionary = {
        'name': '',
        'is_public': True,
        'owner_members': [],
        'all_members': [],
    }
    
    owner_ids = []
    member_ids = []

    # Check if the channel exists and if the auth_user is in the channel
    channel_data = data_store.get_data()['channels']
    channel_exists = False
    auth_user_in_channel = False

    for channel in channel_data:
        if channel_id == channel['chan_id']:
            channel_exists = True
            return_dictionary['name'] = channel['name']
            return_dictionary['is_public'] = channel['is_public']
            member_ids = channel['users_id']
            owner_ids = channel['owner_id']
            if auth_user_id in channel['users_id']:
                auth_user_in_channel = True

    if not channel_exists:
        raise InputError("Channel ID not valid")

    if not auth_user_in_channel:
        raise AccessError("User isn't part of the channel")

    # Add the owner_ids and member_ids to the return dictionary
    for user in user_data:
        if user['id'] in owner_ids:
            # user_exists = True
            return_dictionary['owner_members'].append({
            'u_id': user['id'],
            'email': user['emails'],
            'name_first': user['names'],
            'name_last': user['name_lasts'],
            'handle_str': user['handle'],
            'profile_img_url': url + 'imgurl/' + user['profile_img_name']
        })
        if user['id'] in member_ids:
            return_dictionary['all_members'].append({
            'u_id': user['id'],
            'email': user['emails'],
            'name_first': user['names'],
            'name_last': user['name_lasts'],
            'handle_str': user['handle'],
            'profile_img_url': url + 'imgurl/' + user['profile_img_name']
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
def channel_messages_v1(token, channel_id, start):
    """
    Returns the messages sent in the specified channel.

    Accesses the data within the specified channel and returns a
    dictionary with the details of a range of message. ('start' argument
    + 50 messages). If the start argument value passed in is greater than
    total messages sent in the channel minus 50 it displays the messages
    from the start value up until the most first message in the channel sent.

    Args:
        token: The generated token of user displaying the channel messaages.
        channel_id: The integer id of the channel that the user wants to get
        the message details of.
        start: The start index of the messages being displayed, with index 0 is the
        most recent message in the channel.

    Returns:
        A dictionary with:
                {
                    'messages': [
                        {
                            'message_id': 1,
                            'u_id': 1,
                            'message': 'Hello world',
                            'reacts' : [{'user_id' : 1, 'react_id' : 1}]
                            'time_created': 1582426789,
                        }
                    ],
                    'start': 0,
                    'end': 50,
                }

    Raises:
        Input Error: - The channel id does not exist.
                     - start is greater than the total number of messages in the channel.
                     - start can't be negative

        Access Error: - The token does not exist.
                      - The token is not part of the channel.
    """


    
    user_data = data_store.get_data()['users']
    
    valid_token = False
    for user in user_data:
        if token in user['token']:
            valid_token = True

    if not valid_token:
        raise AccessError("Invalid Token")
    

    return_dictionary = {
        'messages': [],
    }
    
    auth_user_id = get_u_id(token)

    # check if the user exists
    user_data = data_store.get_data()['users']
    # user_exists = False
    # for user in user_data:
    #     if auth_user_id == user['id']:
    #         user_exists = True

    # if not user_exists:
        # raise AccessError("User doesn't exist")

    #check if the channel exists and if the auth_user is in the channel
    channel_data = data_store.get_data()['channels']
    channel_exists = False
    auth_user_in_channel = False

    for channel in channel_data:
        if channel_id == channel['chan_id']:
            channel_exists = True
            curr_channel = channel
            if auth_user_id in channel['users_id']:
                auth_user_in_channel = True

    if not channel_exists:
        raise InputError("Channel doesn't exist")

    if not auth_user_in_channel:
        raise AccessError("User isn't part of the channel")

    '''
    messages is a list of strings, everytime a new message is sent, .append the
    string to messages. When function is called, call messages.reverse() so that most
    recent message has index of 0, specified by the requirements. 
    '''

    channel_data = data_store.get_data()['channels']

    msg = []

    # Prevents following changes to messages from affecting out database
    msg = copy.deepcopy(curr_channel['messages'])

    msg.reverse() # Reversed so that newest message has index of 0
    # print(msg)
    if start < 0:
        raise InputError("Start cannot be negative")
    # elif not msg:
    #     if start != 0:
    #         raise InputError("Start is greater than the total number of messages in the channel")
    elif start > len(msg) - 1 and start != 0:
        raise InputError("Start is greater than the total number of messages in the channel")

    # If there are e.g. 50 messages and start = 30, can only return 20, end = -1
    if len(msg) < (start + 50):
        return_messages = msg[start:]
        end = -1
    else: # If there are e.g. 100 messages and start = 30, returns 30 up to 80, end = 80
        return_messages = msg[start:start + 50]
        end = start + 50

    return_dictionary['messages'] = return_messages
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
    #             'reacts' : [{'user_id' : 1, 'react_id' : 1}]
    #             'is_pinned' : False
    #         }
    #     ],
    #     'start': 0,
    #     'end': 50,
    # }

# Add a user to a channel
def channel_join_v1(token, channel_id):
    """
    This funciton makes a specified user a mamber of a specific channel

    Will add the user to the channel's 'user_ids' key's list and the channels
    to the user's 'channels' key's list.

    Args:
        token: The generated token of user joining the channel.
        channel_id: The integer id of the channel that the user wants to join.

    Returns:
        An empty dictionary.

    Raises:
        Input Error: - the channel id inputted does not exist
                     - the token is already in the channel

        Access Error: - The token does not exist
                      - the token is not a global owner and tries to join a private channel

    """
    
    user_data = data_store.get_data()['users']
    
    # check if the user and token exists
    user_data = data_store.get_data()['users']

    valid_token = False
    for user in user_data:
        if token in user['token']:
            valid_token = True

    if not valid_token:
        raise AccessError("Invalid Token")
    
     # turn token into user 
    auth_user_id = get_u_id(token)
    
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
            curr_channel = channel

            # Check if the user is aready in the channel
            if auth_user_id in channel['users_id']:
                raise InputError("User already member of channel")

            # Check if the channel is private
            if not channel['is_public'] and not is_global_owner:
                raise AccessError("Channel is not public")

    if not channel_exists:
        raise InputError("Channel doesn't exist")

    # Add user_id to the channel
    curr_channel['users_id'].append(auth_user_id)

    # Add channel_id to the user
    for user in user_data:
        if (user['id']) == (auth_user_id):
            user['channels'].append(channel_id)

    update_user_stats(auth_user_id, "channels_joined", True)
    update_permanent_storage()
    return {}


def channel_leave_v1(token, channel_id):
    """
    The specified user leaves the channel

    Args:
        token: The generated token of user leaving the channel.
        channel_id: The integer id of the channel that the user wants to leave.

    Returns:
        An empty dictionary.

    Raises:
        Input Error: - the channel id inputted does not exist

        Access Error: - The token does not exist
                      - token not part of the channel

    """    
    user_data = data_store.get_data()['users']
    
    valid_token = False
    for user in user_data:
        if token in user['token']:
            valid_token = True

    if not valid_token:
        raise AccessError("Invalid Token")
    
    # turn token into user 
    auth_user_id = get_u_id(token)
    
    #check if the channel exists
    channel_data = data_store.get_data()['channels']
    channel_exists = False
    user_in_channel = False

    for channel in channel_data:
        if channel_id == channel['chan_id']:
            channel_exists = True
            
        # check if the user is aready in the channel
            if auth_user_id in channel['users_id']:
                user_in_channel = True
            
    if not channel_exists:
        raise InputError("Channel doesn't exist")
    
    if not user_in_channel:
        raise AccessError("User not part of the channel")
    
    # remove the channel from the user
    for user in user_data:
        if user['id'] == auth_user_id:
            user['channels'].remove(channel_id)

    # remove the user from the channel
    channel_data[channel_id - 1]['users_id'].remove(auth_user_id)
    
    if auth_user_id in channel_data[channel_id - 1]['owner_id']:
        channel_data[channel_id - 1]['owner_id'].remove(auth_user_id)

    update_user_stats(auth_user_id, "channels_joined", False)
    update_permanent_storage()
    
    return {}

def channel_add_owner_v1(token, channel_id, u_id):
    """
    Adds a user already in the channel as an owner



    Args:
        token: The generated token of the user calling the function
        channel_id: The integer id of the channel that the user is being made owner in.
        u_id: The integer id of the user being made the owner.

    Returns:
        An empty dictionary.

    Raises:
        Input Error: - The channel id does not exist
                     - u_id owner.
                     - u_id does not exist.
                     - The u_id is not part of the channel.

        Access Error:
                      - The token is not part of the channel.
                      - Invalid token.
                      - token doesn't have permisions to add owner.
                      
    """ 
    channel_data = data_store.get_data()['channels']
    user_data = data_store.get_data()['users']
    global_data = data_store.get_data()['global_owners']
    user_data = data_store.get_data()['users']
    valid_token = False
    for user in user_data:
        if token in user['token']:
            valid_token = True

    if not valid_token:
        raise AccessError("Invalid Token")

    # Check if the channel exists
    channel_data = data_store.get_data()['channels']
    channel_exists = False
    for channel in channel_data:
        if channel_id == channel['chan_id']:
            channel_exists = True
            curr_channel = channel
    
    if not channel_exists:
        raise InputError("Channel ID not valid")

    # Check the permission of the token
    global_data = data_store.get_data()['global_owners']
    token_in_channel = get_u_id(token) in curr_channel['users_id']
    is_global_owner = get_u_id(token) in global_data
    is_channel_owner = get_u_id(token) in curr_channel['owner_id']
    token_perm_valid = (token_in_channel and is_global_owner) or is_channel_owner
    if not token_perm_valid:
        raise AccessError("User does not have owner permissions in the channel")

    # Check if the u_id is valid
    valid_user = False
    for user in user_data:
        if u_id == user['id']:
            valid_user = True
        
    if not valid_user:
        raise InputError("u_id does not refer to a valid user")

    # Check if the u_id refers to someone in the channel
    user_in_channel = u_id in curr_channel['users_id']
    if not user_in_channel:
        raise InputError("u_id isn't part of the channel")
    
    # Check if the user is already an owner of the channel
    if u_id in curr_channel['owner_id']:
        raise InputError("User is already an owner in the channel")

    # add u_id as channel owner
    curr_channel['owner_id'].append(u_id)

    update_permanent_storage()
            
    return {}
    #Return type {}
    
def channel_remove_owner_v1(token, channel_id, u_id):
    """
    Removes a user from the owner status in the channel



    Args:
        token: The generated token of the user calling the function
        channel_id: The integer id of the channel that the user is being removed owner in.
        u_id: The integer id of the user being removed as owner.

    Returns:
        An empty dictionary.

    Raises:
        Input Error: - The channel id does not exist
                     - u_id isn't owner.
                     - u_id does not exist.
                     - u_id only owner of the channel.

        Access Error:
                      - The token is not part of the channel.
                      - Invalid token.
                      - token doesn't have permisions to add owner.
                      - The u_id is not part of the channel
                      
    """    
    channel_data = data_store.get_data()['channels']
    user_data = data_store.get_data()['users']
    global_data = data_store.get_data()['global_owners']
    user_data = data_store.get_data()['users']
    valid_token = False
    for user in user_data:
        if token in user['token']:
            valid_token = True

    if not valid_token:
        raise AccessError("Invalid Token")

    # Check if the channel exists
    channel_data = data_store.get_data()['channels']
    channel_exists = False
    for channel in channel_data:
        if channel_id == channel['chan_id']:
            channel_exists = True
            curr_channel = channel
    
    if not channel_exists:
        raise InputError("Channel ID not valid")

    # Check the permission of the token
    global_data = data_store.get_data()['global_owners']
    token_in_channel = get_u_id(token) in curr_channel['users_id']
    is_global_owner = get_u_id(token) in global_data
    is_channel_owner = get_u_id(token) in curr_channel['owner_id']
    token_perm_valid = (token_in_channel and is_global_owner) or is_channel_owner
    if not token_perm_valid:
        raise AccessError("User does not have owner permissions in the channel")

    # Check if the u_id is valid
    valid_user = False
    for user in user_data:
        if u_id == user['id']:
            valid_user = True
        
    if not valid_user:
        raise InputError("u_id does not refer to a valid user")
    
    # Check if the user is not an owner of the channel
    user_is_owner = u_id in curr_channel['owner_id']
    if not user_is_owner:
        raise InputError("u_id refers to a user who is not an owner of the channel")

    # Check if the user is the only owner of the channel
    if len(curr_channel['owner_id']) == 1:
        raise InputError("Cannot remove the only channel owner")

    # Remove u_id as channel owner
    curr_channel['owner_id'].remove(u_id)

    update_permanent_storage()
            
    return {}
