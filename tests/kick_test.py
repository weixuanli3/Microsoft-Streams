'''Contains tests for kick.py'''
import pytest

from other_functions.kick import channel_kick_v1, dm_kick_v1
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.channel import channel_join_v1, channel_details_v1
from src.dm import dm_create_v1, dm_details_v1
from src.data_store import get_u_id
from src.config import url
from src.error import InputError
from src.error import AccessError
from src.other import clear_v1

# tests for channel_kick_v1
def test_channel_kick_invalid_token():
    clear_v1()
    user1_token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan_id = channels_create_v1(user1_token, "Channel 1", True)['channel_id']
    with pytest.raises(AccessError):
            channel_kick_v1(-1, chan_id, 2)

def test_channel_kick_invalid_channel_id():
    clear_v1()
    user1_token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    channels_create_v1(user1_token, "Channel 1", True)['channel_id']
    with pytest.raises(InputError):
            channel_kick_v1(user1_token, 33, 1)

def test_channel_kick_invalid_user_id():
    clear_v1()
    user1_token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan_id = channels_create_v1(user1_token, "Channel 1", True)['channel_id']
    with pytest.raises(InputError):
            channel_kick_v1(user1_token, chan_id, 0)

def test_channel_kick_token_no_perms():
    clear_v1()
    user1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")
    user2_token = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['token']
    chan_id = channels_create_v1(user1['token'], "Channel 1", True)['channel_id']
    channel_join_v1(user2_token, chan_id)
    with pytest.raises(AccessError):
            channel_kick_v1(user2_token, chan_id, user1['auth_user_id'])

def test_channel_kick_valid():
    clear_v1()
    user1_token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    user2 = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")
    chan_id = channels_create_v1(user1_token, "Channel 1", True)['channel_id']
    channel_join_v1(user2['token'], chan_id)
    channel_kick_v1(user1_token, chan_id, user2['auth_user_id'])
    assert (channel_details_v1(user1_token, chan_id) == {
        'name' : 'Channel 1',
        'is_public' : True,
        'owner_members' : [{'email': 'john.doe@aunsw.edu.au', 'handle_str': 'johndoe', 'name_first': 'John', 'name_last': 'Doe', 'u_id': get_u_id(user1_token), 'profile_img_url': url + 'imgurl/default.jpg'}],
        'all_members' : [{'email': 'john.doe@aunsw.edu.au', 'handle_str': 'johndoe', 'name_first': 'John', 'name_last': 'Doe', 'u_id': get_u_id(user1_token), 'profile_img_url': url + 'imgurl/default.jpg'}],
    })

# tests for dm_kick_v1
def test_dm_kick_invalid_token():
    clear_v1()
    user1_token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    user2_id = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['auth_user_id']
    dm_id = dm_create_v1(user1_token, [user2_id])['dm_id']
    with pytest.raises(AccessError):
            dm_kick_v1(-1, dm_id, 2)

def test_dm_kick_invalid_channel_id():
    clear_v1()
    user1_token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    channels_create_v1(user1_token, "Channel 1", True)['channel_id']
    with pytest.raises(InputError):
            dm_kick_v1(user1_token, 33, 1)

def test_dm_kick_invalid_user_id():
    clear_v1()
    user1_token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    user2_id = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['auth_user_id']
    dm_id = dm_create_v1(user1_token, [user2_id])['dm_id']
    with pytest.raises(InputError):
            dm_kick_v1(user1_token, dm_id, -1)

def test_dm_kick_token_no_perms():
    clear_v1()
    user1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")
    user2 = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")
    dm_id = dm_create_v1(user1['token'], [user2['auth_user_id']])['dm_id']
    with pytest.raises(AccessError):
            dm_kick_v1(user2['token'], dm_id, user1['auth_user_id'])

def test_dm_kick_valid():
    clear_v1()
    user1 = auth_register_v1("patrick.liang@unsw.com", "katrick", "Patrick", "Liang")
    user2_id = auth_register_v1("john.citizen@unsw.com", "password", "John", "Citizen")['auth_user_id']
    user3_id = auth_register_v1("jane.doe@aunsw.edu.au", "naisud", "Jane", "Doe")['auth_user_id']
    dm_id = dm_create_v1(user1['token'], [user2_id, user3_id])['dm_id']
    dm_kick_v1(user1['token'], dm_id, user3_id)
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
    assert dm_details_v1(user1['token'], dm_id) == {
        'name': 'janedoe, johncitizen, patrickliang',
        'members': [u1, u2]
    }
