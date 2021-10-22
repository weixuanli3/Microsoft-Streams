import pytest
import requests
import json
from src.error import AccessError, InputError
from src.request_helper_functions import *
from src.config import url
from src.auth import auth_logout_v1, auth_register_v1
from src.channels import channels_create_v1
from src.channel import channel_invite_v1, channel_leave_v1, channel_messages_v1
from src.channel import channel_join_v1, channel_remove_owner_v1, channel_add_owner_v1
from src.channel import channel_details_v1
from src.message import message_send_v1
from src.other import clear_v1
from src.data_store import get_u_id

@pytest.fixture
def default_setup():
    clear_req()
    u1 = auth_register_req("patrick.liang@unsw.com", "katrick", "Patrick", "Liang")
    u2 = auth_register_req("john.citizen@unsw.com", "password", "John", "Citizen")
    u3 = auth_register_req("john.doe@unsw.com", "bruhyikes", "John", "Doe")
    return (u1, u2, u3)

@pytest.fixture
def Channel_setup(default_setup):
    u1, u2, u3 = default_setup
    u1_tok = u1['token']
    u2_tok = u2['token']
    chan1_id = channels_create_req(u1_tok, "Channel 1", True)['channel_id']
    chan2_id = channels_create_req(u2_tok, "Channel 2", True)['channel_id']
    return (u1, u2, u3, chan1_id, chan2_id)

@pytest.fixture
def Channel_setup_one(default_setup):
    u1, u2, u3 = default_setup
    u1_tok = u1['token']
    u2_tok = u2['token']
    chan1_id = channels_create_req(u1_tok, "Channel 1", True)['channel_id']
    return (u1, u2, u3, chan1_id)


def test_invite_invalid_channel(default_setup):
    u1, u2, u3 = default_setup
    u1_tok = u1['token']
    u2_id = u2['auth_user_id']
    u3_id = u3['auth_user_id']
    channels_create_req(u1_tok, "Channel 1", True)
    assert channel_invite_req(u1_tok, 33, u2_id)['code'] == InputError.code
    channels_create_req(u2['token'], "Channel 2", True)
    assert channel_invite_req(u2['token'], 44, u3_id)['code'] == InputError.code



def test_channel_invite_uid_invalid():
    clear_req()
    u1 = auth_register_req("patrick.liang@unsw.com", "katrick", "Patrick", "Liang")
    chan1_id = channels_create_req(u1['token'], "Channel 1", True)
    assert channel_invite_req(u1['token'], chan1_id, 22)['code'] == InputError.code

def test_channel_invite_uid_in_channel(Channel_setup):
    u1, u2, u3, chan1_id, chan2_id = Channel_setup
    u1_tok = u1['token']
    u2_id = u2['auth_user_id']
    u3_id = u3['auth_user_id']
    channel_join_req(u2['token'], chan1_id)
    channel_join_req(u3['token'], chan2_id)
    assert channel_invite_req(u1['token'], chan1_id, u2_id)['code'] == InputError.code
    assert channel_invite_req(u2['token'], chan2_id, u3_id)['code'] == InputError.code

def test_channel_invite_auth_not_in_channel(Channel_setup):
    u1, u2, u3, chan1_id, chan2_id = Channel_setup

    assert channel_invite_req(u2['token'], chan1_id, u3['auth_user_id'])['code'] == AccessError.code
    assert channel_invite_req(u1['token'], chan2_id, u3['auth_user_id'])['code'] == AccessError.code

def test_channel_invite_valid(Channel_setup):
    u1, u2, u3, chan1_id, chan2_id = Channel_setup
    channel_invite_req(u1['token'], chan1_id, u3['auth_user_id'])
    channel_invite_req(u2['token'], chan2_id, u3['auth_user_id'])

