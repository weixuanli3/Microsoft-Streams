'''Contains http tests for dm.py'''
import pytest
import requests
import json
from src.error import AccessError, InputError
from other_functions.request_helper_functions import *
from src.config import url

@pytest.fixture
def default_setup():
    clear_req()
    u1 = auth_register_req("patrick.liang@unsw.com", "katrick", "Patrick", "Liang")
    u2 = auth_register_req("john.citizen@unsw.com", "password", "John", "Citizen")
    u3 = auth_register_req("john.doe@unsw.com", "bruhyikes", "John", "Doe")
    return (u1, u2, u3)

@pytest.fixture
def dms_setup(default_setup):
    u1, u2, u3 = default_setup
    u1_tok = u1['token']
    u2_tok = u2['token']
    u2_id = u2['auth_user_id']
    u3_id = u3['auth_user_id']
    dm_id1 = dm_create_req(u1_tok, [u2_id, u3_id])['dm_id']
    dm_id2 = dm_create_req(u2_tok, [u3_id])['dm_id']
    return (u1, u2, u3, dm_id1, dm_id2)

def test_dm_create_invalid(default_setup):
    u1, u2, u3 = default_setup
    u1_tok = u1['token']
    u2_id = u2['auth_user_id']
    u3_id = u3['auth_user_id']
    invalid_dm_id = dm_create_req(u1_tok, [u3_id + u2_id])
    assert invalid_dm_id['code'] == InputError.code

    invalid_dm_id2 = dm_create_req(u1_tok, [u2_id, u3_id + u2_id, u3_id])
    assert invalid_dm_id2['code'] == InputError.code

    auth_logout_req(u1_tok)
    invalid_token = dm_create_req(u1_tok, [u3_id, u2_id])
    assert invalid_token['code'] == AccessError.code
    
def test_dm_create_invalid_token(default_setup):
    u1, u2, u3 = default_setup

    assert dm_create_req("mdsfjo", [u2['token'], u3['token'], u1['token']])['code'] == AccessError.code


def test_dm_create_valid(default_setup):
    u1, u2, u3 = default_setup
    u1_tok = u1['token']
    u2_tok = u2['token']
    u2_id = u2['auth_user_id']
    u3_id = u3['auth_user_id']

    dm_id1 = dm_create_req(u1_tok, [u2_id, u3_id])['dm_id']
    dm_id2 = dm_create_req(u2_tok, [u3_id])['dm_id']

    assert dm_id1 != dm_id2

# not a member and then invalid dm id
def test_dm_details_invalid(default_setup):
    u1, u2, u3 = default_setup
    u1_tok = u1['token']
    u2_id = u2['auth_user_id']
    u3_tok = u3['token']
    
    invalid_dm_id = dm_details_req(u1_tok, 23)
    assert invalid_dm_id['code'] == InputError.code

    dm_id = dm_create_req(u1_tok, [u2_id])['dm_id']
    user_not_in_dm = dm_details_req(u3_tok, dm_id)
    assert user_not_in_dm['code'] == AccessError.code

def test_dm_details_valid(default_setup):
    u1, u2, u3 = default_setup
    u1_tok = u1['token']
    u1_id = u1['auth_user_id']
    u2_id = u2['auth_user_id']
    u3_id = u3['auth_user_id']
    user1 = {
        "u_id": u1_id,
        "email": "patrick.liang@unsw.com",
        "name_first": "Patrick",
        "name_last": "Liang",
        "handle_str": "patrickliang",
        'profile_img_url': url + 'imgurl/default.jpg'
    }
    user2 = {
        "u_id": u2_id,
        "email": "john.citizen@unsw.com",
        "name_first": "John",
        "name_last": "Citizen",
        "handle_str": "johncitizen",
        'profile_img_url': url + 'imgurl/default.jpg'
    }
    user3 = {
        "u_id": u3_id,
        "email": "john.doe@unsw.com",
        "name_first": "John",
        "name_last": "Doe",
        "handle_str": "johndoe",
        'profile_img_url': url + 'imgurl/default.jpg'
    }
    dm_id0 = dm_create_req(u1_tok, [u3_id, u2_id])['dm_id']
    details = dm_details_req(u1_tok, dm_id0)
    assert details == {
        'name': "johncitizen, johndoe, patrickliang",
        'members': [user1, user3, user2]
    }
    
