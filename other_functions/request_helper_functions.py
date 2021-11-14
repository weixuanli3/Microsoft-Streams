''' This module contains helper functions to send and receive requests from http server'''
from src.config import url
import json
import requests

def auth_login_req(email, password):
    input_data = {
        'email': email,
        'password': password
    }
    return requests.post(f"{url}auth/login/v2", data=json.dumps(input_data)).json()

def auth_register_req(email, password, name_first, name_last):
    input_data = {
        "email": email,
        "password": password,
        "name_first": name_first,
        "name_last": name_last
    }
    return requests.post(f"{url}auth/register/v2", data=json.dumps(input_data)).json()

def auth_logout_req(token):
    input_data = {
        "token": token
    }
    return requests.post(f"{url}auth/logout/v1", data=json.dumps(input_data)).json()

def channels_create_req(token, name, is_public):
    input_data = {
        "token": token,
        "name": name,
        "is_public": is_public
    }
    return requests.post(f"{url}channels/create/v2", data=json.dumps(input_data)).json()

def channels_list_req(token):
    input_data = {
        "token": token
    }
    return requests.get(f"{url}channels/list/v2", params=input_data).json()

def channels_listall_req(token):
    input_data = {
        "token": token
    }
    return requests.get(f"{url}channels/listall/v2", params=input_data).json()

def channel_details_req(token, channel_id):
    input_data = {
        "token": token,
        "channel_id": channel_id
    }
    return requests.get(f"{url}channel/details/v2", params=input_data).json()

def channel_join_req(token, channel_id):
    input_data = {
        "token": token,
        "channel_id": channel_id
    }
    return requests.post(f"{url}channel/join/v2", data=json.dumps(input_data)).json()

def channel_invite_req(token, channel_id, u_id):
    input_data = {
        "token": token,
        "channel_id": channel_id,
        "u_id": u_id
    }
    return requests.post(f"{url}channel/invite/v2", data=json.dumps(input_data)).json()


def channel_messages_req(token, channel_id, start):
    input_data = {
        "token": token,
        "channel_id": channel_id,
        "start": start
    }
    return requests.get(f"{url}channel/messages/v2", params=input_data).json()

def channel_leave_req(token, channel_id):
    input_data = {
        "token": token,
        "channel_id": channel_id,
    }
    return requests.post(f"{url}channel/leave/v1", data=json.dumps(input_data)).json()

def channel_addowner_req(token, channel_id, u_id):
    input_data = {
        "token": token,
        "channel_id": channel_id,
        "u_id": u_id
    }
    return requests.post(f"{url}channel/addowner/v1", data=json.dumps(input_data)).json()

def channel_removeowner_req(token, channel_id, u_id):
    input_data = {
        "token": token,
        "channel_id": channel_id,
        "u_id": u_id
    }
    return requests.post(f"{url}channel/removeowner/v1", data=json.dumps(input_data)).json()

def message_send_req(token, channel_id, message):
    input_data = {
        "token": token,
        "channel_id": channel_id,
        "message": message
    }
    return requests.post(f"{url}message/send/v1", data=json.dumps(input_data)).json()

def message_edit_req(token, message_id, message):
    input_data = {
        "token": token,
        "message_id": message_id,
        "message": message
    }
    return requests.put(f"{url}message/edit/v1", data=json.dumps(input_data)).json()

def message_remove_req(token, message_id):
    input_data = {
        "token": token,
        "message_id": message_id
    }
    return requests.delete(f"{url}message/remove/v1", data=json.dumps(input_data)).json()

def dm_create_req(token, u_ids):
    input_data = {
        "token": token,
        "u_ids": u_ids
    }
    return requests.post(f"{url}dm/create/v1", data=json.dumps(input_data)).json()

def dm_list_req(token):
    input_data = {
        "token": token
    }
    return requests.get(f"{url}dm/list/v1", params=input_data).json()

def dm_remove_req(token, dm_id):
    input_data = {
        "token": token,
        "dm_id": dm_id
    }
    return requests.delete(f"{url}dm/remove/v1", data=json.dumps(input_data)).json()

def dm_details_req(token, dm_id):
    input_data = {
        "token": token,
        "dm_id": dm_id
    }
    return requests.get(f"{url}dm/details/v1", params=input_data).json()

def dm_leave_req(token, dm_id):
    input_data = {
        "token": token,
        "dm_id": dm_id
    }
    return requests.post(f"{url}dm/leave/v1", data=json.dumps(input_data)).json()

def dm_messages_req(token, dm_id, start):
    input_data = {
        "token": token,
        "dm_id": dm_id,
        "start": start
    }
    return requests.get(f"{url}dm/messages/v1", params=input_data).json()

def message_senddm_req(token, dm_id, message):
    input_data = {
        "token": token,
        "dm_id": dm_id,
        "message": message
    }
    return requests.post(f"{url}message/senddm/v1", data=json.dumps(input_data)).json()

def users_all_req(token):
    input_data = {
        "token": token,
    }
    return requests.get(f"{url}users/all/v1", params=input_data).json()

def user_profile_req(token, u_id):
    input_data = {
        "token": token,
        "u_id": u_id
    }
    return requests.get(f"{url}user/profile/v1", params=input_data).json()

def user_profile_setname_req(token, name_first, name_last):
    input_data = {
        "token": token,
        "name_first": name_first,
        "name_last": name_last
    }
    return requests.put(f"{url}user/profile/setname/v1", data=json.dumps(input_data)).json()

