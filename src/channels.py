from src.data_store import data_store
from src.error import InputError

def channels_list_v1(auth_user_id):
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
    for channels in channel_data:
        if channels['chan_id'] in channel_ids and channels['is_public']:
            new_chan = {
                'channel_id': channels['chan_id'],
                'name': channels['name']
            }
            if 'channels' in channel_dict:
                channel_dict['channels'].append(new_chan)
            else:
                channel_dict['channels'] = new_chan

    return channel_dict

def channels_listall_v1(auth_user_id):
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
    for channels in channel_data:
        if channels['chan_id'] in channel_ids:
            new_chan = {
                'channel_id': channels['chan_id'],
                'name': channels['name']
            }
            if 'channels' in channel_dict:
                channel_dict['channels'].append(new_chan)
            else:
                channel_dict['channels'] = new_chan

    return channel_dict

def channels_create_v1(auth_user_id, name, is_public):
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
    for channel in channel_data:
        if name == channel['name']:
            raise InputError("Channel name already exists")
    new_channel_id = len(channel_data) + 1

    curr_user['channels'].append(new_channel_id)

    channel_data.append({
        'chan_id': new_channel_id,
        'name': name,
        'owner_id': auth_user_id,
        'users_id': {auth_user_id},
        'is_public': is_public
    })
    return {
        'channel_id': new_channel_id,
    }