def test_channel_invite_channel_id_empty(default_setup):
    u1, u2, u3  = default_setup
    assert channel_invite_req(u1['token'], "", u3['auth_user_id'])['code'] == InputError.code
    assert channel_invite_req(u2['token'], "", u3['auth_user_id'])['code'] == InputError.code

def test_channel_invite_user_id_empty(Channel_setup):
    u1, u2, u3, chan1_id, chan2_id = Channel_setup
    channel_join_req(u3['token'], chan1_id)
    
    assert channel_invite_req(u1['token'], chan1_id, "")['code'] == InputError.code
    assert channel_invite_req(u2['token'], chan2_id, "")['code'] == InputError.code
    assert channel_invite_req(u3['token'], chan1_id, "")['code'] == InputError.code

def test_channel_invite_no_channels(default_setup):
    u1, u2, u3 = default_setup
    assert channel_invite_req(u1['token'], 1, u3['auth_user_id'])['code'] == InputError.code

def test_channel_invite_auth_id_invalid(Channel_setup):
    u1, u2, u3, chan1_id, chan2_id = Channel_setup
    
    assert channel_invite_req("", chan1_id, u3['auth_user_id'])['code'] == AccessError.code
    assert channel_invite_req("", chan2_id, u3['auth_user_id'])['code'] == AccessError.code

def test_channel_invite_user_invites_self(Channel_setup):
    u1, u2, u3, chan1_id, chan2_id = Channel_setup
    channel_join_req(u3['token'], chan1_id)
    
    assert channel_invite_req(u1['token'], chan1_id, u1['auth_user_id'])['code'] == InputError.code
    assert channel_invite_req(u2['token'], chan2_id, u2['auth_user_id'])['code'] == InputError.code
    assert channel_invite_req(u3['token'], chan1_id, u3['auth_user_id'])['code'] == InputError.code

def test_channel_invite_all_invalid():
    assert channel_invite_req("", "", "")['code'] == AccessError.code

# The following tests are for channel_join
def test_channel_join_public_channel(Channel_setup):
    u1, u2, u3, chan1_id, chan2_id = Channel_setup
    assert channel_join_req(u3['token'], chan1_id) == {}
    assert channel_join_req(u3['token'], chan2_id) == {}

def test_channel_join_channel_user_aready_in(Channel_setup):
    u1, u2, u3, chan1_id, chan2_id = Channel_setup
    channel_join_req(u3['token'], chan1_id)
    channel_join_req(u3['token'], chan2_id)
    
    assert channel_join_req(u3['token'], chan1_id)['code'] == InputError.code
    assert channel_join_req(u3['token'], chan2_id)['code'] == InputError.code


def test_channel_join_channel_private(default_setup):
    u1, u2, u3 = default_setup
    chan1_id = channels_create_req(u1['token'], "Channel 1", False)['channel_id']
    chan2_id = channels_create_req(u2['token'], "Channel 2", False)['channel_id']
    assert channel_join_req(u3['token'], chan1_id)['code'] == AccessError.code
    assert channel_join_req(u3['token'], chan2_id)['code'] == AccessError.code

def test_channel_join_channel_user_aready_in_private(default_setup):
    u1, u2, u3 = default_setup
    chan1_id = channels_create_req(u1['token'], "Channel 1", False)
    chan2_id = channels_create_req(u2['token'], "Channel 2", False)
    chan3_id = channels_create_req(u3['token'], "Channel 3", False)
    
    assert channel_join_req(u1['token'], chan1_id)['code'] == InputError.code
    assert channel_join_req(u2['token'], chan2_id)['code'] == InputError.code
    assert channel_join_req(u3['token'], chan3_id)['code'] == InputError.code

def test_channel_join_channel_user_does_not_exist():
    clear_req()
    u1 = auth_register_req("patrick.liang@unsw.com", "katrick", "Patrick", "Liang")
    chan_id = channels_create_req(u1['token'], "Channel 1", True)['channel_id']
    auth_logout_req(u1['token'])
    assert channel_join_req(443, chan_id)['code'] == AccessError.code

