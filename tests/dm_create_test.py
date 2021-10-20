import pytest
from src.auth import auth_register_v1
from src.dm import dm_create_v1
from src.error import AccessError, InputError
from src.other import clear_v1

@pytest.fixture
def def_setup():
    clear_v1()
    owner = auth_register_v1("john.doe@unsw.com", "bruhdems", "John", "Doe")
    user1 = auth_register_v1("patrick.liang@unsw.com", "katrick", "Patrick", "Liang")
    user2 = auth_register_v1("john.citizen@unsw.com", "password", "John", "Citizen")
    return (owner, user1, user2)

def test_normal(def_setup):
    owner, user1, user2 = def_setup
    own_token = owner['token']
    own_id = owner['auth_user_id']
    user1_token = user1['token']
    user1_id = user1['auth_user_id']
    user2_token = user2['token']
    user2_id = user2['auth_user_id']
    dm_create_v1(own_token, [user1_id, user2_id])
    dm_create_v1(user1_token, [user2_id])
    dm_create_v1(user2_token, [own_id])

def test_invalid_token(def_setup):
    owner, user1, user2 = def_setup
    own_id = owner['auth_user_id']
    user1_id = user1['auth_user_id']
    user2_id = user2['auth_user_id']
    with pytest.raises(AccessError):
        dm_create_v1("owneradfse", [own_id])
    with pytest.raises(AccessError):
        dm_create_v1("bruhdems", [own_id, user1_id, user2_id])

def test_u_id_does_not_exist(def_setup):
    owner, user1, user2 = def_setup
    own_token = owner['token']
    user1_id = user1['auth_user_id']
    user2_id = user2['auth_user_id']
    with pytest.raises(InputError):
        dm_create_v1(own_token, [-3, -2])
    with pytest.raises(InputError):
        dm_create_v1(own_token, [-3, user1_id, user2_id])

def test_diff_dm_id(def_setup):
    owner, user1, user2 = def_setup
    own_token = owner['token']
    own_id = owner['auth_user_id']
    user1_token = user1['token']
    user1_id = user1['auth_user_id']
    user2_token = user2['token']
    user2_id = user2['auth_user_id']
    dm_id1 = dm_create_v1(own_token, [user1_id, user2_id])['dm_id']
    dm_id2 = dm_create_v1(user1_token, [user2_id])['dm_id']
    dm_id3 = dm_create_v1(user2_token, [own_id])['dm_id']
    assert dm_id1 != dm_id2
    assert dm_id2 != dm_id3
    assert dm_id3 != dm_id1

def test_no_users(def_setup):
    owner, user1, user2 = def_setup
    own_token = owner['token']
    user1_token = user1['token']
    user2_token = user2['token']
    dm_create_v1(own_token, [])
    dm_create_v1(user1_token, [])
    dm_create_v1(user2_token, [])

# Assumption, if the dm that is to be created already exists, return the id 
# of the existing dm
# def test_dm_exists(def_setup):
#    owner, owner_id, user1, user1_id, user2, user2_id = def_setup
#    dm_id1 = dm_create_v1(owner, [user1_id, user2_id])['dm_id']
#    dm_id2 = dm_create_v1(owner, [user1_id, user2_id])['dm_id']
#    assert dm_id1 == dm_id2

def test_dm_same_members_diff_owner():
    clear_v1()
    owner = auth_register_v1("john.doe@unsw.com", "bruhdems", "John", "Doe")
    user1 = auth_register_v1("patrick.liang@unsw.com", "katrick", "Patrick", "Liang")
    own_token = owner['token']
    own_id = owner['auth_user_id']
    user1_token = user1['token']
    user1_id = user1['auth_user_id']
    dm_id1 = dm_create_v1(own_token, [user1_id])['dm_id']
    dm_id2 = dm_create_v1(user1_token, [own_id])['dm_id']
    assert dm_id1 != dm_id2
