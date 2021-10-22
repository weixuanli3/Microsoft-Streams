import pytest
import requests
import json
from src.error import AccessError, InputError
from other_functions.request_helper_functions import *
from src.config import url
from src.data_store import data_store

@pytest.fixture
def default_setup():
    clear_req()
    u1 = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")
    u2 = auth_register_req("john.doe1@aunsw.edu.au","password","Jane","Doe")
    return (u1, u2)

@pytest.fixture
def channels_setup(default_setup):
    u1, u2 = default_setup
    u1_tok = u1['token']
    chan_id_1 = channels_create_req(u1_tok, "Stream", True)['channel_id']
    return (u1, u2, chan_id_1)

# Tests for admin/user/remove/v1
def test_admin_user_remove_only_global():
    clear_req()
    user_data = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")
    invalid_only_global = admin_user_remove_req(user_data['token'], user_data['auth_user_id'])
    assert invalid_only_global['code'] == AccessError.code

def test_admin_user_remove_invalid_user():
    clear_req()
    u1 = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")
    u1_tok = u1['token']
    invalid_user = admin_user_remove_req(u1_tok, -1)
    assert invalid_user['code'] == InputError.code
    
def test_admin_user_remove_removed_from_channels(channels_setup):
    u1, u2, chan_id_1 = channels_setup
    u1_tok = u1['token']
    u2_tok = u2['token']
    u2_id = u2['auth_user_id']
    u3 = auth_register_req("nangston.w@unsw.com", "nangwei", "Wynston", "Wang")
    u3_tok = u3['token']
    u3_id = u3['auth_user_id']
    channel_join_req(u2_tok, chan_id_1)
    channel_join_req(u3_tok, chan_id_1)
    
    channels_create_req(u2_tok, "Streams", True)
    
    assert admin_user_remove_req(u1_tok, u2_id) == {}
    assert admin_user_remove_req(u1_tok, u3_id) == {}
    
    assert channel_details_req(u1_tok, chan_id_1) == {
        'name' : 'Stream',
        'is_public' : True,
        'owner_members' : [
            {
                'email': 'john.doe@aunsw.edu.au', 
                'handle_str': 'johndoe', 
                'name_first': 'John', 
                'name_last': 'Doe', 
                'u_id': u1['auth_user_id']
            }],
        'all_members' : [
                {
                    'email': 'john.doe@aunsw.edu.au', 
                    'handle_str': 'johndoe', 
                    'name_first': 'John', 
                    'name_last': 'Doe', 
                    'u_id': u1['auth_user_id']
                }
            ],
        }
    
def test_admin_user_remove_remove_from_dms(default_setup):
    u1, u2 = default_setup
    u1_tok = u1['token']
    u2_tok = u2['token']
    u2_id = u2['auth_user_id']
    dm_id = dm_create_req(u1_tok, [u2_id])['dm_id']
    
    message_senddm_req(u1_tok, dm_id, "I will remove you")
    message_senddm_req(u2_tok, dm_id, "I want to be removed")
    
    # print(message_send_req(u2_tok, dm_id, "I want to be removed"))
    
    admin_user_remove_req(u1_tok, u2_id)
    
    assert dm_details_req(u1_tok, dm_id) == {
    'name' : 'janedoe, johndoe',
    'members' : [ {
            'u_id': u1['auth_user_id'],
            'email': 'john.doe@aunsw.edu.au',
            'name_first': 'John',
            'name_last': 'Doe',
            'handle_str': 'johndoe'
        } ]
    }
    
    # print(dm_messages_req(u1_tok, dm_id, 0))
    
    assert dm_messages_req(u1_tok, dm_id, 0)['messages'][0]['message'] == 'Removed user'   
    
# Tests for admin/userpermission/change/v1

