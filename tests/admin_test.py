'''Contains tests for admin.py'''
import pytest

from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.channel import channel_invite_v1, channel_leave_v1, channel_messages_v1
from src.channel import channel_join_v1
from src.channel import channel_details_v1
from src.error import InputError
from src.error import AccessError
from src.other import clear_v1
from src.data_store import Datastore, data_store, get_u_id
from src.admin import admin_user_remove_id, admin_userpermission_change_v1
from src.dm import dm_create_v1, dm_details_v1, dm_messages_v1
from src.message import message_send_v1, message_senddm_v1

# Tests for admin/user/remove/v1

# Trying to remove only global user
def test_admin_user_remove_id_only_globel_user():
    clear_v1()
    user_data = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")
    with pytest.raises(InputError):
            admin_user_remove_id(user_data['token'], user_data['auth_user_id'])

def test_admin_user_remove_id_invalid_user():
    clear_v1()
    user_data = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")
    with pytest.raises(InputError):
            admin_user_remove_id(user_data['token'], -1)

def test_admin_user_remove_id_removed_from_channels():
    clear_v1()
    # Set up user
    user1_data = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")
    user2_data = auth_register_v1("john.doe1@aunsw.edu.au","password","Jane","Doe")
    # set up channels
    chan_id = channels_create_v1(user1_data['token'], "Stream", True)
    channels_create_v1(user1_data['token'], "Stream2", True)
    channel_join_v1(user2_data['token'], chan_id['channel_id'])

    message_send_v1(user2_data['token'], chan_id['channel_id'], "1")
    message_send_v1(user2_data['token'], chan_id['channel_id'], "2")

    admin_user_remove_id(user1_data['token'], user2_data['auth_user_id'])
    # Test 
    expected = {
        'name' : 'Stream',
        'is_public' : True,
        'owner_members' : [
            {
                'email': 'john.doe@aunsw.edu.au', 
                'handle_str': 'johndoe', 
                'name_first': 'John', 
                'name_last': 'Doe', 
                'u_id': user1_data['auth_user_id']
            }],
        'all_members' : [
                {
                    'email': 'john.doe@aunsw.edu.au', 
                    'handle_str': 'johndoe', 
                    'name_first': 'John', 
                    'name_last': 'Doe', 
                    'u_id': user1_data['auth_user_id']
                }
            ],
        }

    result = channel_details_v1(user1_data['token'], chan_id['channel_id'])

    assert expected == result

def test_admin_user_remove_id_owner_from_channels():
    clear_v1()
    # Set up user
    user1_data = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")
    user2_data = auth_register_v1("john.doe1@aunsw.edu.au","password","Jane","Doe")
    # set up channels
    chan_id = channels_create_v1(user1_data['token'], "Stream", True)
    channels_create_v1(user1_data['token'], "Stream2", True)
    channel_join_v1(user2_data['token'], chan_id['channel_id'])

    message_send_v1(user1_data['token'], chan_id['channel_id'], "1")
    message_send_v1(user2_data['token'], chan_id['channel_id'], "2")

    # Make user 2 admin
    admin_userpermission_change_v1(user1_data['token'], user2_data['auth_user_id'], 1)
    # Remove user 1
    admin_user_remove_id(user2_data['token'], user1_data['auth_user_id'])
    
    # Test 
    expected = {
        'name' : 'Stream',
        'is_public' : True,
        'owner_members' : [],
        'all_members' : [
                {
                    'email': 'john.doe1@aunsw.edu.au', 
                    'handle_str': 'janedoe', 
                    'name_first': 'Jane', 
                    'name_last': 'Doe', 
                    'u_id': user2_data['auth_user_id']
                }
            ],
        }

    result = channel_details_v1(user2_data['token'], chan_id['channel_id'])

    assert expected == result


# THis test will forever make me want to not be here
# POTENTIAL FIX
def test_admin_user_remove_id_remove_from_dms():
    clear_v1()
    user1_data = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")
    user2_data = auth_register_v1("john.doe1@aunsw.edu.au","password","Jane","Doe")

    dm_id = dm_create_v1(user1_data['token'], [user2_data['auth_user_id']])

    message_senddm_v1(user1_data['token'], dm_id['dm_id'], "I will removed you")
    message_senddm_v1(user2_data['token'], dm_id['dm_id'], "I want to be banned")
    
    admin_user_remove_id(user1_data['token'], user2_data['auth_user_id'])
    # Is rhe name geenrated in alphbetical order of handles?
    # Is auth creater put into the members list?

    dm_details = dm_details_v1(user1_data['token'], dm_id['dm_id'])

    expected_dm_details = {
        'name' : 'janedoe, johndoe',
        'members' : [ {
                'u_id': user1_data['auth_user_id'],
                'email': 'john.doe@aunsw.edu.au',
                'name_first': 'John',
                'name_last': 'Doe',
                'handle_str': 'johndoe'
            } ]
    }

    assert dm_details == expected_dm_details

    message = dm_messages_v1(user1_data['token'], dm_id['dm_id'], 0)['messages'][0]['message']
    expected_message = 'Removed user'

    assert message == expected_message

