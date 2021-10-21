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
    chan1_id = channels_create_req(u1_tok, "Channel 1", True)
    chan2_id = channels_create_req(u2_tok, "Channel 2", True)
    return (u1, u2, u3, chan1_id, chan2_id)


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

def test_channel_invite_auth_not_in_channel():
    clear_v1()
    user1_token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    user2_token = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['token']
    user3_token = auth_register_v1("john.green@aunsw.edu.au", "codeword", "John", "Green")['token']
    channel1_id = channels_create_v1(user1_token, "Channel 1", True)['channel_id']
    with pytest.raises(AccessError):
        channel_invite_v1(user2_token, channel1_id, get_u_id(user3_token))

def test_channel_invite_valid():
    clear_v1()
    user1_token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    user2_token = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['token']
    channel1_id = channels_create_v1(user1_token, "Channel 1", True)['channel_id']
    channel_invite_v1(user1_token, channel1_id, get_u_id(user2_token))

def test_channel_invite_channel_id_empty():
    clear_v1()
    user1_token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    user2_token = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['token']
    channels_create_v1(user1_token, "Channel 1", True)['channel_id']
    with pytest.raises(InputError):
        channel_invite_v1(user1_token, "", get_u_id(user2_token))

def test_channel_invite_user_id_empty():
    clear_v1()
    user1_token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    channel1_id = channels_create_v1(user1_token, "Channel 1", True)['channel_id']
    with pytest.raises(InputError):
        channel_invite_v1(user1_token, channel1_id, "")

def test_channel_invite_no_channels():
    clear_v1()
    user1_token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    user2_token = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['token']
    with pytest.raises(InputError):
        channel_invite_v1(user1_token, 1, get_u_id(user2_token))

def test_channel_invite_auth_id_invalid():
    clear_v1()
    user1_token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    channel1_id = channels_create_v1(user1_token, "Channel 1", True)['channel_id']
    with pytest.raises(AccessError):
        channel_invite_v1("", channel1_id, get_u_id(user1_token))

def test_channel_invite_user_invites_self():
    clear_v1()
    user1_token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    channel1_id = channels_create_v1(user1_token, "Channel 1", True)['channel_id']
    with pytest.raises(InputError):
        channel_invite_v1(user1_token, channel1_id, get_u_id(user1_token))

def test_channel_invite_all_invalid():
    clear_v1()
    with pytest.raises(AccessError):
        channel_invite_v1("", "", "")

# The following tests are for channel_join
def test_channel_join_public_channel():
    clear_v1()
    user1_token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    user2_token = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['token']
    channel_id = channels_create_v1(user1_token, "Channel 1", True)['channel_id']
    assert channel_join_v1(user2_token, channel_id) == {}

def test_channel_join_channel_user_aready_in():
    clear_v1()
    user_token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    channel_id = channels_create_v1(user_token, "Channel 1", True)['channel_id']
    with pytest.raises(InputError):
        channel_join_v1(user_token, channel_id)


def test_channel_join_channel_private():
    clear_v1()
    user1_token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    user2_token = auth_register_v1("john.smith@aunsw.edu.au","password","John","Smith")['token']
    channel_id = channels_create_v1(user1_token, "Channel 1", False)['channel_id']
    with pytest.raises(AccessError):
        channel_join_v1(user2_token, channel_id)


def test_channel_join_channel_user_aready_in_private():
    clear_v1()
    auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    user2_token = auth_register_v1("john.smith@aunsw.edu.au","password","John","Smith")['token']
    channel_id = channels_create_v1(user2_token, "Channel 1", False)['channel_id']
    with pytest.raises(InputError):
        channel_join_v1(user2_token, channel_id)


def test_channel_join_channel_user_does_not_exist():
    clear_v1()
    user_token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    channel_id = channels_create_v1(user_token, "Channel 1", True)['channel_id']
    with pytest.raises(AccessError):
        channel_join_v1(4, channel_id)

def test_channel_join_channel_channel_does_not_exist():
    clear_v1()
    user_token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    with pytest.raises(InputError):
        channel_join_v1(user_token, 3333)

