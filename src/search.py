'''Contains all functions related to sending, editing and deleting messages'''
from src.data_store import data_store, update_permanent_storage, get_u_id
from src.error import InputError, AccessError

def search_v1(token, query_str):
    return {
        "messages": [
            {
                "message_id": 1,
                "u_id": 1,
                "message": "bruh",
                "time_created": "Some timestamp...",
                "reacts": [
                    {
                        "react_id": 1,
                        "u_ids": [1,2,3],
                        "is_this_user_reacted": True
                    }
                ],
                "is_pinned": True
            }
        ]
    }