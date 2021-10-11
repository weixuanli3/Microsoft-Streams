'''Contains functions relating to creating, listing, removing DMs'''
from src.data_store import data_store
from src.error import InputError
from src.error import AccessError

def dm_create_v1(token, u_ids):
    pass
    #Return type {dm_id}

def dm_list_v1(token):
    pass
    #Return type {dms}
    
def dm_remove_v1(token, dm_id):
    pass
    #Return type {}

def dm_details_v1(token, dm_id):
    pass
    #Return type {name, members}
    
def dm_leave_v1(token, dm_id):
    pass
    #Return type {}

def dm_messages_v1(token, dm_id, start):
    pass
    #Return type {messages, start, end}
    