def test_channel_join_channel_channel_does_not_exist(default_setup):
    u1, u2, u3 = default_setup
    assert channel_join_req(u1['token'], 3333)['code'] == InputError.code
    assert channel_join_req(u2['token'], 3333)['code'] == InputError.code
    assert channel_join_req(u3['token'], 3333)['code'] == InputError.code

def test_channel_join_channel_user_token_empty():
    clear_req()
    u1 = auth_register_req("patrick.liang@unsw.com", "katrick", "Patrick", "Liang")
    chan_id = channels_create_req(u1['token'], "Channel 1", True)['channel_id']
    assert channel_join_req("", chan_id)['code'] == AccessError.code

def test_channel_join_channel_channel_id_empty(Channel_setup):
    u1, u2, u3, chan1_id, chan2_id = Channel_setup
    assert channel_join_req(u1['token'], "")['code'] == InputError.code
    assert channel_join_req(u2['token'], "")['code'] == InputError.code
    assert channel_join_req(u3['token'], "")['code'] == InputError.code

def test_channel_join_global_user_joins_private(default_setup):
    u1, u2, u3 = default_setup
    
    chan1_id = channels_create_req(u2['token'], "Channel 1", False)['channel_id']
    chan2_id = channels_create_req(u3['token'], "Channel 1", False)['channel_id']
    channel_join_req(u1['token'], chan1_id)
    channel_join_req(u1['token'], chan2_id)

def test_channel_join_all_invalid():
    clear_req()
    assert channel_join_req("", "")['code'] == AccessError.code

# The following tests are for channel_details iteration 1
def test_channel_details_valid_channel(Channel_setup):
    u1, u2, u3, chan1_id, chan2_id = Channel_setup
    channel_join_req(u3['token'], chan1_id)
    channel_join_req(u3['token'], chan2_id)
    assert channel_details_req(u1['token'], chan1_id) == {'name' : 'Channel 1','is_public' : True,'owner_members' : [{'email': 'patrick.liang@unsw.com', 'handle_str': 'patrickliang', 'name_first': 'Patrick', 'name_last': 'Liang', 'u_id': u1['auth_user_id']}],'all_members' : [{'email': 'patrick.liang@unsw.com', 'handle_str': 'patrickliang', 'name_first': 'Patrick', 'name_last': 'Liang', 'u_id': u1['auth_user_id']}, {'email': 'john.doe@unsw.com', 'handle_str': 'johndoe', 'name_first': 'John', 'name_last': 'Doe', 'u_id': u3['auth_user_id']}],
    }
    assert channel_details_req(u2['token'], chan2_id) == {
        'name' : 'Channel 2',
        'is_public' : True,
        'owner_members' : [{'email': 'john.citizen@unsw.com', 'handle_str': 'johncitizen', 'name_first': 'John', 'name_last': 'Citizen', 'u_id': u2['auth_user_id']}],
        'all_members' : [{'email': 'john.citizen@unsw.com', 'handle_str': 'johncitizen', 'name_first': 'John', 'name_last': 'Citizen', 'u_id': u2['auth_user_id']}, {'email': 'john.doe@unsw.com', 'handle_str': 'johndoe', 'name_first': 'John', 'name_last': 'Doe', 'u_id': u3['auth_user_id']}],
    }

