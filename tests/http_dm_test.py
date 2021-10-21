import pytest
import requests
import json
from src.error import AccessError, InputError
from src.config import url
from src.data_store import data_store

@pytest.fixture
def default_setup():
    requests.delete(f"{url}clear/v1")
    user1 = {
        "email": "patrick.liang@unsw.com",
        "password": "katrick",
        "name_first": "Patrick",
        "name_last": "Liang"
    }
    user2 = {
        "email": "john.citizen@unsw.com",
        "password": "password",
        "name_first": "John",
        "name_last": "Citizen"
    }
    user3 = {
        "email": "john.doe@unsw.com",
        "password": "bruhyikes",
        "name_first": "John",
        "name_last": "Doe"
    }
    u1 = requests.post(f"{url}auth/register/v2", data=json.dumps(user1)).json()
    u2 = requests.post(f"{url}auth/register/v2", data=json.dumps(user2)).json()
    u3 = requests.post(f"{url}auth/register/v2", data=json.dumps(user3)).json()
    return (u1, u2, u3)


def test_dm_create_invalid_id(default_setup):
    u1, u2, u3 = default_setup
    u1_tok = u1['token']
    u2_id = u2['auth_user_id']
    u3_id = u3['auth_user_id']
    input0 = {
        "token": u1_tok,
        "u_ids": [u3_id + u2_id]
    }
    response0 = requests.post(f"{url}dm/create/v1", data=json.dumps(input0))
    assert response0.status_code == InputError.code

    input1 = {
        "token": u1_tok,
        "u_ids": [u3_id + u2_id, u2_id, u3_id]
    }
    response1 = requests.post(f"{url}dm/create/v1", data=json.dumps(input1))
    assert response1.status_code == InputError.code

def test_dm_create_valid(default_setup):
    u1, u2, u3 = default_setup
    u1_tok = u1['token']
    u2_tok = u2['token']
    u2_id = u2['auth_user_id']
    u3_id = u3['auth_user_id']
    input0 = {
        "token": u1_tok,
        "u_ids": [u2_id, u3_id]
    }
    response0 = requests.post(f"{url}dm/create/v1", data=json.dumps(input0))
    response0_data = response0.json()

    input1 = {
        "token": u2_tok,
        "u_ids": [u3_id]
    }
    response1 = requests.post(f"{url}dm/create/v1", data=json.dumps(input1))
    response1_data = response1.json()

    assert response1_data['dm_id'] != response0_data['dm_id']

# not a member and then invalid dm id
def test_dm_details_invalid(default_setup):
    u1, u2, u3 = default_setup
    u1_tok = u1['token']
    u2_id = u2['auth_user_id']
    u3_tok = u3['token']
    input0 = {
        "token": u1_tok,
        "dm_id": 23
    }
    response0 = requests.get(f"{url}/dm/details/v1", params=input0)
    assert response0.status_code == InputError.code

    input1 = {
        "token": u1_tok,
        "u_ids": [u2_id]
    }
    response1 = requests.post(f"{url}/dm/create/v1", data=json.dumps(input1)).json()
    dm_id = response1['dm_id']

    input2 = {
        "token": u3_tok,
        "dm_id": dm_id
    }
    response2 = requests.get(f"{url}/dm/details/v1", params=input2)
    assert response2.status_code == AccessError.code

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
    input0 = {
        "token": u1_tok,
        "u_ids": [u2_id, u3_id]
    }
    response0 = requests.post(f"{url}dm/create/v1", data=json.dumps(input0))
    response0_data = response0.json()
    dm_id0 = response0_data['dm_id']

    input1 = {
        "token": u1_tok,
        "dm_id": dm_id0
    }

    response1 = requests.get(f"{url}dm/details/v1", params=input1).json()
    assert response1 == {
        'name': "johncitizen, johndoe, patrickliang",
        'members': [user1, user2, user3]
    }
