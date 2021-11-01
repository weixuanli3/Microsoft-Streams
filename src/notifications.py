''' Contains functions for getting notifications'''
from src.data_store import data_store, update_permanent_storage, get_u_id
from src.error import InputError, AccessError
from datetime import datetime

def notifications_get_v1(token):
    return {
        "notifications": [
            {
                "channel_id": 1,
                "dm_id": -1,
                "notification_message": "bruh tagged you in bruh: asdfasdf"
            }
        ]
    }