def test_channel_join_channel_user_token_empty():
    clear_v1()
    user_token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    channel_id = channels_create_v1(user_token, "Channel 1", True)['channel_id']
    with pytest.raises(AccessError):
        channel_join_v1("", channel_id)

def test_channel_join_channel_channel_id_empty():
    clear_v1()
    user_token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    channels_create_v1(user_token, "Channel 1", True)['channel_id']
    with pytest.raises(InputError):
        channel_join_v1(user_token, "")

def test_channel_join_global_user_joins_private():
    clear_v1()
    user1_token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    user2_token = auth_register_v1("john.smith@aunsw.edu.au","password","John","Smith")['token']
    channel_id = channels_create_v1(user2_token, "Channel 1", False)['channel_id']
    channel_join_v1(user1_token, channel_id)

def test_channel_join_all_invalid():
    clear_v1()
    with pytest.raises(AccessError):
        channel_join_v1("", "")

# The following tests are for channel_details iteration 1

def test_channel_details_valid_channel():
    clear_v1()
    user1_token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    user2_token = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['token']
    channel_id = channels_create_v1(user1_token, "Channel 1", True)['channel_id']
    channel_join_v1(user2_token, channel_id)
    assert (channel_details_v1(user1_token, channel_id) == {
        'name' : 'Channel 1',
        'is_public' : True,
        'owner_members' : [{'email': 'john.doe@aunsw.edu.au', 'handle_str': 'johndoe', 'name_first': 'John', 'name_last': 'Doe', 'u_id': get_u_id(user1_token)}],
        'all_members' : [{'email': 'john.doe@aunsw.edu.au', 'handle_str': 'johndoe', 'name_first': 'John', 'name_last': 'Doe', 'u_id': get_u_id(user1_token)}, {'email': 'john.smith@aunsw.edu.au', 'handle_str': 'johnsmith', 'name_first': 'John', 'name_last': 'Smith', 'u_id': get_u_id(user2_token)}],
    })

def test_channel_details_valid_private_channel():
    clear_v1()
    user1_token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    channel_id = channels_create_v1(user1_token, "Channel 1", False)['channel_id']
    assert (channel_details_v1(user1_token, channel_id) == {
        'name' : 'Channel 1',
        'is_public' : False,
        'owner_members' : [{'email': 'john.doe@aunsw.edu.au', 'handle_str': 'johndoe', 'name_first': 'John', 'name_last': 'Doe', 'u_id': get_u_id(user1_token)}],
        'all_members' : [{'email': 'john.doe@aunsw.edu.au', 'handle_str': 'johndoe', 'name_first': 'John', 'name_last': 'Doe', 'u_id': get_u_id(user1_token)}],
    })
    
def test_channel_details_non_existant_channel():
    clear_v1()
    user_token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    channels_create_v1(user_token, "channel1", True)
    with pytest.raises(InputError):
        channel_details_v1(user_token, 33)

def test_channel_details_not_in_channel():
    clear_v1()
    user1_token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    user2_token = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['token']
    channel_id = channels_create_v1(user1_token, "Channel 1", True)['channel_id']
    with pytest.raises(AccessError):
        channel_details_v1(user2_token, channel_id)

def test_channel_details_user_id_invalid():
    clear_v1()
    user1_token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    channel_id = channels_create_v1(user1_token, "Channel 1", True)['channel_id']
    with pytest.raises(AccessError):
        channel_details_v1("", channel_id)

def test_channel_details_channel_id_invalid():
    clear_v1()
    user1_token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    with pytest.raises(InputError):
        channel_details_v1(user1_token, "")

def test_channel_details_user_id_and_channel_id_invalid():
    clear_v1()
    user1_token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    channels_create_v1(user1_token, "Channel 1", True)['channel_id']
    with pytest.raises(AccessError):
        channel_details_v1("", "")

def test_channel_details_all_invalid():
    clear_v1()
    with pytest.raises(AccessError):
        channel_details_v1("", "")