def test_channel_details_valid_private_channel(default_setup):
    u1, u2, u3 = default_setup
    chan1_id = channels_create_req(u1['token'], "Channel 1", False)['channel_id']
    chan2_id = channels_create_req(u2['token'], "Channel 2", False)['channel_id']
    channel_invite_req(u2['token'], chan2_id, u3['auth_user_id'])
    channel_invite_req(u1['token'], chan1_id, u3['auth_user_id'])
    
    assert channel_details_req(u1['token'], chan1_id) == {'name' : 'Channel 1','is_public' : False,'owner_members' : [{'email': 'patrick.liang@unsw.com', 'handle_str': 'patrickliang', 'name_first': 'Patrick', 'name_last': 'Liang', 'u_id': u1['auth_user_id']}],'all_members' : [{'email': 'patrick.liang@unsw.com', 'handle_str': 'patrickliang', 'name_first': 'Patrick', 'name_last': 'Liang', 'u_id': u1['auth_user_id']}, {'email': 'john.doe@unsw.com', 'handle_str': 'johndoe', 'name_first': 'John', 'name_last': 'Doe', 'u_id': u3['auth_user_id']}],
    }
    assert channel_details_req(u2['token'], chan2_id) == {
        'name' : 'Channel 2',
        'is_public' : False,
        'owner_members' : [{'email': 'john.citizen@unsw.com', 'handle_str': 'johncitizen', 'name_first': 'John', 'name_last': 'Citizen', 'u_id': u2['auth_user_id']}],
        'all_members' : [{'email': 'john.citizen@unsw.com', 'handle_str': 'johncitizen', 'name_first': 'John', 'name_last': 'Citizen', 'u_id': u2['auth_user_id']}, {'email': 'john.doe@unsw.com', 'handle_str': 'johndoe', 'name_first': 'John', 'name_last': 'Doe', 'u_id': u3['auth_user_id']}],
    }
    
def test_channel_details_non_existant_channel(default_setup):
    u1, u2, u3= default_setup
    channels_create_req(u1['token'], "Channel 1", False)['channel_id']
    assert channel_details_req(u1['token'], 33)['code'] == InputError.code

def test_channel_details_not_in_channel(Channel_setup):
    u1, u2, u3, chan1_id, chan2_id = Channel_setup
    assert channel_details_req(u1['token'], chan2_id)['code'] == AccessError.code
    assert channel_details_req(u2['token'], chan1_id)['code'] == AccessError.code
    assert channel_details_req(u3['token'], chan1_id)['code'] == AccessError.code

def test_channel_details_user_id_invalid():
    clear_req()
    u1 = auth_register_req("patrick.liang@unsw.com", "katrick", "Patrick", "Liang")
    chan1_id = channels_create_req(u1['token'], "Channel 1", True)['channel_id']
    
    assert channel_details_req("", chan1_id)['code'] == AccessError.code

# The following tests are for channel_messages
def test_channel_messages_invalid_channel():
    clear_req()
    u1 = auth_register_req("patrick.liang@unsw.com", "katrick", "Patrick", "Liang")
    assert channel_messages_req(u1['token'], 33, 0)['code'] == InputError.code

def test_channel_mesg_srt_too_long(default_setup):
    u1, u2, u3 = default_setup
    chan_id = channels_create_req(u1['token'], "Channel 1", True)['channel_id']
    channel_join_req(u2['token'], chan_id)
    channel_join_req(u3['token'], chan_id)
    message_send_req(u1['token'], chan_id, "message")
    message_send_req(u2['token'], chan_id, "message")
    message_send_req(u3['token'], chan_id, "message")
    
    assert channel_messages_req(u1['token'], chan_id, 33)['code'] == InputError.code
    
        
def test_channel_msgs_start_large(default_setup):
    u1, u2, u3 = default_setup
    chan_id = channels_create_req(u1['token'], "Channel 1", True)['channel_id']
    channel_join_req(u2['token'], chan_id)
    channel_join_req(u3['token'], chan_id)
    
    assert channel_messages_req(u1['token'], chan_id, 33)['code'] == InputError.code
        
def test_channel_msgs_start_zero(default_setup):
    u1, u2, u3 = default_setup
    chan_id = channels_create_req(u1['token'], "Channel 1", True)['channel_id']
    channel_join_req(u2['token'], chan_id)
    channel_join_req(u3['token'], chan_id)
    channel_messages_req(u1['token'], chan_id, 0)
    channel_messages_req(u2['token'], chan_id, 0)
    channel_messages_req(u3['token'], chan_id, 0)
        