# Tests for admin/userpermission/change/v1

def test_admin_userpermission_change_invalid_permission():
    clear_v1()
    auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    user2_token = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['token']
    user3_id = auth_register_v1("john.sam@aunsw.edu.au", "kjwnef", "John", "Sam")['auth_user_id']
    with pytest.raises(AccessError):
            admin_userpermission_change_v1(user2_token, user3_id, 1)

def test_admin_userpermission_change_invalid_u_id():
    clear_v1()
    user1_token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    with pytest.raises(InputError):
            admin_userpermission_change_v1(user1_token, -1, 1)
    
def test_admin_userpermission_change_empty_u_id():
    clear_v1()
    auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    user2_token = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['token']
    with pytest.raises(InputError):
            admin_userpermission_change_v1(user2_token, "", 1)

def test_admin_userpermission_change_not_global_owner():
    clear_v1()
    user1_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['auth_user_id']
    user2_token = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['token']
    with pytest.raises(AccessError):
            admin_userpermission_change_v1(user2_token, user1_id, 1)

def test_admin_userpermission_change_permission_same():
    clear_v1()
    user1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")
    user2 = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")
    with pytest.raises(InputError):
        admin_userpermission_change_v1(user1['token'], user2['auth_user_id'], 2)

def test_admin_userpermission_change_self_change():
    clear_v1()
    user1_data = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")
    token = user1_data['token']
    u_id = user1_data['auth_user_id']
    with pytest.raises(InputError):
        admin_userpermission_change_v1(token, u_id, 1)
    # global_owners = data_store.get_data()['global_owners']
    # assert global_owners == [user2_token]

def test_admin_userpermission_change_only_global_owner():
    clear_v1()
    user1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")
    with pytest.raises(InputError):
        admin_userpermission_change_v1(user1['token'], user1['auth_user_id'], 2)

def test_admin_userpermission_invalid_token():
    clear_v1()
    auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")
    user2 = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")
    with pytest.raises(AccessError):
        admin_userpermission_change_v1("ABC", user2['auth_user_id'], 2)

def test_admin_userpermission_change_permission_id_invalid():
    clear_v1()
    user1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")
    user2 = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")
    with pytest.raises(InputError):
        admin_userpermission_change_v1(user1['token'], user2['auth_user_id'], 4)

def test_admin_userpermission_change_global_removed():
    clear_v1()
    user1_token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    user2_id = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['auth_user_id']
    admin_userpermission_change_v1(user1_token, user2_id, 1)
    # global_owners = data_store.get_data()['global_owners']
    # assert global_owners == [user1_token, user2_token]

def test_admin_userpermission_change_global_added():
    clear_v1()
    user1_data = auth_register_v1("john.doe@aunsw.edu.au", "naisud", "John", "Doe")
    user1_id = user1_data['auth_user_id']
    user1_token = user1_data['token']
    user2_data = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")
    user2_id = user2_data['auth_user_id']
    user2_token = user2_data['token']
    admin_userpermission_change_v1(user1_token, user2_id, 1)
    admin_userpermission_change_v1(user2_token, user1_id, 2)
    # global_owners = data_store.get_data()['global_owners']
    # assert global_owners == [user2_token]

def test_admin_userpermission_only_global_removed():
    clear_v1()
    user1_data = auth_register_v1("john.doe@aunsw.edu.au", "naisud", "John", "Doe")
    with pytest.raises(InputError):
        admin_userpermission_change_v1(user1_data['token'], user1_data['auth_user_id'], 2)

# ASSUMPTION - CANNOT CHNAGE TO SELF
def test_admin_userpermission_change_global_to_global():
    clear_v1()
    user1_data = auth_register_v1("john.doe@aunsw.edu.au", "naisud", "John", "Doe")
    with pytest.raises(InputError):
        admin_userpermission_change_v1(user1_data['token'], user1_data['auth_user_id'], 1)

# ASSUMPTION - CANNOT CHNAGE TO SELF
def test_admin_userpermission_change_user_to_user():
    clear_v1()
    user1_data = auth_register_v1("john.doe@aunsw.edu.au", "naisud", "John", "Doe")
    user2_data = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")

    with pytest.raises(InputError):
        admin_userpermission_change_v1(user1_data['token'], user2_data['auth_user_id'], 2)

    clear_v1()