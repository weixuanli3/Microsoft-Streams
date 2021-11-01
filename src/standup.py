'''Contains all functions related to standups'''
from src.data_store import data_store, update_permanent_storage, get_u_id
from src.error import InputError, AccessError
from datetime import datetime

def standup_start_v1(token, channel_id, length):
    return {
        "time_finish": "Some timestamp..."
    }

def standup_active_v1(token, channel_id):
    return {
        "is_active": True,
        "time_finish": "Some timestamp..."
    }

def standup_send_v1(token, channel_id, message):
    return {}