def channels_list_v1(auth_user_id):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }

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