def test_dm_details_bad_token(default_setup):
    u1, u2, u3 = default_setup
    u1_tok = u1['token']
    u2_id = u2['auth_user_id']
    u3_id = u3['auth_user_id']
    dm_id0 = dm_create_req(u1_tok, [u3_id, u2_id])['dm_id']
    assert dm_details_req("fsdffeefw", dm_id0)['code'] == AccessError.code
    
# The following tests are for leave

def test_dm_leave_valid(dms_setup):
    u1, u2, u3, dm_id1, dm_id2 = dms_setup
    u1_tok = u1['token']
    u2_tok = u2['token']
    u2_id = u2['auth_user_id']
    u3_tok = u3['token']
    u3_id = u3['auth_user_id']
    user2 = {
        'u_id': u2_id,
        'email': "john.citizen@unsw.com",
        'name_first': "John",
        'name_last': "Citizen",
        'handle_str': "johncitizen",
        'profile_img_url': url + 'imgurl/default.jpg'
    }
    user3 = {
        "u_id": u3_id,
        "email": "john.doe@unsw.com",
        "name_first": "John",
        "name_last": "Doe",
        "handle_str": "johndoe",
        'profile_img_url': url + 'imgurl/default.jpg'
    }
    assert dm_leave_req(u1_tok, dm_id1) == {}
    assert dm_leave_req(u3_tok, dm_id2) == {}

    assert dm_details_req(u2_tok, dm_id1) == {
        'name': 'johncitizen, johndoe, patrickliang',
        'members': [user2, user3]
    }
    assert dm_details_req(u2_tok, dm_id2) == {
        'name': 'johncitizen, johndoe',
        'members': [user2]
    }

    
def test_dm_leave_bad_token(default_setup):
    u1, u2, u3 = default_setup
    
    dm_id = dm_create_req(u1['token'], [u2['auth_user_id'], u3['auth_user_id']])['dm_id']

    assert dm_leave_req("efef", dm_id)['code'] == AccessError.code


def test_dm_leave_invalid(dms_setup):
    u1, u2, u3, dm_id1, dm_id2 = dms_setup
    u1_tok = u1['token']
    u2_tok = u2['token']
    u3_tok = u3['token']
    u4_tok = auth_register_req("nangstonkjn.w@unsw.com", "nangwei", "Wynston", "Wang")['token']
    assert dm_leave_req(u2_tok, dm_id1 + dm_id2)['code'] == InputError.code
    assert dm_leave_req(u1_tok, -1)['code'] == InputError.code
    assert dm_leave_req(u2_tok, -1)['code'] == InputError.code
    assert dm_leave_req(u3_tok, -1)['code'] == InputError.code

    assert dm_leave_req(u4_tok, dm_id1)['code'] == AccessError.code
    assert dm_leave_req(u1_tok, dm_id2)['code'] == AccessError.code
    assert dm_leave_req(u4_tok, dm_id1)['code'] == AccessError.code
    dm_leave_req(u3_tok, dm_id2)
    assert dm_leave_req(u3_tok, dm_id2)['code'] == AccessError.code

# The following tests are for dm_list