def test_admin_userpermission_change_invalid_perms(default_setup):
    u1, u2 = default_setup
    u1_id = u1['auth_user_id']
    u2_tok = u2['token']
    
    invalid_perms = admin_userpermission_change_req(u2_tok, u1_id, 2)
    
    assert invalid_perms['code'] == AccessError.code

def test_admin_userpermission_change_invalid_u_id():
    clear_req()
    u1_tok = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    
    invalid_u_id = admin_userpermission_change_req(u1_tok, -1, 1)
    
    assert invalid_u_id['code'] == InputError.code
    
def test_admin_userpermissions_change_empty_u_id():
    clear_req()
    u1_tok = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    
    invalid_u_id = admin_userpermission_change_req(u1_tok, "", 1)
    
    assert invalid_u_id['code'] == InputError.code
    
def test_admin_userpermissions_not_global_owner(default_setup):
    u1, u2 = default_setup
    u1_id = u1['auth_user_id']
    u2_tok = u2['token']
    
    not_global = admin_userpermission_change_req(u2_tok, u1_id, 2)
    
    assert not_global['code'] == AccessError.code
    
def test_admin_userpermission_change_permission_same(default_setup):
    u1, u2 = default_setup
    u1_tok = u1['token']
    u2_id = u2['auth_user_id']
    
    perm_same = admin_userpermission_change_req(u1_tok, u2_id, 2)
    
    assert perm_same['code'] == InputError.code
    
def test_admin_userpermission_change_self_change(default_setup):
    u1, u2 = default_setup
    u1_tok = u1['token']
    u1_id = u1['auth_user_id']
    u2_id = u2['auth_user_id']
    admin_userpermission_change_req(u1_tok, u2_id, 1)
    
    self_change = admin_userpermission_change_req(u1_tok, u1_id, 1)
    
    assert self_change['code'] == InputError.code
    
def test_admin_userpermission_change_only_global_owner():
    clear_req()
    u1 = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")
    u1_tok = u1['token']
    u1_id = u1['auth_user_id']
    
    only_global = admin_userpermission_change_req(u1_tok, u1_id, 2)
    
    assert only_global['code'] == InputError.code
    
def test_admin_userpermission_invalid_token():
    clear_req()
    auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")
    u2 = auth_register_req("john.smith@aunsw.edu.au", "naisud", "John", "Smith")
    u2_id = u2['auth_user_id']
    
    invalid_token = admin_userpermission_change_req("ABC", u2_id, 2)
    
    assert invalid_token['code'] == AccessError.code
    
def test_admin_userpermission_change_permission_id_invalid(default_setup):
    u1, u2 = default_setup
    u1_tok = u1['token']
    u2_id = u2['auth_user_id']
    
    invalid_id = admin_userpermission_change_req(u1_tok, u2_id, 4)
    
    assert invalid_id['code'] == InputError.code
    
def test_admin_userpermission_change_global(default_setup):
    u1, u2 = default_setup
    u1_tok = u1['token']
    u2_tok = u2['token']
    u2_id = u2['auth_user_id']
    
    chan_id = channels_create_req(u1_tok, "Streams", False)['channel_id']
    
    admin_userpermission_change_req(u1_tok, u2_id, 1)
    
    assert channel_join_req(u2_tok, chan_id) == {}

def test_admin_userpermission_change_remove_global(default_setup):
    u1, u2 = default_setup
    u1_tok = u1['token']
    u2_tok = u2['token']
    u1_id = u1['auth_user_id']
    u2_id = u2['auth_user_id']
    
    chan_id_1 = channels_create_req(u1_tok, "Streams", False)['channel_id']
    chan_id_2 = channels_create_req(u2_tok, "Streams 2", False)['channel_id']
    
    admin_userpermission_change_req(u1_tok, u2_id, 1)
    
    admin_userpermission_change_req(u2_tok, u1_id, 2)
    
    assert channel_join_req(u2_tok, chan_id_1) == {}
    
    not_global = channel_join_req(u1_tok, chan_id_2)
    
    assert not_global['code'] == AccessError.code
    
