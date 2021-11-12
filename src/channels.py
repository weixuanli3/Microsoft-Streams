''' Contains the functions to create a new channel and to list pub/priv channels'''
import datetime
from datetime import datetime
from datetime import timezone
import datetime as dt

from src.data_store import data_store, update_permanent_storage
from src.user import update_user_stats, update_workspace_stats
from src.error import InputError
from src.error import AccessError

def channels_list_v1(token):
    '''
    Function will take in an user_id and list all the public channels the user is in

    Arguments:
        token - Used to uniquely identify the user

    Exceptions:
        AccessError - Occurs when:
            Token doesn't exist

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
    # Check if the given user_id exists in the database
    user_exists = False
    for user in user_data:
        if token in user['token']:
            user_exists = True
            channel_ids = user['channels']

    if not user_exists:
        raise AccessError("User doesn't exist")

    channel_data = data_store.get_data()['channels']
    channel_dict = {
        'channels': []
    }
    # Go through the channels, if the user is in the channel, append it
    for channels in channel_data:
        if channels['chan_id'] in channel_ids:
            channel_dict['channels'].append({
                'channel_id': channels['chan_id'],
                'name': channels['name']
            })

    return channel_dict

def channels_listall_v1(token):
    '''
    Function will take in an user_id and list all the public and private channels
    the user is in
    Arguments:
        token (int) - Used to uniquely identify the user

    Exceptions:
        Access - Occurs when:
            Given token does not exist in the system

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
    # Check if the given user_id exists in the database
    user_exists = False
    for user in user_data:
        if token in user['token']:
            user_exists = True

    if not user_exists:
        raise AccessError("User doesn't exist")

    channel_data = data_store.get_data()['channels']
    channel_dict = {
        'channels': []
    }
    # Append all the channels that exist
    for channels in channel_data:
        channel_dict['channels'].append({
            'channel_id': channels['chan_id'],
            'name': channels['name']
        })

    return channel_dict

def channels_create_v1(token, name, is_public):
    '''
    Function will take in an user_id and list all the public and private channels
    the user is in

    Arguments:
        token - Used to uniquely identify the user

    Exceptions:
        InputError - Occurs when:
            Channel name is taken
            Channel name is smaller than 1 character or greater than 20
            Channel name is all spaces
        AcessError - Occurs when:
            Invalid token

    Return Value:
        Returns a dicionary containing the new channel_id
        Example:
        return {
            'channel_id': 4
        }
    '''
    user_data = data_store.get_data()['users']
    # Check if the given token exists in the database
    user_exists = False
    for user in user_data:
        if token in user['token']:
            user_exists = True
            auth_user_id = user['id']
            curr_user = user

    if not user_exists:
        raise AccessError("User doesn't exist")

    if len(name) < 1 or len(name) > 20:
        raise InputError("Invalid channel name")

    # Do not allow names of all white space
    name_is_all_spaces = name == (len(name) * ' ')
    if name_is_all_spaces:
        raise InputError("Name cannot be all white space")

    channel_data = data_store.get_data()['channels']
    # Append the new channel id to the list of channels the user is in
    new_channel_id = len(channel_data) + 1
    curr_user['channels'].append(new_channel_id)
    # Update the channels key in the data dictionary
    channel_data.append({
        'chan_id': new_channel_id,
        'name': name,
        'owner_id': [auth_user_id],
        'users_id': [auth_user_id],
        'is_public': is_public,
        'messages': [],
        'standup': {
            'is_active': False,
            'start_user': -1,
            'finish_time': dt.datetime.timestamp(dt.datetime.now()),
            'messages': ""
        },
    })
    update_workspace_stats("channels_exist", True)
    update_user_stats(auth_user_id, "channels_joined", True)
    update_permanent_storage()
    return {
        'channel_id': new_channel_id,
    }