# The following tests are for channel_messages
def test_channel_messages_invalid_channel():
    clear_v1()
    user_token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    with pytest.raises(InputError):
        channel_messages_v1(user_token, 33, 0)

# def test_channel_mesg_srt_too_long():
#     clear_v1()
#     user_token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
#     channel_id = channels_create_v1(user_token, "Channel 1", True)['channel_id']
#     message_send_v1(user_token, channel_id, "Hey there")
#     with pytest.raises(InputError):
#         channel_messages_v1(user_token, channel_id, 33)
    
        
def test_channel_msgs_start_large():
    clear_v1()
    user_token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    channel_id = channels_create_v1(user_token, "Channel 1", True)['channel_id']
    with pytest.raises(InputError):
        channel_messages_v1(user_token, channel_id, 33)
        
def test_channel_msgs_start_zero():
    clear_v1()
    user_token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    channel_id = channels_create_v1(user_token, "Channel 1", True)['channel_id']
    channel_messages_v1(user_token, channel_id, 0)
        
def test_channel_messages_start_negative():
    clear_v1()
    user_token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    channel_id = channels_create_v1(user_token, "Channel 1", True)['channel_id']
    with pytest.raises(InputError):
        channel_messages_v1(user_token, channel_id, -3)

def test_channel_messages_user_not_member():
    clear_v1()
    user1_token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    user2_token = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['token']
    channel_id = channels_create_v1(user1_token, "Channel 1", True)['channel_id']
    with pytest.raises(AccessError):
        channel_messages_v1(user2_token, channel_id, 0)

def test_channel_messages_no_channel_id():
    clear_v1()
    user1_token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    user2_token = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['token']
    channels_create_v1(user1_token, "Channel 1", True)['channel_id']
    with pytest.raises(InputError):
        channel_messages_v1(user2_token, "", 0)

def test_channel_messages_start_empty():
    clear_v1()
    user1_token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    user2_token = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['token']
    channel_id = channels_create_v1(user1_token, "Channel 1", True)['channel_id']
    with pytest.raises(AccessError):
        channel_messages_v1(user2_token, channel_id, "")

def test_channel_messages_invalid_user():
    clear_v1()
    user1_token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    channel_id = channels_create_v1(user1_token, "Channel 1", True)['channel_id']
    with pytest.raises(AccessError):
        channel_messages_v1(2, channel_id, 0)

def test_channel_messages_all_invalid():
    clear_v1()
    with pytest.raises(AccessError):
        channel_messages_v1("", "", 0)
        
def test_channel_messages_valid():
    clear_v1()
    user1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")
    user1_token = user1['token']
    # user1_id = user1['auth_user_id']
    # user2_token = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['token']
    chan_id = channels_create_v1(user1_token, "Channel 1", True)['channel_id']
    message_send_v1(user1_token, chan_id, "oogoa booga")
    message_send_v1(user1_token, chan_id, "Hi there")
    message_send_v1(user1_token, chan_id, "#@$%^RT&Y*UIOJNK")
    channel_messages_v1(user1_token, chan_id, 0)
    # assert channel_messages_v1(user1_token, chan_id, 1) == {
    #     'messages': [{'message_id' : msg1, 'u_id' : user1_id, 'message' : "oogoa booga", 'time_created' : timestamp}],
    #     'start': 1,
    #     'end': 3,  
    # }
    