def test_channel_messages_start_negative(default_setup):
    u1, u2, u3 = default_setup
    chan_id = channels_create_req(u1['token'], "Channel 1", True)['channel_id']
    channel_join_req(u2['token'], chan_id)
    channel_join_req(u3['token'], chan_id)
    assert channel_messages_req(u1['token'], chan_id, -3)['code'] == InputError.code
    assert channel_messages_req(u2['token'], chan_id, -3)['code'] == InputError.code
    assert channel_messages_req(u3['token'], chan_id, -3)['code'] == InputError.code

def test_channel_messages_user_not_member(Channel_setup_one):
    u1, u2, u3, chan_id = Channel_setup_one
    assert channel_messages_req(u2['token'], chan_id, 0)['code'] == AccessError.code
    assert channel_messages_req(u3['token'], chan_id, 0)['code'] == AccessError.code

def test_channel_messages_invalid_user():
    clear_req()
    u1 = auth_register_req("patrick.liang@unsw.com", "katrick", "Patrick", "Liang")
    chan_id = channels_create_req(u1['token'], "Channel 1", True)['channel_id']
    assert channel_messages_req(44, chan_id, 0)['code'] == AccessError.code
        
def test_channel_messages_valid(Channel_setup_one):
    u1, u2, u3, chan_id = Channel_setup_one
    channel_join_req(u2['token'], chan_id)
    channel_join_req(u3['token'], chan_id)
    message_send_req(u1['token'], chan_id, "message")
    message_send_req(u2['token'], chan_id, "message")
    message_send_req(u3['token'], chan_id, "message")
    
    channel_messages_req(u1['token'], chan_id, 0)
    
def test_channel_messages_valid_over_50_messages(Channel_setup_one):
    u1, u2, u3, chan_id = Channel_setup_one
    channel_join_req(u2['token'], chan_id)
    channel_join_req(u3['token'], chan_id)
    message_send_req(u1['token'], chan_id, "message")
    message_send_req(u2['token'], chan_id, "message")
    message_send_req(u3['token'], chan_id, "message")
    message_send_req(u1['token'], chan_id, "message")
    message_send_req(u2['token'], chan_id, "message")
    message_send_req(u3['token'], chan_id, "message")
    message_send_req(u1['token'], chan_id, "message")
    message_send_req(u2['token'], chan_id, "message")
    message_send_req(u3['token'], chan_id, "message")
    message_send_req(u1['token'], chan_id, "message")
    message_send_req(u2['token'], chan_id, "message")
    message_send_req(u3['token'], chan_id, "message")
    message_send_req(u1['token'], chan_id, "message")
    message_send_req(u2['token'], chan_id, "message")
    message_send_req(u3['token'], chan_id, "message")
    message_send_req(u1['token'], chan_id, "message")
    message_send_req(u2['token'], chan_id, "message")
    message_send_req(u3['token'], chan_id, "message")
    message_send_req(u1['token'], chan_id, "message")
    message_send_req(u2['token'], chan_id, "message")
    message_send_req(u3['token'], chan_id, "message")
    message_send_req(u1['token'], chan_id, "message")
    message_send_req(u2['token'], chan_id, "message")
    message_send_req(u3['token'], chan_id, "message")
    message_send_req(u1['token'], chan_id, "message")
    message_send_req(u2['token'], chan_id, "message")
    message_send_req(u3['token'], chan_id, "message")
    message_send_req(u1['token'], chan_id, "message")
    message_send_req(u2['token'], chan_id, "message")
    message_send_req(u3['token'], chan_id, "message")
    message_send_req(u1['token'], chan_id, "message")
    message_send_req(u2['token'], chan_id, "message")
    message_send_req(u3['token'], chan_id, "message")
    message_send_req(u1['token'], chan_id, "message")
    message_send_req(u2['token'], chan_id, "message")
    message_send_req(u3['token'], chan_id, "message")
    message_send_req(u1['token'], chan_id, "message")
    message_send_req(u2['token'], chan_id, "message")
    message_send_req(u3['token'], chan_id, "message")
    message_send_req(u1['token'], chan_id, "message")
    message_send_req(u2['token'], chan_id, "message")
    message_send_req(u3['token'], chan_id, "message")
    message_send_req(u1['token'], chan_id, "message")
    message_send_req(u2['token'], chan_id, "message")
    message_send_req(u3['token'], chan_id, "message")
    message_send_req(u1['token'], chan_id, "message")
    message_send_req(u2['token'], chan_id, "message")
    message_send_req(u3['token'], chan_id, "message")
    message_send_req(u1['token'], chan_id, "message")
    message_send_req(u2['token'], chan_id, "message")
    message_send_req(u3['token'], chan_id, "message")
    message_send_req(u1['token'], chan_id, "message")
    message_send_req(u2['token'], chan_id, "message")
    message_send_req(u3['token'], chan_id, "message")
    
    channel_messages_req(u1['token'], chan_id, 0)

