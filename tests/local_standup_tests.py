import pytest
from src.error import AccessError, InputError
from src.other import clear_v1
from src.standup import standup_start_v1, standup_active_v1, standup_send_v1
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.channel import channel_invite_v1, channel_leave_v1, channel_messages_v1, channel_join_v1
from datetime import time, datetime

@pytest.fixture
def default_setup():
    clear_v1()
    u1 = auth_register_v1("john.doe@unsw.com", "password1", "John", "Doe")
    u1_tok = u1['token']
    chan1_id = channels_create_v1(u1_tok, "Channel 1", True)['channel_id']
    return (u1_tok, chan1_id)

''' standup/start/v1 '''

def test_standup_start_invalid_channel():
    clear_v1()
    u1 = auth_register_v1("john.doe@unsw.com", "password1", "John", "Doe")
    u1_tok = u1['token']
    with pytest.raises(InputError):
        standup_start_v1(u1_tok, "channel", 5)

def test_standup_start_invalid_length(default_setup):
    u1_tok, chan1_id = default_setup
    with pytest.raises(InputError):
        standup_start_v1(u1_tok, chan1_id, -1)
    with pytest.raises(InputError):
        standup_start_v1(u1_tok, chan1_id, -9999999)
        
def test_standup_start_already_active_standup(default_setup):
    u1_tok, chan1_id = default_setup
    u2 = auth_register_v1("john.doe1@unsw.com", "password1", "John", "Doe")
    u2_tok = u2['token']
    channel_join_v1(u2_tok, chan1_id)
    standup_start_v1(u1_tok, chan1_id, 5)
    with pytest.raises(InputError):
        standup_start_v1(u2_tok, chan1_id, 5)
        
def test_standup_start_not_member_of_channel():
    clear_v1()
    u1 = auth_register_v1("john.doe@unsw.com", "password1", "John", "Doe")
    u1_tok = u1['token']
    u2 = auth_register_v1("john.doe1@unsw.com", "password1", "John", "Doe")
    u2_tok = u2['token']
    chan1_id = channels_create_v1(u1_tok, "Channel 1", True)['channel_id']
    with pytest.raises(AccessError):
        standup_start_v1(u2_tok, chan1_id, 5)

''' standup/active/v1 '''

def test_standup_active_invalid_channel(default_setup):
    u1_tok, chan1_id = default_setup
    standup_start_v1(u1_tok, chan1_id, 5)
    with pytest.raises(InputError):
        standup_active_v1(u1_tok, 5)
        
def test_standup_active_not_member_of_channel():
    clear_v1()
    u1 = auth_register_v1("john.doe@unsw.com", "password1", "John", "Doe")
    u1_tok = u1['token']
    u2 = auth_register_v1("john.doe1@unsw.com", "password1", "John", "Doe")
    u2_tok = u2['token']
    chan1_id = channels_create_v1(u1_tok, "Channel 1", True)['channel_id']
    with pytest.raises(AccessError):
        standup_active_v1(u2_tok, chan1_id)

# Not sure what return value so isn't complete
# def test_standup_active_already_active():
#     u1_tok, chan1_id = default_setup
#     u2 = auth_register_v1("john.doe1@unsw.com", "password1", "John", "Doe")
#     u2_tok = u2['token']
#     channel_join_v1(u2_tok, chan1_id)
#     standup_start_v1(u1_tok, chan1_id, 5)
#     assert standup_start_v1(u2_tok, chan1_id) == {}
    
def test_standup_active_not_active(default_setup):
    u1_tok, chan1_id = default_setup
    assert standup_active_v1(u1_tok, chan1_id) == {False, None}

''' standup/send/v1 '''

def test_standup_send_invalid_channel(default_setup):
    u1_tok, chan1_id = default_setup
    standup_start_v1(u1_tok, chan1_id, 5)
    with pytest.raises(InputError):
        standup_send_v1(u1_tok, "channel", "message")
        
def test_standup_send_message_long(default_setup):
    u1_tok, chan1_id = default_setup
    standup_start_v1(u1_tok, chan1_id, 5)
    with pytest.raises(InputError):
        standup_send_v1(u1_tok, chan1_id, "argh!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

def test_standup_send_not_active(default_setup):
    u1_tok, chan1_id = default_setup
    with pytest.raises(InputError):
        standup_send_v1(u1_tok, chan1_id, "message")
        
def test_standup_send_not_member():
    clear_v1()
    u1 = auth_register_v1("john.doe@unsw.com", "password1", "John", "Doe")
    u1_tok = u1['token']
    u2 = auth_register_v1("john.doe1@unsw.com", "password1", "John", "Doe")
    u2_tok = u2['token']
    chan1_id = channels_create_v1(u1_tok, "Channel 1", True)['channel_id']
    with pytest.raises(AccessError):
        standup_send_v1(u2_tok, chan1_id, "message")

def test_standup_send_valid(default_setup):
    u1_tok, chan1_id = default_setup
    standup_start_v1(u1_tok, chan1_id, 5)
    standup_send_v1(u1_tok, chan1_id, "argh!!!!!!")