def test_channel_messages_valid_over_50_messages():
    clear_v1()
    user1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")
    user1_token = user1['token']
    # user1_id = user1['auth_user_id']
    # user2_token = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['token']
    chan_id = channels_create_v1(user1_token, "Channel 1", True)['channel_id']
    message_send_v1(user1_token, chan_id, "oogoa booga")
    message_send_v1(user1_token, chan_id, "Hi there")
    message_send_v1(user1_token, chan_id, "#@$%^RT&Y*UIOJNK")
    message_send_v1(user1_token, chan_id, "oogoa booga")
    message_send_v1(user1_token, chan_id, "Hi there")
    message_send_v1(user1_token, chan_id, "#@$%^RT&Y*UIOJNK")
    message_send_v1(user1_token, chan_id, "oogoa booga")
    message_send_v1(user1_token, chan_id, "Hi there")
    message_send_v1(user1_token, chan_id, "#@$%^RT&Y*UIOJNK")
    message_send_v1(user1_token, chan_id, "oogoa booga")
    message_send_v1(user1_token, chan_id, "Hi there")
    message_send_v1(user1_token, chan_id, "#@$%^RT&Y*UIOJNK")
    message_send_v1(user1_token, chan_id, "oogoa booga")
    message_send_v1(user1_token, chan_id, "Hi there")
    message_send_v1(user1_token, chan_id, "#@$%^RT&Y*UIOJNK")
    message_send_v1(user1_token, chan_id, "oogoa booga")
    message_send_v1(user1_token, chan_id, "Hi there")
    message_send_v1(user1_token, chan_id, "#@$%^RT&Y*UIOJNK")
    message_send_v1(user1_token, chan_id, "oogoa booga")
    message_send_v1(user1_token, chan_id, "Hi there")
    message_send_v1(user1_token, chan_id, "#@$%^RT&Y*UIOJNK")
    message_send_v1(user1_token, chan_id, "oogoa booga")
    message_send_v1(user1_token, chan_id, "Hi there")
    message_send_v1(user1_token, chan_id, "#@$%^RT&Y*UIOJNK")
    message_send_v1(user1_token, chan_id, "oogoa booga")
    message_send_v1(user1_token, chan_id, "Hi there")
    message_send_v1(user1_token, chan_id, "#@$%^RT&Y*UIOJNK")
    message_send_v1(user1_token, chan_id, "oogoa booga")
    message_send_v1(user1_token, chan_id, "Hi there")
    message_send_v1(user1_token, chan_id, "#@$%^RT&Y*UIOJNK")
    message_send_v1(user1_token, chan_id, "oogoa booga")
    message_send_v1(user1_token, chan_id, "Hi there")
    message_send_v1(user1_token, chan_id, "#@$%^RT&Y*UIOJNK")
    message_send_v1(user1_token, chan_id, "oogoa booga")
    message_send_v1(user1_token, chan_id, "Hi there")
    message_send_v1(user1_token, chan_id, "#@$%^RT&Y*UIOJNK")
    message_send_v1(user1_token, chan_id, "oogoa booga")
    message_send_v1(user1_token, chan_id, "Hi there")
    message_send_v1(user1_token, chan_id, "#@$%^RT&Y*UIOJNK")
    message_send_v1(user1_token, chan_id, "oogoa booga")
    message_send_v1(user1_token, chan_id, "Hi there")
    message_send_v1(user1_token, chan_id, "#@$%^RT&Y*UIOJNK")
    message_send_v1(user1_token, chan_id, "oogoa booga")
    message_send_v1(user1_token, chan_id, "Hi there")
    message_send_v1(user1_token, chan_id, "#@$%^RT&Y*UIOJNK")
    message_send_v1(user1_token, chan_id, "oogoa booga")
    message_send_v1(user1_token, chan_id, "Hi there")
    message_send_v1(user1_token, chan_id, "#@$%^RT&Y*UIOJNK")
    message_send_v1(user1_token, chan_id, "oogoa booga")
    message_send_v1(user1_token, chan_id, "Hi there")
    message_send_v1(user1_token, chan_id, "#@$%^RT&Y*UIOJNK")
    message_send_v1(user1_token, chan_id, "oogoa booga")
    message_send_v1(user1_token, chan_id, "Hi there")
    message_send_v1(user1_token, chan_id, "#@$%^RT&Y*UIOJNK")
    message_send_v1(user1_token, chan_id, "oogoa booga")
    message_send_v1(user1_token, chan_id, "Hi there")
    message_send_v1(user1_token, chan_id, "#@$%^RT&Y*UIOJNK")
    message_send_v1(user1_token, chan_id, "oogoa booga")
    message_send_v1(user1_token, chan_id, "Hi there")
    message_send_v1(user1_token, chan_id, "#@$%^RT&Y*UIOJNK")
    message_send_v1(user1_token, chan_id, "oogoa booga")
    message_send_v1(user1_token, chan_id, "Hi there")
    message_send_v1(user1_token, chan_id, "#@$%^RT&Y*UIOJNK")
    message_send_v1(user1_token, chan_id, "oogoa booga")
    message_send_v1(user1_token, chan_id, "Hi there")
    message_send_v1(user1_token, chan_id, "#@$%^RT&Y*UIOJNK")
    message_send_v1(user1_token, chan_id, "oogoa booga")
    message_send_v1(user1_token, chan_id, "Hi there")
    message_send_v1(user1_token, chan_id, "#@$%^RT&Y*UIOJNK")
    message_send_v1(user1_token, chan_id, "oogoa booga")
    message_send_v1(user1_token, chan_id, "Hi there")
    message_send_v1(user1_token, chan_id, "#@$%^RT&Y*UIOJNK")
    channel_messages_v1(user1_token, chan_id, 0)