def test_dm_list_valid(default_setup):
    u1, u2, u3 = default_setup
    u1_tok = u1['token']
    u2_tok = u2['token']
    u2_id = u2['auth_user_id']
    u3_id = u3['auth_user_id']
    u3_tok = u3['token']
    assert dm_list_req(u1_tok) == {'dms': []}
    dm_id1 = dm_create_req(u1_tok, [u2_id, u3_id])['dm_id']
    assert dm_list_req(u1_tok) == {
        'dms': [
            {
                'dm_id': dm_id1,
                'name': 'johncitizen, johndoe, patrickliang'
            }
        ]
    }
    dm_id2 = dm_create_req(u2_tok, [u3_id])['dm_id']
    assert dm_list_req(u1_tok) == {
        'dms': [
            {
                'dm_id': dm_id1,
                'name': 'johncitizen, johndoe, patrickliang'
            }
        ]
    }
    assert dm_list_req(u2_tok) == {
        'dms': [
            {
                'dm_id': dm_id1,
                'name': 'johncitizen, johndoe, patrickliang'
            },
            {
                'dm_id': dm_id2,
                'name': 'johncitizen, johndoe'
            }
        ]
    }
    assert dm_list_req(u3_tok) == {
        'dms': [
            {
                'dm_id': dm_id1,
                'name': 'johncitizen, johndoe, patrickliang'
            },
            {
                'dm_id': dm_id2,
                'name': 'johncitizen, johndoe'
            }
        ]
    }

def test_dm_list_bad_token(default_setup):
    u1, u2, u3 = default_setup
    dm_create_req(u1['token'], [u2['auth_user_id'], u3['auth_user_id']])

    assert dm_list_req("dsfjnodcf")['code'] == AccessError.code
    
# The following tests are for dm_remove

def test_dm_remove_valid(default_setup):
    u1, u2, u3 = default_setup
    u1_tok = u1['token']
    u2_tok = u2['token']
    u2_id = u2['auth_user_id']
    u3_id = u3['auth_user_id']
    dm_id1 = dm_create_req(u1_tok, [u2_id, u3_id])['dm_id']
    dm_id2 = dm_create_req(u2_tok, [u3_id])['dm_id']
    dm_remove_req(u1_tok, dm_id1)
    dm_remove_req(u2_tok, dm_id2)

def test_dm_remove_bad_token(default_setup):
    u1, u2, u3 = default_setup
    u1_tok = u1['token']
    u2_tok = u2['token']
    u2_id = u2['auth_user_id']
    u3_id = u3['auth_user_id']
    dm_id1 = dm_create_req(u1_tok, [u2_id, u3_id])['dm_id']
    dm_id2 = dm_create_req(u2_tok, [u3_id])['dm_id']
    assert dm_remove_req("dfvwffd", dm_id1)['code'] == AccessError.code
    assert dm_remove_req("dcsdcsdc", dm_id2)['code'] == AccessError.code

def test_dm_remove_invalid(dms_setup):
    u1, u2, u3, dm_id1, dm_id2 = dms_setup
    u1_tok = u1['token']
    u2_tok = u2['token']
    u3_tok = u3['token']
    dm_id3 = dm_id1 + dm_id2 + 3123
    assert dm_remove_req(u2_tok, dm_id3)['code'] == InputError.code
    assert dm_remove_req(u1_tok, dm_id3)['code'] == InputError.code
    assert dm_remove_req(u2_tok, dm_id3)['code'] == InputError.code
    assert dm_remove_req(u3_tok, dm_id3)['code'] == InputError.code

    assert dm_remove_req(u1_tok, dm_id2)['code'] == AccessError.code
    assert dm_remove_req(u2_tok, dm_id1)['code'] == AccessError.code
    assert dm_remove_req(u3_tok, dm_id1)['code'] == AccessError.code

