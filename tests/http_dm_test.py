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
        "handle_str": "patrickliang"
    }
    user2 = {
        "u_id": u2_id,
        "email": "john.citizen@unsw.com",
        "name_first": "John",
        "name_last": "Citizen",
        "handle_str": "johncitizen"
    }
    user3 = {
        "u_id": u3_id,
        "email": "john.doe@unsw.com",
        "name_first": "John",
        "name_last": "Doe",
        "handle_str": "johndoe"
    }
    dm_id0 = dm_create_req(u1_tok, [u3_id, u2_id])['dm_id']
    details = dm_details_req(u1_tok, dm_id0)
    assert details == {
        'name': "johncitizen, johndoe, patrickliang",
        'members': [user1, user3, user2]
    }

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
        'handle_str': "johncitizen"
    }
    user3 = {
        "u_id": u3_id,
        "email": "john.doe@unsw.com",
        "name_first": "John",
        "name_last": "Doe",
        "handle_str": "johndoe"
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