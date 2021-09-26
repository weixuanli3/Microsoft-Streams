from src.data_store import data_store
from src.error import InputError

def channels_list_v1(auth_user_id):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }

def channels_listall_v1(auth_user_id):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }

def channels_create_v1(auth_user_id, name, is_public):
    user_data = data_store.get_data()['users']
    user_exists = False
    for user in user_data:
        if auth_user_id == {user['id']}:
            user_exists = True
            if len(name) < 1 or len(name) > 20:
                raise InputError("Invalid channel name")
            user['channels'].add(name)
    
    if not user_exists:
        raise InputError("User doesn't exist")
    
    channel_data = data_store.get_data()['channels']
    for channel in channel_data:
        if name == channel['name']:
            raise InputError("Channel name already exists")
    new_channel_id = len(channel_data) + 1
    channel_data.append({
        'chan_id': new_channel_id,
        'name': name,
        'owner': name,
        'users': {auth_user_id},
        'public': is_public
    })
    return {
        'channel_id': new_channel_id,
    }
