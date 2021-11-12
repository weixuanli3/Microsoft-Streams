'''Contains all functions related to sending, editing and deleting messages'''
from src.data_store import data_store, update_permanent_storage, get_u_id
from src.error import InputError, AccessError

def search_v1(token, query_str):
    
    user_data = data_store.get_data()['users']
    dm_data = data_store.get_data()['DMs']
    channel_data = data_store.get_data()['channels']
    
    valid_token = False
    for user in user_data:
        if token in user['token']:
            valid_token = True

    if not valid_token:
        raise AccessError("Invalid Token")
    
    user_id = get_u_id(token)
    
    query_valid = False
    if 1 <= len(query_str) <= 1000:
        query_valid = True
    
    if not query_valid:
        raise InputError("Length of query is less than 1 or over 1000 characters")
    
    list_messages = {"messages": []}
    
    #Search all user's DMs
    for dm in dm_data:
        for members in dm['members']:
            if user_id == members['u_id']:
                for msg in dm['messages']:
                    if query_str in msg['message']:
                        list_messages['messages'].append(msg)
        
    #Search all user's channels
    for channel in channel_data:
        if user_id in channel['users_id']:
            for msg in channel['messages']:
                if query_str in msg['message']:
                    list_messages['messages'].append(msg)
                    
    return list_messages
    
    # return {
    #     "messages": [
    #         {
    #             "message_id": 1,
    #             "u_id": 1,
    #             "message": "bruh",
    #             "time_created": "Some timestamp...",
    #             "reacts": [
    #                 {
    #                     "react_id": 1,
    #                     "u_ids": [1,2,3],
    #                     "is_this_user_reacted": True
    #                 }
    #             ],
    #             "is_pinned": True
    #         }
    #     ]
    # }