# the following tests are for channel_addowner
def test_channel_addowner_channel_invalid():
    clear_v1()
    token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    user_id = auth_register_v1("jade.lee@aunsw.edu.au","password","Jade","Lee")['auth_user_id']
    channels_create_v1(token, "Channel1", True)
    with pytest.raises(InputError):
        channel_add_owner_v1(token, 4, user_id)

def test_channel_addowner_user_invalid():
    clear_v1()
    token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan_id = channels_create_v1(token, "Channel", True)['channel_id']
    with pytest.raises(InputError):
        channel_add_owner_v1(token, chan_id, 33)

def test_channel_addowner_user_not_member():
    clear_v1()
    token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    user_id = auth_register_v1("jade.lee@aunsw.edu.au","password","Jade","Lee")['auth_user_id']
    chan_id = channels_create_v1(token, "Channel", True)['channel_id']
    with pytest.raises(InputError):
        channel_add_owner_v1(token, chan_id, user_id)

def test_channel_addowner_user_valid_then_user_already_owner():
    clear_v1()
    token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    user_data = auth_register_v1("jade.lee@aunsw.edu.au","password","Jade","Lee")
    chan_id = channels_create_v1(token, "Channel", True)['channel_id']
    channel_join_v1(user_data['token'], chan_id)
    assert channel_add_owner_v1(token, chan_id, user_data['auth_user_id']) == {}
    with pytest.raises(InputError):
        channel_add_owner_v1(token, chan_id, user_data['auth_user_id'])

def test_channel_addowner_token_not_member():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    token2 = auth_register_v1("john.lo@aunsw.edu.au","password","John","Lo")['token']
    user_data = auth_register_v1("jade.lee@aunsw.edu.au","password","Jade","Lee")
    chan_id = channels_create_v1(token1, "Channel", True)['channel_id']
    channel_join_v1(user_data['token'], chan_id)
    with pytest.raises(AccessError):
        channel_add_owner_v1(token2, chan_id, user_data['auth_user_id'])
        
def test_channel_addowner_token_not_existant():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    token2 = auth_register_v1("john.lo@aunsw.edu.au","password","John","Lo")['token']
    user_data = auth_register_v1("jade.lee@aunsw.edu.au","password","Jade","Lee")
    chan_id = channels_create_v1(token1, "Channel", True)['channel_id']
    channel_join_v1(user_data['token'], chan_id)
    auth_logout_v1(token2)
    with pytest.raises(AccessError):
        channel_add_owner_v1(token2, chan_id, user_data['auth_user_id'])

def test_channel_addowner_token_not_owner():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    token2 = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['token']
    user_data = auth_register_v1("jade.lee@aunsw.edu.au","password","Jade","Lee")
    chan_id = channels_create_v1(token1, "Channel", True)['channel_id']
    channel_join_v1(user_data['token'], chan_id)
    channel_join_v1(token2, chan_id)
    with pytest.raises(AccessError):
        channel_add_owner_v1(token2, chan_id, user_data['auth_user_id'])
        