def test_dm_messages_valid_less_than_50(default_setup):
    u1, u2, u3 = default_setup
    u1_tok = u1['token']
    u1_id = u1['auth_user_id']
    u2_tok = u2['token']
    u2_id = u2['auth_user_id']
    u3_tok = u3['token']
    u3_id = u3['auth_user_id']
    dm_id1 = dm_create_req(u1_tok, [u2_id, u3_id])['dm_id']
    m1 = message_senddm_req(u1_tok, dm_id1, "Hey everyone")['message_id']
    m2 = message_senddm_req(u2_tok, dm_id1, "Hello")['message_id']
    m3 = message_senddm_req(u3_tok, dm_id1, "G'day")['message_id']
    dm_msg = dm_messages_req(u1_tok, dm_id1, 0)
    msgs = [
        "Hey everyone",
        "Hello",
        "G'day"
    ]
    msg_ids = [m3, m2, m1]
    u_ids = [u3_id, u2_id, u1_id]
    assert dm_msg['start'] == 0
    assert dm_msg['end'] == -1
    for i in range(0, 3):
        assert dm_msg['messages'][i]['message_id'] == msg_ids[i]
        assert dm_msg['messages'][i]['u_id'] == u_ids[i]
        assert dm_msg['messages'][i]['message'] == msgs[2 - i]
        
def test_dm_messages_bad_token(default_setup):
    u1, u2, u3 = default_setup
    u1_tok = u1['token']
    u2_tok = u2['token']
    u2_id = u2['auth_user_id']
    u3_tok = u3['token']
    u3_id = u3['auth_user_id']
    dm_id1 = dm_create_req(u1_tok, [u2_id, u3_id])['dm_id']
    message_senddm_req(u1_tok, dm_id1, "Hey everyone")['message_id']
    message_senddm_req(u2_tok, dm_id1, "Hello")['message_id']
    message_senddm_req(u3_tok, dm_id1, "G'day")['message_id']
    assert dm_messages_req("fdvnjfdoif", dm_id1, 0)['code'] == AccessError.code
    

def test_dm_messages_valid_more_than_50(default_setup):
    u1, u2, u3 = default_setup
    u1_tok = u1['token']
    u1_id = u1['auth_user_id']
    u2_tok = u2['token']
    u2_id = u2['auth_user_id']
    u3_tok = u3['token']
    u3_id = u3['auth_user_id']
    dm_id1 = dm_create_req(u1_tok, [u2_id, u3_id])['dm_id']
    msgs = [str(i) for i in range(0, 72)]
    u_ids = [u1_id, u2_id, u3_id]
    tokens = [u1_tok, u2_tok, u3_tok]
    msg_ids = []
    for i in range(0, 72):
        msg_ids.append(message_senddm_req(tokens[i % 3], dm_id1, msgs[i])['message_id'])
    dm_msg = dm_messages_req(u1_tok, dm_id1, 0)
    messages = dm_msg['messages']
    assert dm_msg['start'] == 0
    assert dm_msg['end'] == 50
    for i in range(0, 50):
        assert messages[i]['message_id'] == msg_ids[71 - i]
        assert messages[i]['u_id'] == u_ids[(71 - i) % 3]
        assert messages[i]['message'] == msgs[71 - i]
    

def test_dm_messages_invalid(dms_setup):
    u1, u2, u3, dm_id1, dm_id2 = dms_setup
    u1_tok = u1['token']
    u2_tok = u2['token']
    u3_tok = u3['token']
    # Test an invalid dm_id
    dm_id3 = dm_id1 + dm_id2 + 123
    assert dm_messages_req(u1_tok, dm_id3, 0)['code'] == InputError.code
    # Test if the start is greater than the number of messages
    message_senddm_req(u1_tok, dm_id1, "Hey everyone")
    message_senddm_req(u2_tok, dm_id1, "Hello")
    assert dm_messages_req(u3_tok, dm_id1, 5)['code'] == InputError.code
    # Test if the user is not in the dm
    assert dm_messages_req(u1_tok, dm_id2, 5)['code'] == AccessError.code
    # Test if the start index is negative
    assert dm_messages_req(u3_tok, dm_id1, -23)['code'] == InputError.code
    # Test if there are no messages to display
    assert dm_messages_req(u2_tok, dm_id2, 4)['code'] == InputError.code