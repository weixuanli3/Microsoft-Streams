''' Contains http tests for notifications_get'''
import pytest
import string
from src.error import AccessError, InputError
from other_functions.request_helper_functions import *

@pytest.fixture
def def_setup():
    clear_req()
    owner = auth_register_req("john.doe@unsw.com", "bruhdems", "John", "Doe")
    user1 = auth_register_req("patrick.liang@unsw.com", "katrick", "Patrick", "Liang")
    user2 = auth_register_req("john.citizen@unsw.com", "password", "John", "Citizen")
    own_handle_str = user_profile_req(owner['token'], owner['auth_user_id'])['user']['handle_str']
    u1_handle_str = user_profile_req(user1['token'], user1['auth_user_id'])['user']['handle_str']
    u2_handle_str = user_profile_req(user2['token'], user2['auth_user_id'])['user']['handle_str']
    return (owner, user1, user2, own_handle_str, u1_handle_str, u2_handle_str)

def test_notif_invalid_token(def_setup):
    owner, user1, user2, _, _, _ = def_setup
    token = owner['token'] + user1['token'] + user2['token']
    assert notifications_get_req(token)['code'] == AccessError.code

def test_notif_none(def_setup):
    owner, _, _, _, _, _ = def_setup
    assert notifications_get_req(owner['token']) == {
        'notifications': []
    }

def test_notif_one(def_setup):
    owner, user1, _, own_handle, _, _ = def_setup
    own_tok = owner['token']
    u1_tok = user1['token']
    u1_id = user1['auth_user_id']
    dm_id = dm_create_req(own_tok, [u1_id])['dm_id']
    
    dm_name = dm_details_req(own_tok, dm_id)['name']

    assert notifications_get_req(u1_tok) == {
        'notifications': [
            {
                'channel_id': -1,
                'dm_id': dm_id,
                'notification_message': f"{own_handle} added you to {dm_name}"
            }
        ]
    }

def test_notif_return_type(def_setup):
    owner, user1, _, _, _, _ = def_setup
    own_token = owner['token']
    chan_id = channels_create_req(own_token, "Banter", True)['channel_id']
    user_token = user1['token']
    user_id = user1['auth_user_id']
    channel_invite_req(own_token, chan_id, user_id)

    notifs = notifications_get_req(user_token)
    assert isinstance(notifs, dict)
    assert isinstance(notifs['notifications'], list)

    first_notif = notifs['notifications'][0]
    assert isinstance(first_notif, dict)
    assert isinstance(first_notif['channel_id'], int)
    assert isinstance(first_notif['dm_id'], int)
    assert isinstance(first_notif['notification_message'], str)

def test_notif_muliple_tags(def_setup):
    owner, user1, _, own_handle, u1_handle, _ = def_setup
    own_tok = owner['token']
    u1_tok = user1['token']
    chan_id = channels_create_req(own_tok, "BRUHDEMS", True)['channel_id']
    channel_join_req(u1_tok, chan_id)
    msg = f"@{u1_handle} @{u1_handle} @{u1_handle} hi"
    message_send_req(own_tok, chan_id, msg)
    assert notifications_get_req(u1_tok) == {
        'notifications': [
            {
                'channel_id': chan_id,
                'dm_id': -1,
                'notification_message': f"{own_handle} tagged you in BRUHDEMS: {msg[0:20]}"
            }
        ]
    }

def test_notif_tag_msg_less_20(def_setup):
    owner, user1, user2, own_handle, u1_handle, u2_handle = def_setup
    own_tok = owner['token']
    u1_tok = user1['token']
    u2_tok = user2['token']
    chan_id = channels_create_req(own_tok, "BRUHDEMS", True)['channel_id']
    channel_join_req(u1_tok, chan_id)
    channel_join_req(u2_tok, chan_id)
    message_send_req(own_tok, chan_id, f"@{u1_handle} hi")
    message_send_req(u2_tok, chan_id, f"@{u1_handle} hoi")
    assert notifications_get_req(u1_tok) == {
        'notifications': [
            {
                'channel_id': chan_id,
                'dm_id': -1,
                'notification_message': f"{u2_handle} tagged you in BRUHDEMS: @{u1_handle} hoi"
            },
            {
                'channel_id': chan_id,
                'dm_id': -1,
                'notification_message': f"{own_handle} tagged you in BRUHDEMS: @{u1_handle} hi"
            }
        ]
    }