def test_channel_addowner_global_owner_adding():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    token2 = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['token']
    user_data = auth_register_v1("jade.lee@aunsw.edu.au","password","Jade","Lee")
    chan_id = channels_create_v1(token2, "Channel", True)['channel_id']
    channel_join_v1(user_data['token'], chan_id)
    channel_add_owner_v1(token1, chan_id, user_data['auth_user_id'])
    
def test_channel_addowner_global_owner_being_added():
    clear_v1()
    user1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")
    token2 = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['token']
    chan_id = channels_create_v1(token2, "Channel", True)['channel_id']
    channel_join_v1(user1['token'], chan_id)
    with pytest.raises(InputError):
        channel_add_owner_v1(token2, chan_id, user1['auth_user_id'])

# the following tests are for channel_removeowner
        
def test_channel_removeowner_channel_invalid():
    clear_v1()
    token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    user_id = auth_register_v1("jade.lee@aunsw.edu.au","password","Jade","Lee")['auth_user_id']
    channels_create_v1(token, "Channel1", True)
    with pytest.raises(InputError):
        channel_remove_owner_v1(token, 22, user_id)
        
def test_channel_removeowner_user_not_owner():
    clear_v1()
    user1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")
    user2 = auth_register_v1("jade.lee@aunsw.edu.au","password","Jade","Lee")
    chan_id = channels_create_v1(user1['token'], "Channel", True)['channel_id']
    channel_join_v1(user2['token'], chan_id)
    with pytest.raises(AccessError):
        channel_remove_owner_v1(user2['token'], chan_id, user1['auth_user_id'])

def test_channel_removeowner_user_invalid():
    clear_v1()
    token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan_id = channels_create_v1(token, "Channel", True)['channel_id']
    with pytest.raises(InputError):
        channel_remove_owner_v1(token, chan_id, 33)

def test_channel_removeowner_user_not_member():
    clear_v1()
    token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    user_id = auth_register_v1("jade.lee@aunsw.edu.au","password","Jade","Lee")['auth_user_id']
    chan_id = channels_create_v1(token, "Channel", True)['channel_id']
    with pytest.raises(InputError):
        channel_remove_owner_v1(token, chan_id, user_id)

def test_channel_removeowner_user_valid_then_user_not_owner():
    clear_v1()
    token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    user_data = auth_register_v1("jade.lee@aunsw.edu.au","password","Jade","Lee")
    chan_id = channels_create_v1(token, "Channel", True)['channel_id']
    channel_join_v1(user_data['token'], chan_id)
    channel_add_owner_v1(token, chan_id, user_data['auth_user_id'])
    assert channel_remove_owner_v1(token, chan_id, user_data['auth_user_id']) == {}
    with pytest.raises(InputError):
        channel_remove_owner_v1(token, chan_id, user_data['auth_user_id'])

def test_channel_removeowner_token_not_member():
    clear_v1()
    token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    user_data = auth_register_v1("jade.lee@aunsw.edu.au","password","Jade","Lee")
    chan_id = channels_create_v1(token, "Channel", True)['channel_id']
    channel_join_v1(user_data['token'], chan_id)
    with pytest.raises(AccessError):
        channel_remove_owner_v1("dc", chan_id, user_data['auth_user_id'])
        
def test_channel_removeowner_token_not_existant():
    clear_v1()
    token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    user_data = auth_register_v1("jade.lee@aunsw.edu.au","password","Jade","Lee")
    chan_id = channels_create_v1(token, "Channel", True)['channel_id']
    channel_join_v1(user_data['token'], chan_id)
    auth_logout_v1(token)
    with pytest.raises(AccessError):
        channel_remove_owner_v1(token, chan_id, user_data['auth_user_id'])
        

def test_channel_removeowner_token_not_owner():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    token2 = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['token']
    user_data = auth_register_v1("jade.lee@aunsw.edu.au","password","Jade","Lee")
    chan_id = channels_create_v1(token1, "Channel", True)['channel_id']
    channel_join_v1(user_data['token'], chan_id)
    channel_add_owner_v1(token1, chan_id, user_data['auth_user_id'])
    with pytest.raises(AccessError):
        channel_remove_owner_v1(token2, chan_id, user_data['auth_user_id'])

