''' Contains the functions to create a new channel and to list pub/priv channels'''
from src.data_store import data_store
from src.error import InputError

def channels_list_v1(auth_user_id):
    '''
    Function will take in an user_id and list all the public channels the user is in

    Arguments:
        auth_user_id (int) - Used to uniquely identify the user

    Exceptions:
        InputError - Occurs when:
            Given user_id does not exist in the system

    Return Value:
        Returns {} when user is not a part of any channel
        Returns a dictionary to a list of channels which are smaller dictionaries
        that contains channel_id and name otherwise
        Example:
        return {
            'channels': [
                {
                    'channel_id': 2
                    'name': "Channel 2"
                },
                {
                    'channel_id': 6
                    'name': "Channel Private"
                }
            ]
        }
    '''
    user_data = data_store.get_data()['users']
    user_exists = False
    for user in user_data:
        if auth_user_id == user['id']:
            user_exists = True
            channel_ids = user['channels']

    if not user_exists:
        raise InputError("User doesn't exist")

    channel_data = data_store.get_data()['channels']
    channel_dict = {}
    channel_list = []
    for channels in channel_data:
        if channels['chan_id'] in channel_ids and channels['is_public']:
            new_chan = {
                'channel_id': channels['chan_id'],
                'name': channels['name']
            }
            
            if 'channels' not in channel_dict:
                channel_dict['channels'] = [new_chan]
            else:
                channel_dict['channels'].append(new_chan)

    return channel_dict

def channels_listall_v1(auth_user_id):
    '''
    Function will take in an user_id and list all the public and private channels
    the user is in
    Arguments:
        auth_user_id (int) - Used to uniquely identify the user

    Exceptions:
        InputError - Occurs when:
            Given user_id does not exist in the system

    Return Value:
        Returns {} when user is not a part of any channel
        Returns a dictionary to a list of channels which are smaller dictionaries
        that contains channel_id and name otherwise
        Example:
        return {
            'channels': [
                {
                    'channel_id': 2
                    'name': "Channel 2"
                },
                {
                    'channel_id': 6
                    'name': "Channel Private"
                }
            ]
        }
    '''
    user_data = data_store.get_data()['users']
    user_exists = False
    for user in user_data:
        if auth_user_id == user['id']:
            user_exists = True
            channel_ids = user['channels']

    if not user_exists:
        raise InputError("User doesn't exist")

    channel_data = data_store.get_data()['channels']
    channel_dict = {}
    channel_list = []
    for channels in channel_data:
        if channels['chan_id'] in channel_ids:
            new_chan = {
                'channel_id': channels['chan_id'],
                'name': channels['name']
            }

            if 'channels' not in channel_dict:
                channel_dict['channels'] = [new_chan]
            else:
                channel_dict['channels'].append(new_chan)

    return channel_dict

def channels_create_v1(auth_user_id, name, is_public):
    '''
    Function will take in an user_id and list all the public and private channels \
    the user is in

    Arguments:
        auth_user_id (int) - Used to uniquely identify the user

    Exceptions:
        InputError - Occurs when:
            Given user_id does not exist in the system
            Channel name is taken
            Channel name is smaller than 1 character or greater than 20

    Return Value:
        Returns a dicionary containing the new channel_id
        Example:
        return {
            'channel_id': 4
        }
    '''
    user_data = data_store.get_data()['users']
    user_exists = False
    for user in user_data:
        if auth_user_id == user['id']:
            user_exists = True
            curr_user = user

    if not user_exists:
        raise InputError("User doesn't exist")

    if len(name) < 1 or len(name) > 20:
        raise InputError("Invalid channel name")

    channel_data = data_store.get_data()['channels']

    new_channel_id = len(channel_data) + 1
    curr_user['channels'].append(new_channel_id)

    channel_data.append({
        'chan_id': new_channel_id,
        'name': name,
        'owner_id': auth_user_id,
        'users_id': [auth_user_id],
        'is_public': is_public,
        'messages': [],
    })
    return {
        'channel_id': new_channel_id,
    }
