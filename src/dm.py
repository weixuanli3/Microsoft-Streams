'''Contains functions relating to creating, listing, removing DMs'''
from sys import _clear_type_cache
from src.data_store import data_store, get_u_id, update_permanent_storage
from src.error import InputError
from src.error import AccessError

def dm_create_v1(token, u_ids):

    user_data = data_store.get_data()['users']
        
    user_exists = []
    for user in user_data:
        for u_id in u_ids:
            if u_id == user['id']:
                user_exists.append(1)

    if user_exists.count(1) != len(u_ids):
        raise InputError("User doesn't exist")
    
    # for id in user_data_ids:
    #     if id not in user_data_ids:
    #         raise InputError("At least one of the u_ids is invalid")
    
    # all_valid = False
    
    # # check all u_ids are valid
    # for u_id in u_ids:
    #     for user in user_data:
    #         if u_id == user['id']:
    #             all_valid = True
    #         else:
    #             all_valid = False
    # if not all_valid:
    #     raise InputError("At least one of the u_ids is invalid")
    
    # check if token is valid
    valid_token = False
    for user in user_data:
        if token in user['token']:
            valid_token = True

    if not valid_token:
        raise AccessError("Invalid Token")
    
    dm_data = data_store.get_data()['DMs']
    dm_id = len(dm_data) + 1
    
    list_name = []
    list_members = []
    
    # add owner's handle to name list
    for user in user_data:
        if get_u_id(token) == user['id']:
            list_name.append(user['handle'])
            list_members.append({'email': user['emails'],
                        'handle_str': user['handle'],
                        'name_first': user['names'],
                        'name_last': user['name_lasts'],
                        'u_id': user['id']})
    
    # add each user's handle to name list
    for u_id in u_ids:
        for user in user_data:
            if u_id == user['id']:
                list_name.append(user['handle'])
                list_members.append({'email': user['emails'],
                        'handle_str': user['handle'],
                        'name_first': user['names'],
                        'name_last': user['name_lasts'],
                        'u_id': user['id']})
                
    
    # sort handles in alphabetical order
    sorted_name = sorted(list_name)

    dm_name =  ", ".join(sorted_name)
    

    
    new_dm = {
        'dm_id': dm_id,
        'owner': get_u_id(token),
        'name': dm_name,
        'members': list_members,
        'messages': []
    }
    
    dm_data.append(new_dm)
    
    update_permanent_storage()
    
    return {'dm_id': dm_id}
    #Return type {dm_id}

def dm_list_v1(token):
    
    dm_data = data_store.get_data()['DMs']
    user_id = get_u_id(token)
    dms = []
    
    for dm in dm_data:
        for dm_members in dm['members']:    
            if user_id == dm_members['u_id']:
                dms.append(dm)
    
    # for dm in dm_data:
    #     if user_id in dm['members']:
    #         dms.append(dm)
    
    update_permanent_storage()
    
    return {'dms': dms}
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
        # check if user not in dm
        
        
    for dm in DM_data:
        if dm['dm_id'] == dm_id:                 
            if user_id != dm['owner']:
                raise AccessError("The user is not in the origional DM creator")
            else:
                DM_data.remove(dm)

    # Dms[dm_id][members].clear()

    # Set members in the DM to an empty list
    # Do I need to remove the owner as well????
 

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
    
    user_in_dm = False
    
    # check if user not in dm
    for dm in DM_data:
        if dm_id == dm['dm_id']:
            for dm_members in dm['members']:    
                if user_id == dm_members['u_id']:
                    user_in_dm = True
                    return_dict = {
                        'name': dm['name'],
                        'members': dm['members']
                    }               


    if not user_in_dm:
        raise AccessError("User is not a member of the DM")
    
    # for dm in DM_data:
    #     if dm['dm_id'] == dm_id:                 
    #         if user_id not in dm['members']:
    #             raise AccessError("The user is not in dm_id")
    #         else:
    #             return_dict = {
    #                 'name': dm['name'],
    #                 'members': dm['members']
    #             }
    
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
            for dm_member in dm['members']:    
                if user_id == dm_member['u_id']:
                    user_in_dm = True
                    dm['members'].remove(dm_member)

    if dm_id_valid and not user_in_dm:
        raise AccessError("User is not a member of the DM")
    
       # check if user not in dm
    for dm in dm_data:
        if dm_id == dm['dm_id']:
            for dm_members in dm['members']:    
                if user_id == dm_members['u_id']:
                    user_in_dm = True
                    # dm.remove(dm_members)

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
    dm_is_valid = False
    
    for dm in dm_data:
        if dm_id == dm['dm_id']:
            dm_is_valid = True
            for dm_members in dm['members']:    
                if user_id == dm_members['u_id']:
                    user_in_dm = True

    if not user_in_dm:
        raise AccessError("User is not a member of the DM")

    if not dm_is_valid:
        raise InputError("dm_id does not refer to a valid DM")
    
    msg = []
    
    for dm in dm_data:
        if dm_id == dm['dm_id']:
            msg = (dm['messages'])
    
    msg.reverse()
    
    if start < 0:
        raise InputError("Start cannot be negative")
    elif not msg:
        raise InputError("Start is greater than the total number of messages in the channel")
    elif start > len(msg) - 1:
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

    update_permanent_storage()

    return return_dictionary
        
    #Return type {messages, start, end}
    