def test_channel_removeowner_user_only_owner():
    clear_v1()
    user_data = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")
    chan_id = channels_create_v1(user_data['token'], "Channel", True)['channel_id']
    with pytest.raises(InputError):
        channel_remove_owner_v1(user_data['token'], chan_id, user_data['auth_user_id'])

def test_channel_removeowner_token_not_member_valid():
    clear_v1()
    user1_data = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")
    user2_data = auth_register_v1("jade.lee@aunsw.edu.au","password","Jade","Lee")
    chan_id = channels_create_v1(user1_data['token'], "Channel", True)['channel_id']
    channel_join_v1(user2_data['token'], chan_id)
    channel_add_owner_v1(user1_data['token'], chan_id, user2_data['auth_user_id'])
    assert channel_remove_owner_v1(user1_data['token'], chan_id, user1_data['auth_user_id']) == {}

# Tests for channel_leave
def test_channel_leave_invalid_token():
    clear_v1()
    user1_token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    user2_token = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['token']
    chan_id = channels_create_v1(user1_token, "Channel 1", True)['channel_id']
    with pytest.raises(AccessError):
            channel_leave_v1(user2_token, chan_id)

def test_channel_leave_empty_token():
    clear_v1()
    user1_token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan_id = channels_create_v1(user1_token, "Channel 1", True)['channel_id']
    with pytest.raises(AccessError):
            channel_leave_v1("", chan_id)
            
def test_channel_leave_non_existant_token():
    clear_v1()
    user1_token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan_id = channels_create_v1(user1_token, "Channel 1", True)['channel_id']
    auth_logout_v1(user1_token)
    with pytest.raises(AccessError):
            channel_leave_v1(user1_token, chan_id)

def test_channel_leave_invalid_channel_id():
    clear_v1()
    user1_token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    user2_token = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['token']
    channels_create_v1(user2_token, "Channel 1", True)['channel_id']
    with pytest.raises(InputError):
            channel_leave_v1(user1_token, 33)

def test_channel_leave_empty_channel_id():
    clear_v1()
    user1_token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    channels_create_v1(user1_token, "Channel 1", True)['channel_id']
    with pytest.raises(InputError):
            channel_leave_v1(user1_token, "")

def test_channel_leave_valid_token_and_channel():
    clear_v1()
    user1_token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    user2_token = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['token']
    chan_id = channels_create_v1(user1_token, "Channel 1", True)['channel_id']
    channel_join_v1(user2_token, chan_id)
    channel_leave_v1(user2_token, chan_id)
    assert (channel_details_v1(user1_token, chan_id) == {
        'name' : 'Channel 1',
        'is_public' : True,
        'owner_members' : [{'email': 'john.doe@aunsw.edu.au', 'handle_str': 'johndoe', 'name_first': 'John', 'name_last': 'Doe', 'u_id': get_u_id(user1_token)}],
        'all_members' : [{'email': 'john.doe@aunsw.edu.au', 'handle_str': 'johndoe', 'name_first': 'John', 'name_last': 'Doe', 'u_id': get_u_id(user1_token)}],
    })
    
def test_channel_owner_leaves_valid_token_and_channel():
    clear_v1()
    user1_token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    user2_token = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['token']
    chan_id = channels_create_v1(user1_token, "Channel 1", True)['channel_id']
    channel_join_v1(user2_token, chan_id)
    channel_leave_v1(user1_token, chan_id)
    assert (channel_details_v1(user2_token, chan_id) == {
        'name' : 'Channel 1',
        'is_public' : True,
        'owner_members' : [],
        'all_members' : [{'email': 'john.smith@aunsw.edu.au', 'handle_str': 'johnsmith', 'name_first': 'John', 'name_last': 'Smith', 'u_id': get_u_id(user2_token)}],
    })
    