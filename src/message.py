'''Contains all functions related to sending, editing and deleting messages'''
from src.data_store import data_store
from src.error import InputError
from src.error import AccessError

def message_send_v1(token, channel_id, message):
    pass
    #Return type {message_id}

def message_edit_v1(token, message_id, message):
    pass
    #Return type {}
    
def message_senddm_v1(token, dm_id, message):
    pass
    #return type {message_id}
    
def message_remove_v1(token, dm_id):
    pass
    #return type {}    
