'''Contains tests for dm_details function'''
import pytest
from src.auth import auth_register_v1
from src.config import url
from src.dm import dm_create_v1, dm_list_v1, dm_details_v1
from src.error import AccessError, InputError
from src.other import clear_v1

@pytest.fixture
def def_setup():
    clear_v1()
    owner = auth_register_v1("john.doe@unsw.com", "bruhdems", "John", "Doe")
    user1 = auth_register_v1("patrick.liang@unsw.com", "katrick", "Patrick", "Liang")
    user2 = auth_register_v1("john.citizen@unsw.com", "password", "John", "Citizen")
    user3 = auth_register_v1("nangston.w@unsw.com", "nangwei", "Wynston", "Wang")
    own_tok = owner['token']
    u1_tok = user1['token']
    u1_id = user1['auth_user_id']
    u2_id = user2['auth_user_id']
    dm_id1 = dm_create_v1(own_tok, [u1_id, u2_id])['dm_id']
    dm_id2 = dm_create_v1(u1_tok, [u2_id])['dm_id']
    return (owner, user1, user2, user3, dm_id1, dm_id2)

def test_valid_details(def_setup):
    owner, user1, user2, user3, dm_id1, dm_id2 = def_setup
    own_tok = owner['token']
    own_id = owner['auth_user_id']
    u1_tok = user1['token']
    u1_id = user1['auth_user_id']
    u2_id = user2['auth_user_id']
    u3_tok = user3['token']
    u3_id = user3['auth_user_id']
    dm_id3 = dm_create_v1(u3_tok, [])['dm_id']
    ow = {
        'u_id': own_id,
        'email': "john.doe@unsw.com",
        'name_first': "John",
        'name_last': "Doe",
        'handle_str': "johndoe",
        'profile_img_url': url + 'imgurl/default.jpg'
    }
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
    u3 = {
        'u_id': u3_id,
        'email': "nangston.w@unsw.com",
        'name_first': "Wynston",
        'name_last': "Wang",
        'handle_str': "wynstonwang",
        'profile_img_url': url + 'imgurl/default.jpg'
    }
    assert dm_details_v1(own_tok, dm_id1) == {
        'name': 'johncitizen, johndoe, patrickliang',
        'members': [ow, u1, u2]
    }
    assert dm_details_v1(u1_tok, dm_id1) == {
        'name': 'johncitizen, johndoe, patrickliang',
        'members': [ow, u1, u2]
    }
    assert dm_details_v1(u1_tok, dm_id2) == {
        'name': 'johncitizen, patrickliang',
        'members': [u1, u2]
    }
    assert dm_details_v1(u3_tok, dm_id3) == {
        'name': 'wynstonwang',
        'members': [u3]
    }

def test_invalid_dm_id(def_setup):
    owner, user1, user2, user3, dm_id1, dm_id2 = def_setup
    own_tok = owner['token']
    u1_tok = user1['token']
    u2_tok = user2['token']
    u3_tok = user3['token']
    with pytest.raises(InputError):
        dm_details_v1(u1_tok, dm_id1 + dm_id2 + 1)
    with pytest.raises(InputError):
        dm_details_v1(u1_tok, -1)
    with pytest.raises(InputError):
        dm_details_v1(u2_tok, -1)
    with pytest.raises(InputError):
        dm_details_v1(u3_tok, -1)
    with pytest.raises(InputError):
        dm_details_v1(own_tok, -1)

def test_valid_dm_not_member(def_setup):
    owner, user1, user2, user3, dm_id1, dm_id2 = def_setup
    own_tok = owner['token']
    u1_tok = user1['token']
    u2_tok = user2['token']
    u3_tok = user3['token']
    dm_id3 = dm_create_v1(u3_tok, [])['dm_id']
    with pytest.raises(AccessError):
        dm_details_v1(u3_tok, dm_id1)
    with pytest.raises(AccessError):
        dm_details_v1(own_tok, dm_id2)
    with pytest.raises(AccessError):
        dm_details_v1(u3_tok, dm_id1)
    with pytest.raises(AccessError):
        dm_details_v1(u1_tok, dm_id3)
    with pytest.raises(AccessError):
        dm_details_v1(u2_tok, dm_id3)