def user_profile_setemail_req(token, email):
    input_data = {
        "token": token,
        "email": email
    }
    return requests.put(f"{url}user/profile/setemail/v1", data=json.dumps(input_data)).json()

def user_profile_sethandle_req(token, handle_str):
    input_data = {
        "token": token,
        "handle_str": handle_str
    }
    return requests.put(f"{url}user/profile/sethandle/v1", data=json.dumps(input_data)).json()

def admin_user_remove_req(token, u_id):
    input_data = {
        "token": token,
        "u_id": u_id
    }
    return requests.delete(f"{url}admin/user/remove/v1", data=json.dumps(input_data)).json()

def admin_userpermission_change_req(token, u_id, permission_id):
    input_data = {
        "token": token,
        "u_id": u_id,
        "permission_id": permission_id
    }
    return requests.post(f"{url}admin/userpermission/change/v1", data=json.dumps(input_data)).json()

def clear_req():
    requests.delete(f"{url}clear/v1")

def notifications_get_req(token):
    input_data = {
        "token": token
    }
    return requests.get(f"{url}notifications/get/v1", params=input_data).json()

def search_req(token, query_str):
    input_data = {
        "token": token,
        "query_str": query_str
    }
    return requests.get(f"{url}search/v1", params=input_data).json()

def message_share_req(token, og_message_id, message, channel_id, dm_id):
    input_data = {
        "token": token,
        "og_message_id": og_message_id,
        "message": message,
        "channel_id": channel_id,
        "dm_id": dm_id
    }
    return requests.post(f"{url}message/share/v1", data=json.dumps(input_data)).json()

def message_react_req(token, message_id, react_id):
    input_data = {
        "token": token,
        "message_id": message_id,
        "react_id": react_id
    }
    return requests.post(f"{url}message/react/v1", data=json.dumps(input_data)).json()

def message_unreact_req(token, message_id, react_id):
    input_data = {
        "token": token,
        "message_id": message_id,
        "react_id": react_id
    }
    return requests.post(f"{url}message/unreact/v1", data=json.dumps(input_data)).json()

def message_pin_req(token, message_id):
    input_data = {
        "token": token,
        "message_id": message_id
    }
    return requests.post(f"{url}message/pin/v1", data=json.dumps(input_data)).json()

def message_unpin_req(token, message_id):
    input_data = {
        "token": token,
        "message_id": message_id
    }
    return requests.post(f"{url}message/unpin/v1", data=json.dumps(input_data)).json()

def message_sendlater_req(token, channel_id, message, time_sent):
    input_data = {
        "token": token,
        "channel_id": channel_id,
        "message": message,
        "time_sent": time_sent
    }
    return requests.post(f"{url}message/sendlater/v1", data=json.dumps(input_data)).json()

def message_sendlaterdm_req(token, dm_id, message, time_sent):
    input_data = {
        "token": token,
        "dm_id": dm_id,
        "message": message,
        "time_sent": time_sent
    }
    return requests.post(f"{url}message/sendlaterdm/v1", data=json.dumps(input_data)).json()

def standup_start_req(token, channel_id, length):
    input_data = {
        "token": token,
        "channel_id": channel_id,
        "length": length
    }
    return requests.post(f"{url}standup/start/v1", data=json.dumps(input_data)).json()

def standup_active_req(token, channel_id):
    input_data = {
        "token": token,
        "channel_id": channel_id
    }
    return requests.get(f"{url}standup/active/v1", params=input_data).json()

def standup_send_req(token, channel_id, message):
    input_data = {
        "token": token,
        "channel_id": channel_id,
        "message": message
    }
    return requests.post(f"{url}standup/send/v1", data=json.dumps(input_data)).json()

def auth_passwordreset_request_req(email):
    input_data = {
        "email": email
    }
    return requests.post(f"{url}auth/passwordreset/request/v1", data=json.dumps(input_data)).json()

def auth_passwordreset_reset_req(reset_code, new_password):
    input_data = {
        "reset_code": reset_code,
        "new_password": new_password
    }
    return requests.post(f"{url}auth/passwordreset/reset/v1", data=json.dumps(input_data)).json()

def user_profile_uploadphoto_req(token, img_url, x_start, y_start, x_end, y_end):
    input_data = {
        "token": token,
        "img_url": img_url,
        "x_start": x_start,
        "y_start": y_start,
        "x_end": x_end,
        "y_end": y_end
    }
    return requests.post(f"{url}user/profile/uploadphoto/v1", data=json.dumps(input_data)).json()

def user_stats_req(token):
    input_data = {
        "token": token
    }
    return requests.get(f"{url}user/stats/v1", params=input_data).json()

def users_stats_req(token):
    input_data = {
        "token": token
    }
    return requests.get(f"{url}users/stats/v1", params=input_data).json()

def echo_req(value):
    input_data = {
        'value': value
    }
    return requests.get(f"{url}echo", params=input_data).json()

def channel_kick_req(token, channel_id, user_id):
    input_data = {
        "token": token,
        "channel_id": channel_id,
        "user_id": user_id
    }
    return requests.post(f"{url}channel/kick/v1", data=json.dumps(input_data)).json()

def dm_kick_req(token, dm_id, user_id):
    input_data = {
        "token": token,
        "dm_id": dm_id,
        "user_id": user_id
    }
    return requests.post(f"{url}dm/kick/v1", data=json.dumps(input_data)).json()