# the following tests are for channel_addowner
def test_channel_addowner_channel_invalid(Channel_setup_one):
    u1, u2, u3, chan_id = Channel_setup_one
    assert channel_addowner_req(u1['token'], 4, u2['auth_user_id'])['code'] == InputError.code
    assert channel_addowner_req(u1['token'], 4, u3['auth_user_id'])['code'] == InputError.code

def test_channel_addowner_user_invalid():
    clear_req()
    u1 = auth_register_req("patrick.liang@unsw.com", "katrick", "Patrick", "Liang")
    chan_id = channels_create_req(u1['token'], "Channel 1", True)['channel_id']
    assert channel_addowner_req(u1['token'], chan_id, 44)['code'] == InputError.code

def test_channel_addowner_user_not_member(Channel_setup_one):
    u1, u2, u3, chan_id = Channel_setup_one
    assert channel_addowner_req(u1['token'], chan_id, u2['auth_user_id'])['code'] == InputError.code
    assert channel_addowner_req(u1['token'], chan_id, u3['auth_user_id'])['code'] == InputError.code

def test_channel_addowner_user_valid_then_user_already_owner(Channel_setup_one):
    u1, u2, u3, chan_id = Channel_setup_one
    channel_join_req(u2['token'], chan_id)
    channel_join_req(u3['token'], chan_id)
    channel_addowner_req(u1['token'], chan_id, u2['auth_user_id'])
    channel_addowner_req(u1['token'], chan_id, u3['auth_user_id'])
    assert channel_addowner_req(u1['token'], chan_id, u2['auth_user_id'])['code'] == InputError.code
    assert channel_addowner_req(u1['token'], chan_id, u3['auth_user_id'])['code'] == InputError.code
    
def test_channel_addowner_token_not_member(Channel_setup_one):
    u1, u2, u3, chan_id = Channel_setup_one
    channel_join_req(u3['token'], chan_id)
    assert channel_addowner_req(u2['token'], chan_id, u3['auth_user_id'])['code'] == AccessError.code)
        
def test_channel_addowner_token_not_existant(Channel_setup_one):
    u1, u2, u3, chan_id = Channel_setup_one
    channel_join_req(u3['token'], chan_id)
    auth_logout_req(u1['token'])
    assert channel_addowner_req(u1['token'], chan_id, u3['auth_user_id'])['code'] == AccessError.code

def test_channel_addowner_token_not_owner(Channel_setup_one):
    u1, u2, u3, chan_id = Channel_setup_one
    channel_join_req(u2['token'], chan_id)
    channel_join_req(u3['token'], chan_id)
    assert channel_addowner_req(u2['token'], chan_id, u3['auth_user_id'])['code'] == AccessError.code
        
