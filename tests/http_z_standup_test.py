import pytest
import requests
import json
from src.error import AccessError, InputError
from other_functions.request_helper_functions import *

@pytest.fixture
def default_setup():
    clear_req()
    u1 = auth_register_req("john.doe@unsw.com", "password1", "John", "Doe")
    u1_tok = u1['token']
    chan1_id = channels_create_req(u1_tok, "Channel 1", True)['channel_id']
    return (u1_tok, chan1_id)

''' standup/start/req '''

def test_standup_start_invalid_channel():
    clear_req()
    u1 = auth_register_req("john.doe@unsw.com", "password1", "John", "Doe")
    u1_tok = u1['token']
    assert standup_start_req(u1_tok, "channel", 5)['code'] == InputError.code

def test_standup_start_invalid_length(default_setup):
    u1_tok, chan1_id = default_setup
    assert standup_start_req(u1_tok, chan1_id, -1)['code'] == InputError.code
    assert standup_start_req(u1_tok, chan1_id, -9999999)['code'] == InputError.code
        
def test_standup_start_already_active_standup(default_setup):
    u1_tok, chan1_id = default_setup
    u2 = auth_register_req("john.doe1@unsw.com", "password1", "John", "Doe")
    u2_tok = u2['token']
    channel_join_req(u2_tok, chan1_id)
    standup_start_req(u1_tok, chan1_id, 5)
    assert standup_start_req(u2_tok, chan1_id, 5)['code'] == InputError.code
        
def test_standup_start_not_member_of_channel():
    clear_req()
    u1 = auth_register_req("john.doe@unsw.com", "password1", "John", "Doe")
    u1_tok = u1['token']
    u2 = auth_register_req("john.doe1@unsw.com", "password1", "John", "Doe")
    u2_tok = u2['token']
    chan1_id = channels_create_req(u1_tok, "Channel 1", True)['channel_id']
    assert standup_start_req(u2_tok, chan1_id, 5)['code'] == AccessError.code

''' standup/active/req '''

def test_standup_active_invalid_channel(default_setup):
    u1_tok, chan1_id = default_setup
    standup_start_req(u1_tok, chan1_id, 5)
    assert standup_active_req(u1_tok, 5)['code'] == InputError.code
        
def test_standup_active_not_member_of_channel():
    clear_req()
    u1 = auth_register_req("john.doe@unsw.com", "password1", "John", "Doe")
    u1_tok = u1['token']
    u2 = auth_register_req("john.doe1@unsw.com", "password1", "John", "Doe")
    u2_tok = u2['token']
    chan1_id = channels_create_req(u1_tok, "Channel 1", True)['channel_id']
    assert standup_active_req(u2_tok, chan1_id)['code'] == AccessError.code

# Not sure what return value so isn't complete
# def test_standup_active_already_active():
#     u1_tok, chan1_id = default_setup
#     u2 = auth_register_req("john.doe1@unsw.com", "password1", "John", "Doe")
#     u2_tok = u2['token']
#     channel_join_req(u2_tok, chan1_id)
#     standup_start_req(u1_tok, chan1_id, 5)
#     assert standup_start_req(u2_tok, chan1_id) == {}
    
def test_standup_active_not_active(default_setup):
    u1_tok, chan1_id = default_setup
    assert standup_active_req(u1_tok, chan1_id) == {
        "is_active": False, 
        "time_finish": None
    }

''' standup/send/req '''

def test_standup_send_invalid_channel(default_setup):
    u1_tok, chan1_id = default_setup
    standup_start_req(u1_tok, chan1_id, 5)
    assert standup_send_req(u1_tok, "channel", "message")['code'] == InputError.code
        
def test_standup_send_message_long(default_setup):
    u1_tok, chan1_id = default_setup
    standup_start_req(u1_tok, chan1_id, 5)
    assert standup_send_req(u1_tok, chan1_id, "argh!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")['code'] == InputError.code

def test_standup_send_not_active(default_setup):
    u1_tok, chan1_id = default_setup
    assert standup_send_req(u1_tok, chan1_id, "message")['code'] == InputError.code
        
def test_standup_send_not_member():
    clear_req()
    u1 = auth_register_req("john.doe@unsw.com", "password1", "John", "Doe")
    u1_tok = u1['token']
    u2 = auth_register_req("john.doe1@unsw.com", "password1", "John", "Doe")
    u2_tok = u2['token']
    chan1_id = channels_create_req(u1_tok, "Channel 1", True)['channel_id']
    assert standup_send_req(u2_tok, chan1_id, "message")['code'] == AccessError.code

def test_standup_send_valid(default_setup):
    u1_tok, chan1_id = default_setup
    standup_start_req(u1_tok, chan1_id, 5)
    standup_send_req(u1_tok, chan1_id, "argh!!!!!!")
