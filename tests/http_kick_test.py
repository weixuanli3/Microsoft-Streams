'''Contains http tests for kick.py'''
import pytest
import requests
import json
from src.error import AccessError, InputError
from other_functions.request_helper_functions import *
from src.config import url

# tests for channel_kick_req
def test_channel_kick_invalid_token():
    clear_req()
    user1_token = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan_id = channels_create_req(user1_token, "Channel 1", True)['channel_id']
    assert channel_kick_req(-1, chan_id, 2)['code'] == AccessError.code

def test_channel_kick_invalid_channel_id():
    clear_req()
    user1_token = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    channels_create_req(user1_token, "Channel 1", True)['channel_id']
    assert channel_kick_req(user1_token, 33, 1)['code'] == InputError.code

def test_channel_kick_invalid_user_id():
    clear_req()
    user1_token = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan_id = channels_create_req(user1_token, "Channel 1", True)['channel_id']
    assert channel_kick_req(user1_token, chan_id, 0)['code'] == InputError.code

def test_channel_kick_token_no_perms():
    clear_req()
    user1 = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")
    user2_token = auth_register_req("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['token']
    chan_id = channels_create_req(user1['token'], "Channel 1", True)['channel_id']
    channel_join_req(user2_token, chan_id)
    assert channel_kick_req(user2_token, chan_id, user1['auth_user_id'])['code'] == AccessError.code

def test_channel_kick_valid():
    clear_req()
    user1 = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")
    user1_token = user1['token']
    user1_id = user1['auth_user_id']
    user2 = auth_register_req("john.smith@aunsw.edu.au", "naisud", "John", "Smith")
    chan_id = channels_create_req(user1_token, "Channel 1", True)['channel_id']
    channel_join_req(user2['token'], chan_id)
    channel_kick_req(user1_token, chan_id, user2['auth_user_id'])
    assert (channel_details_req(user1_token, chan_id) == {
        'name' : 'Channel 1',
        'is_public' : True,
        'owner_members' : [{'email': 'john.doe@aunsw.edu.au', 'handle_str': 'johndoe', 'name_first': 'John', 'name_last': 'Doe', 'u_id': user1_id, 'profile_img_url': url + 'imgurl/default.jpg'}],
        'all_members' : [{'email': 'john.doe@aunsw.edu.au', 'handle_str': 'johndoe', 'name_first': 'John', 'name_last': 'Doe', 'u_id': user1_id, 'profile_img_url': url + 'imgurl/default.jpg'}],
    })

# tests for dm_kick_req
def test_dm_kick_invalid_token():
    clear_req()
    user1_token = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    user2_id = auth_register_req("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['auth_user_id']
    dm_id = dm_create_req(user1_token, [user2_id])['dm_id']
    assert dm_kick_req(-1, dm_id, 2)['code'] == AccessError.code

def test_dm_kick_invalid_channel_id():
    clear_req()
    user1_token = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    channels_create_req(user1_token, "Channel 1", True)['channel_id']
    assert dm_kick_req(user1_token, 33, 1)['code'] == InputError.code

def test_dm_kick_invalid_user_id():
    clear_req()
    user1_token = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    user2_id = auth_register_req("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['auth_user_id']
    dm_id = dm_create_req(user1_token, [user2_id])['dm_id']
    assert dm_kick_req(user1_token, dm_id, -1)['code'] == InputError.code

def test_dm_kick_token_no_perms():
    clear_req()
    user1 = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")
    user2 = auth_register_req("john.smith@aunsw.edu.au", "naisud", "John", "Smith")
    dm_id = dm_create_req(user1['token'], [user2['auth_user_id']])['dm_id']
    assert dm_kick_req(user2['token'], dm_id, user1['auth_user_id'])['code'] == AccessError.code

def test_dm_kick_valid():
    clear_req()
    user1 = auth_register_req("patrick.liang@unsw.com", "katrick", "Patrick", "Liang")
    user2_id = auth_register_req("john.citizen@unsw.com", "password", "John", "Citizen")['auth_user_id']
    user3_id = auth_register_req("jane.doe@aunsw.edu.au", "naisud", "Jane", "Doe")['auth_user_id']
    dm_id = dm_create_req(user1['token'], [user2_id, user3_id])['dm_id']
    dm_kick_req(user1['token'], dm_id, user3_id)
    u1_id = user1['auth_user_id']
    u2_id = user2_id
    u1 = {
        'u_id': u1_id,
        'email': "patrick.liang@unsw.com",
        'name_first': "Patrick",
        'name_last': "Liang",
        'handle_str': "patrickliang",
        'profile_img_url': url + 'imgurl/default.jpg'
    }
    u2 = {
        'u_id': u2_id,
        'email': "john.citizen@unsw.com",
        'name_first': "John",
        'name_last': "Citizen",
        'handle_str': "johncitizen",
        'profile_img_url': url + 'imgurl/default.jpg'
    }
    assert dm_details_req(user1['token'], dm_id) == {
        'name': 'janedoe, johncitizen, patrickliang',
        'members': [u1, u2]
    }