def test_channel_addowner_global_owner_adding(default_setup):
    u1, u2, u3 = default_setup
    chan_id = channels_create_req(u2['token'], "Channel 1", True)['channel_id']
    channel_join_req(u3['token'], chan_id)
    channel_addowner_req(u1['token'], chan_id, u3['auth_user_id'])
    
def test_channel_addowner_global_owner_being_added(default_setup):
    u1, u2, u3 = default_setup
    chan_id = channels_create_req(u2['token'], "Channel 1", True)['channel_id']
    channel_join_req(u3['token'], chan_id)
    channel_join_req(u1['token'], chan_id)
    channel_addowner_req(u2['token'], chan_id, u1['auth_user_id'])

# the following tests are for channel_removeowner
        
def test_channel_removeowner_channel_invalid(default_setup):
    u1, u2, u3 = default_setup
    channels_create_req(u1['token'], "Channel 1", True)
    assert channel_removeowner_req(u1['token'], 33, u3['auth_user_id'])['code'] == InputError.code
    assert channel_removeowner_req(u1['token'], 33, u2['auth_user_id'])['code'] == InputError.code
        
def test_channel_removeowner_user_not_owner(Channel_setup_one):
    u1, u2, u3, chan_id = Channel_setup_one
    channel_join_req(u2['token'], chan_id)
    assert channel_removeowner_req(u2['token'], chan_id, u1['auth_user_id'])['code'] == AccessError.code

def test_channel_removeowner_user_invalid(Channel_setup_one):
    u1, u2, u3, chan_id = Channel_setup_one
    channel_join_req(u2['token'], chan_id)
    channel_join_req(u3['token'], chan_id)
    assert channel_removeowner_req(u1['token'], chan_id, 99)['code'] == InputError.code

def test_channel_removeowner_user_not_member(Channel_setup_one):
    u1, u2, u3, chan_id = Channel_setup_one
    
    assert channel_removeowner_req(u1['token'], chan_id, u2['token'])['code'] == InputError.code
    assert channel_removeowner_req(u1['token'], chan_id, u3['token'])['code'] == InputError.code

def test_channel_removeowner_user_valid_then_user_not_owner(Channel_setup_one):
    u1, u2, u3, chan_id = Channel_setup_one
    channel_join_req(u2['token'], chan_id)
    channel_join_req(u3['token'], chan_id)
    channel_addowner_req(u1['token'], chan_id, u2['auth_user_id'])
    channel_removeowner_req(u1['token'], chan_id, u2['auth_user_id'])
    assert channel_removeowner_req(u1['token'], chan_id, u2['auth_user_id'])['code'] == InputError.code

def test_channel_removeowner_token_not_member(default_setup):
    u1, u2, u3  = default_setup
    chan_id = channels_create_req(u2['token'], "Channel 1", True)['channel_id']
    channel_join_req(u1['token'], chan_id)
    assert channel_removeowner_req(u3['token'], chan_id, u2['auth_user_id'])['code'] == AccessError.code
        
def test_channel_removeowner_token_not_existant(Channel_setup_one):
    u1, u2, u3, chan_id = Channel_setup_one
    channel_join_req(u2['token'], chan_id)
    channel_join_req(u3['token'], chan_id)
    channel_addowner_req(u1['token'], chan_id, u2['auth_user_id'])
    auth_logout_req(u1['token'])
    assert channel_removeowner_req(u1['token'], chan_id, u2['auth_user_id'])['code'] == AccessError.code     

def test_channel_removeowner_token_not_owner(default_setup):
    u1, u2, u3 = default_setup
    chan_id = channels_create_req(u1['token'], "Channel 1", True)['channel_id']
    channel_join_req(u2['token'], chan_id)
    channel_join_req(u3['token'], chan_id)
    assert channel_removeowner_req(u2['token'], chan_id, u1['auth_user_id'])['code'] == AccessError.code