def test_notif_tag_msg_more_20(def_setup):
    owner, user1, user2, own_handle, u1_handle, u2_handle = def_setup
    own_tok = owner['token']
    u1_tok = user1['token']
    u1_id = user1['auth_user_id']
    u2_tok = user2['token']
    u2_id = user2['auth_user_id']
    chan_name = "BRUHDEMS"
    chan_id = channels_create_req(own_tok, chan_name, False)['channel_id']
    
    channel_invite_req(own_tok, chan_id, u1_id)
    channel_invite_req(own_tok, chan_id, u2_id)
    msg_1 = f"@{u1_handle} hi how are you today"
    message_send_req(own_tok, chan_id, msg_1)
    msg_2 = f"@{u1_handle} yeah how are you, heard some crazy stuff"
    message_send_req(u2_tok, chan_id, msg_2)
    assert notifications_get_req(u1_tok) == {
        'notifications': [
            {
                'channel_id': chan_id,
                'dm_id': -1,
                'notification_message': f"{u2_handle} tagged you in {chan_name}: {msg_2[:20]}"
            },
            {
                'channel_id': chan_id,
                'dm_id': -1,
                'notification_message': f"{own_handle} tagged you in {chan_name}: {msg_1[:20]}"
            },
            {
                'channel_id': chan_id,
                'dm_id': -1,
                'notification_message': f"{own_handle} added you to {chan_name}"
            }
        ]
    }

def test_notif_more_than_twenty(def_setup):
    owner, user1, _, own_handle, u1_handle, _ = def_setup
    own_tok = owner['token']
    own_id = owner['auth_user_id']
    u1_tok = user1['token']
    u2_id = user1['auth_user_id']

    dm_id = dm_create_req(u1_tok, [own_id, u2_id])['dm_id']
    dm_name = dm_details_req(own_tok, dm_id)['name']

    lowcase = string.ascii_lowercase
    for letter in lowcase:
        message_senddm_req(u1_tok, dm_id, f"@{own_handle} {letter} lol")
    owner_notifs = notifications_get_req(own_tok)['notifications']

    assert len(owner_notifs) == 20
    
    for i in range(20):
        assert owner_notifs[i] == {
            'channel_id': -1,
            'dm_id': dm_id,
            'notification_message': f"{u1_handle} tagged you in {dm_name}: @{own_handle} {lowcase[25 - i]} lo"
        }

def test_notif_reacts(def_setup):
    owner, user1, user2, own_handle, u1_handle, u2_handle = def_setup
    own_tok = owner['token']
    u1_tok = user1['token']
    u1_id = user1['auth_user_id']
    u2_tok = user2['token']
    u2_id = user2['auth_user_id']
    chan_name = 'MERC>BMW'
    chan_id = channels_create_req(own_tok, chan_name, False)['channel_id']
    channel_invite_req(own_tok, chan_id, u1_id)
    channel_invite_req(own_tok, chan_id, u2_id)
    msg_1 = f"@{u1_handle} hi how are you today"
    message_send_req(own_tok, chan_id, msg_1)
    msg_2 = f"@{u1_handle} yeah how are you, heard some crazy stuff"
    message_send_req(u2_tok, chan_id, msg_2)
    msg_id = message_send_req(u1_tok, chan_id, "Could be better without iteration 3 due...")['message_id']
    message_react_req(own_tok, msg_id, 1)
    message_react_req(u2_tok, msg_id, 1)
    assert notifications_get_req(u1_tok) == {
        'notifications': [
            {
                'channel_id': chan_id,
                'dm_id': -1,
                'notification_message': f"{u2_handle} reacted to your message in {chan_name}"
            },
            {
                'channel_id': chan_id,
                'dm_id': -1,
                'notification_message': f"{own_handle} reacted to your message in {chan_name}"
            },
            {
                'channel_id': chan_id,
                'dm_id': -1,
                'notification_message': f"{u2_handle} tagged you in {chan_name}: {msg_2[:20]}"
            },
            {
                'channel_id': chan_id,
                'dm_id': -1,
                'notification_message': f"{own_handle} tagged you in {chan_name}: {msg_1[:20]}"
            },
            {
                'channel_id': chan_id,
                'dm_id': -1,
                'notification_message': f"{own_handle} added you to {chan_name}"
            }
        ]
    }

def test_notif_reacts_more_than_twenty():
    pass