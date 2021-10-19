'''Contains functions relating to creating, listing, removing DMs'''
from src.data_store import data_store, get_u_id, update_permanent_storage
from src.error import InputError
from src.error import AccessError

def dm_create_v1(token, *u_ids):
    
    user_data = data_store.get_data()['users']
    
    all_valid = False
    
    # check all u_ids are valid
    for u_id in u_ids:
        for user in user_data:
            if u_id == user['id']:
                all_valid = True
            else:
                all_valid = False
    if not all_valid:
        raise InputError("At least one of the u_ids is invalid")
    
    dm_data = data_store.get_data()['DMs']
    dm_id = len(dm_data) + 1
    
    list_name = []
    list_members = []
    
    # add each user's handle to name list
    for u_id in u_ids:
        for user in user_data:
            if u_id == user['id']:
                list_name.append(user['handle'])
                list_members.append(user['id'])
                
    
    # add owner's handle to name list
    for user in user_data:
        if get_u_id(token) == user['id']:
            list_name.append(user['handle'])
            list_members.append(user['id'])
    
    # sort handles in alphabetical order
    sorted_name = sorted(list_name)
    
    dm_name = ""
    
    for member in sorted_name:
        dm_name += member
    
    new_dm = {
        'dm_id': dm_id,
        'owner': get_u_id(token),
        'name': dm_name,
        'members': list_members,
        'messages': []
    }
    
    dm_data.append(new_dm)
    
    update_permanent_storage()
    
    return dm_id
    #Return type {dm_id}

def dm_list_v1(token):
    
    dm_data = data_store.get_data()['DMs']
    user_id = get_u_id(token)
    dms = []
    
    for dm in dm_data:
        if user_id in dm['members']:
            dms.append(dm)
    
    update_permanent_storage()
    
    return dms
    #Return type {dms}
    
def dm_remove_v1(token, dm_id):
    # check if the dm id is not valid
    DM_data = data_store.get_data()['DMs']
    DM_exists = False
    for DM in DM_data:
        if dm_id == DM['dm_id']:
            DM_exists = True
    if not DM_exists:
        raise InputError("Invalid dm_id")
    
    #convert token to ID
    user_id = get_u_id(token)
    
    # check if user not the creator of dm
    if user_id not in DM[dm_id]['owner']:
        raise AccessError("The user is not in the origional DM creator")
    # Dms[dm_id][members].clear()

    # Set members in the DM to an empty list
    # Do I need to remove the owner as well????
    DM[dm_id]['members'] = []

    update_permanent_storage()
    #Return type {}
    return{}

def dm_details_v1(token, dm_id):
    
  # check if the dm id is not valid
    DM_data = data_store.get_data()['DMs']
    DM_exists = False
    for DM in DM_data:
        if dm_id == DM['dm_id']:
            DM_exists = True
    if not DM_exists:
        raise InputError("Invalid dm_id")
    
    #convert token to ID
    user_id = get_u_id(token)
    
    # check if user not in dm
    if user_id not in DM[dm_id]['members']:
        raise AccessError("The user is not in dm_id")
    
    return_dict = {
        'name': DM[dm_id]['name'],
        'members': DM[dm_id]['members']
    }
    
    return return_dict
    # Return type {name, members}
    
def dm_leave_v1(token, dm_id):
        
    dm_data = data_store.get_data()['DMs']
    user_id = get_u_id(token)
    
    # test if user is in dm
    user_in_dm = False
    # test if dm_id is valid
    dm_id_valid = False
    
    for dm in dm_data:
        if dm_id == dm['dm_id']:
            dm_id_valid = True
            if user_id in dm['members']:
                dm['members'].remove(user_id)
                user_in_dm = True

    if not user_in_dm:
        raise AccessError("User is not a member of the DM")

    if not dm_id_valid:
        raise InputError("dm_id does not refer to a valid DM")
    
    update_permanent_storage()
    
    return {}    
    #Return type {}

def dm_messages_v1(token, dm_id, start):
    
    user_id = get_u_id(token)
    dm_data = data_store.get_data()['DMs']
    
    return_dictionary = {
        'messages': [],
    }
    
    # test if user is in dm
    user_in_dm = False
    # test if dm_id is valid
    dm_id_valid = False
    
    for dm in dm_data:
        if dm_id == dm['dm_id']:
            dm_id_valid = True
            if user_id in dm['members']:
                user_in_dm = True

    if not user_in_dm:
        raise AccessError("User is not a member of the DM")

    if not dm_id_valid:
        raise InputError("dm_id does not refer to a valid DM")
    
    msg = []
    
    for dm in dm_data:
        if dm_id == dm['dm_id']:
            msg.append(dm['messages'])
    
    msg = msg.reverse()
    
    if start < 0:
        raise InputError("Start cannot be negative")
    elif not msg:
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

    update_permanent_storage()

    return return_dictionary
        
    #Return type {messages, start, end}
    