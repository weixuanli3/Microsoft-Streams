'''Contains tests for dm_list function'''
import pytest
from src.auth import auth_register_v1
from src.dm import dm_create_v1, dm_list_v1
from src.error import AccessError, InputError
from src.other import clear_v1

@pytest.fixture
def def_setup():
    clear_v1()
    owner = auth_register_v1("john.doe@unsw.com", "bruhdems", "John", "Doe")
    user1 = auth_register_v1("patrick.liang@unsw.com", "katrick", "Patrick", "Liang")
    user2 = auth_register_v1("john.citizen@unsw.com", "password", "John", "Citizen")
    return (owner, user1, user2)

def test_dm_list_no_dms():
    clear_v1()
    user3 = auth_register_v1("nangston.w@unsw.com", "nangwei", "Wynston", "Wang")['token']
    assert dm_list_v1(user3) == {'dms': []}

# Not going to test the handle yet, as it requires dm_details_v1
def test_dm_list_one_dm(def_setup):
    owner_d, user1_d, user2_d = def_setup

    owner = owner_d['token']
    user1 = user1_d['auth_user_id']
    user2 = user2_d['auth_user_id']
    dm_id1 = dm_create_v1(owner, [user1, user2])['dm_id']
    assert dm_list_v1(owner)['dms'][0]['dm_id'] == dm_id1

def test_dm_list_two_dms(def_setup):
    owner_d, user1_d, user2_d = def_setup
    own_tok = owner_d['token']
    u1_tok = user1_d['token']
    u1_id = user1_d['auth_user_id']
    u2_tok = user2_d['token']
    u2_id = user2_d['auth_user_id']
    dm_id1 = dm_create_v1(own_tok, [u1_id, u2_id])['dm_id']
    dm_id2 = dm_create_v1(u1_tok, [u2_id])['dm_id']
    assert dm_list_v1(u1_tok)['dms'][0]['dm_id'] == dm_id1
    assert dm_list_v1(u1_tok)['dms'][1]['dm_id'] == dm_id2

    assert dm_list_v1(u2_tok)['dms'][0]['dm_id'] == dm_id1
    assert dm_list_v1(u2_tok)['dms'][1]['dm_id'] == dm_id2
