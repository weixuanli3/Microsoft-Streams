'''Contains functions relating to creating, listing, removing DMs'''
import copy
from sys import _clear_type_cache
from src.config import url
from src.data_store import data_store, get_u_id, update_permanent_storage
from src.user import update_workspace_stats, update_user_stats
from src.error import InputError
from src.error import AccessError
from src.notifications import helper_added_add_notif, helper_reacted_add_notif, helper_tagged_add_notif

def dm_create_v1(token, u_ids):
    """
    Creates a dm chat.
    
    Creates a dm chat with the specified users and the creator who
    becomes the owner.

    Args:
        token: The generated token of user creating the dm.
        u_ids: The integer ids of the users being added to the created dm.

    Returns:
        An empty dictionary.

    Raises:
        Input Error: - one of the inputted u_ids does not exist

        Access Error: - The token does not exist

    """ 
    user_data = data_store.get_data()['users']

    valid_token = False
    for user in user_data:
        if token in user['token']:
            valid_token = True
    if not valid_token:
        raise AccessError("Invalid Token")
        
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
                        'u_id': user['id'],
                        'profile_img_url': url + 'imgurl/' + user['profile_img_name']})
    
    # add each user's handle to name list
    for u_id in u_ids:
        for user in user_data:
            if u_id == user['id']:
                list_name.append(user['handle'])
                list_members.append({'email': user['emails'],
                        'handle_str': user['handle'],
                        'name_first': user['names'],
                        'name_last': user['name_lasts'],
                        'u_id': user['id'],
                        'profile_img_url': url + 'imgurl/' + user['profile_img_name']})
                
    
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
    
    helper_added_add_notif(token, -1, new_dm, None, u_ids)
    update_workspace_stats("dms_exist", True)
    update_user_stats(get_u_id(token), "dms_joined", True)
    update_permanent_storage()
    
    return {'dm_id': dm_id}
    #Return type {dm_id}

def dm_list_v1(token):
    """
    Lists all the dms a user is part of.

    Args:
        token: The generated token of user.

    Returns:
        List of dms
        [{
                    'dm_id': dm['dm_id'],
                    'name': dm['name']
                },
        ]

    Raises:
        Access Error: - The token does not exist

    """ 
    user_data = data_store.get_data()['users']
    
    valid_token = False
    for user in user_data:
        if token in user['token']:
            valid_token = True

    if not valid_token:
        raise AccessError("Invalid Token")
    
    dm_data = data_store.get_data()['DMs']
    user_id = get_u_id(token)
    dms = []
    
    for dm in dm_data:
        for dm_members in dm['members']:    
            if user_id == dm_members['u_id']:
                dms.append({
                    'dm_id': dm['dm_id'],
                    'name': dm['name']
                })
    
    # for dm in dm_data:
    #     if user_id in dm['members']:
    #         dms.append(dm)
    
    update_permanent_storage()
    
    return {'dms': dms}
    #Return type {dms}
    
def dm_remove_v1(token, dm_id):
    """
    Remove an existing DM, so all members are no longer in the DM. 
    This can only be done by the original creator of the DM.

    Args:
        token: The generated token of user.
        dm_id: the dm_id of the dm being removed

    Returns:
        An empty dm

    Raises:
        Input Error: - Invalid dm_id
    
        Access Error: - The token does not exist
                      - user not original creator

    """ 
    user_data = data_store.get_data()['users']
    
    valid_token = False
    for user in user_data:
        if token in user['token']:
            valid_token = True

    if not valid_token:
        raise AccessError("Invalid Token")

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
 
    update_workspace_stats("dms_exist", False)
    update_user_stats(user_id, "dms_joined", False)
    update_permanent_storage()
    #Return type {}
    return{}

def dm_details_v1(token, dm_id):
    """
    Given a DM with ID dm_id that the authorised user is a member of, 
    provide basic details about the DM.

    Args:
        token: The generated token of user.
        dm_id: the dm_id of the dm whose details are being returned

    Returns:
        {
            'name': dm['name'],
            'members':  dm['members']
        }

    Raises:
        Input Error: - Invalid dm_id
    
        Access Error: - The token does not exist
                      - user not member of dm

    """
    user_data = data_store.get_data()['users']
    
    valid_token = False
    for user in user_data:
        if token in user['token']:
            valid_token = True

    if not valid_token:
        raise AccessError("Invalid Token")

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
                        'members':  dm['members']
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
    """
    Given a DM ID, the user is removed as a member of this DM. 
    The creator is allowed to leave and the DM will still exist if this happens. 
    This does not update the name of the DM.

    Args:
        token: The generated token of user.
        dm_id: the dm_id of the dm the user is leaving

    Returns:
        An empty dictionary

    Raises:
        Input Error: - Invalid dm_id
    
        Access Error: - The token does not exist
                      - user not member of dm

    """

    user_data = data_store.get_data()['users']
    
    valid_token = False
    for user in user_data:
        if token in user['token']:
            valid_token = True

    if not valid_token:
        raise AccessError("Invalid Token")
    
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
            if user_id == dm['owner']:
                user_in_dm = True
                dm['owner'] = -1

    if dm_id_valid and not user_in_dm:
        raise AccessError("User is not a member of the DM")
    
    #    # check if user not in dm
    for dm in dm_data:
        if dm_id == dm['dm_id']:
            for dm_members in dm['members']:    
                if user_id == dm_members['u_id']:
                    user_in_dm = True
                    # dm.remove(dm_members)

    if not dm_id_valid:
        raise InputError("dm_id does not refer to a valid DM")
    
    update_user_stats(user_id, "dms_joined", False)
    update_permanent_storage()
    
    return {}    
    #Return type {}

def dm_messages_v1(token, dm_id, start):
    """
Given a DM with ID dm_id that the authorised user is a member of, 
return up to 50 messages between index "start" and "start + 50". 
Message with index 0 is the most recent message in the DM. 
This function returns a new index "end" which is the value of "start + 50", or, 
if this function has returned the least recent messages in the DM, returns -1 in 
"end" to indicate there are no more messages to load after this return.

    Args:
        token: The generated token of user.
        dm_id: the dm_id of the dm whose messages are being returned
        start: the value of start of the list of messages being returned

    Returns:
        {
        'messages': [{'message_id' : message_id, 
                    'u_id' : user_id, 
                    'message' : message, 
                    'time_created' : timestamp
            }],
    }

    Raises:
        Input Error: - Invalid dm_id
    
        Access Error: - The token does not exist
                      - user not member of dm

    """    

    user_data = data_store.get_data()['users']
    
    valid_token = False
    for user in user_data:
        if token in user['token']:
            valid_token = True

    if not valid_token:
        raise AccessError("Invalid Token")
    
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

    if not user_in_dm and dm_is_valid:
        raise AccessError("User is not a member of the DM")

    if not dm_is_valid:
        raise InputError("dm_id does not refer to a valid DM")
    
    msg = []
    
    for dm in dm_data:
        if dm_id == dm['dm_id']:
            # Prevents the following changes from affecting our database
            msg = copy.deepcopy(dm['messages'])
    
    msg.reverse()
    
    if start < 0:
        raise InputError("Start cannot be negative")
    # elif not msg:
        # raise InputError("Start is greater than the total number of messages in the channel")
    elif start > len(msg):
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