def test_channel_removeowner_user_only_owner():
    clear_req()
    u1 = auth_register_req("patrick.liang@unsw.com", "katrick", "Patrick", "Liang")
    chan_id = channels_create_req(u1['token'], "Channel 1", True)['channel_id']
    assert channel_removeowner_req(u1['token'], chan_id, u1['auth_user_id'])['code'] == InputError.code


def test_channel_removeowner_token_not_member_valid(Channel_setup_one):
    u1, u2, u3, chan_id = Channel_setup_one
    channel_join_req(u2['token'], chan_id)
    channel_join_req(u3['token'], chan_id)
    channel_addowner_req(u1['token'], chan_id, u2['auth_user_id'])
    channel_removeowner_req(u1['token'], chan_id, u1['auth_user_id'])

# Tests for channel_leave
def test_channel_leave_not_member(Channel_setup_one):
    u1, u2, u3, chan_id = Channel_setup_one
    assert channel_leave_req(u2['token'], chan_id)['code'] == AccessError.code
    assert channel_leave_req(u3['token'], chan_id)['code'] == AccessError.code

def test_channel_leave_empty_token():
    clear_req()
    u1 = auth_register_req("patrick.liang@unsw.com", "katrick", "Patrick", "Liang")
    chan_id = channels_create_req(u1['token'], "Channel 1", True)['channel_id']
    assert channel_leave_req("", chan_id)['code'] == AccessError.code
           
def test_channel_leave_non_existant_token():
    clear_req()
    u1 = auth_register_req("patrick.liang@unsw.com", "katrick", "Patrick", "Liang")
    chan_id = channels_create_req(u1['token'], "Channel 1", True)['channel_id']
    auth_logout_req(u1['token'])
    assert channel_leave_req(u1['token'], chan_id)['code'] == AccessError.code

def test_channel_leave_invalid_channel_id(default_setup):
    u1, u2, u3 = default_setup
    chan_id = channels_create_req(u1['token'], "Channel 1", True)
    channel_join_req(u2['token'], chan_id)
    channel_join_req(u3['token'], chan_id)
    assert channel_leave_req(u2['token'], 33)['code'] == InputError.code
    assert channel_leave_req(u3['token'], 33)['code'] == InputError.code

def test_channel_leave_valid_token_and_channel(Channel_setup_one):
    u1, u2, u3, chan_id = Channel_setup_one
    channel_join_req(u2['token'], chan_id)
    channel_join_req(u3['token'], chan_id)
    channel_leave_req(u2['token'], chan_id)
    channel_leave_req(u3['token'], chan_id)
    assert channel_details_req(u1['token'], chan_id) == {
        'name' : 'Channel 1',
        'is_public' : True,
        'owner_members' : [{'email': 'patrick.liang@unsw.com', 'handle_str': 'patrickliang', 'name_first': 'Patrick', 'name_last': 'Liang', 'u_id': u1['auth_user_id']}],
        'all_members' : [{'email': 'patrick.liang@unsw.com', 'handle_str': 'patrickliang', 'name_first': 'Patrick', 'name_last': 'Liang', 'u_id': u1['auth_user_id']}],
    }
    
def test_channel_owner_leaves_valid_token_and_channel(Channel_setup_one):
    u1, u2, u3, chan_id = Channel_setup_one
    channel_join_req(u2['token'], chan_id)
    channel_join_req(u3['token'], chan_id)
    channel_leave_req(u3['token'], chan_id)
    channel_leave_req(u1['token'], chan_id)
    assert channel_details_req(u2['token'], chan_id) == {
        'name' : 'Channel 1',
        'is_public' : True,
        'owner_members' : [],
        'all_members' : [{'email': 'john.citizen@unsw.com', 'handle_str': 'johncitizen', 'name_first': 'John', 'name_last': 'Citizen', 'u_id': u2['auth_user_id']}],
    }
    