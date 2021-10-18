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

# Tests for admin/user/remove/v1


# Tests for admin/userpermission/change/v1

def test_admin_userpermission_change_invalid_token():
    clear_v1()
    auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    user2_token = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['token']
    user3_token = auth_register_v1("john.sam@aunsw.edu.au", "kjwnef", "John", "Sam")['token']
    with pytest.raises(AccessError):
            admin_userpermission_change_v1(user2_token, user3_token, 1)

def test_admin_userpermission_change_invalid_u_id():
    clear_v1()
    auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    user2_token = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['token']
    with pytest.raises(InputError):
            admin_userpermission_change_v1(user2_token, -1, 1)
    
def test_admin_userpermission_change_empty_u_id():
    clear_v1()
    auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    user2_token = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['token']
    with pytest.raises(InputError):
            admin_userpermission_change_v1(user2_token, "", 1)

def test_admin_userpermission_change_not_global_owner():
    clear_v1()
    user1_token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    user2_token = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['token']
    with pytest.raises(AccessError):
            admin_userpermission_change_v1(user2_token, user1_token, 1)

def test_admin_userpermission_change_permission_same():
    clear_v1()
    user1_token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    user2_token = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['token']
    with pytest.raises(InputError):
        admin_userpermission_change_v1(user1_token, user2_token, 2)

def test_admin_userpermission_change_self_change():
    clear_v1()
    user1_token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    user2_token = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['token']
    admin_userpermission_change_v1(user1_token, user2_token, 1)
    admin_userpermission_change_v1(user1_token, user1_token, 2)
    global_owners = data_store.get_data()['global_owners']
    assert global_owners == [user2_token]
    

def test_admin_userpermission_change_only_global_owner():
    clear_v1()
    user1_token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    with pytest.raises(InputError):
        admin_userpermission_change_v1(user1_token, user1_token, 2)

def test_admin_userpermission_change_permission_id_invalid():
    clear_v1()
    user1_token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    user2_token = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['token']
    with pytest.raises(InputError):
        admin_userpermission_change_v1(user1_token, user2_token, 4)

def test_admin_userpermission_change_global_removed():
    clear_v1()
    user1_token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    user2_token = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['token']
    admin_userpermission_change_v1(user1_token, user2_token, 1)
    global_owners = data_store.get_data()['global_owners']
    assert global_owners == [user1_token, user2_token]

def test_admin_userpermission_change_global_added():
    clear_v1()
    user1_token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    user2_token = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['token']
    admin_userpermission_change_v1(user1_token, user2_token, 1)
    admin_userpermission_change_v1(user2_token, user1_token, 2)
    global_owners = data_store.get_data()['global_owners']
    assert global_owners == [user2_token]