#import pytest
#from src.auth import auth_register_v1
#from src.dm import dm_create_v1, dm_list_v1, dm_remove_v1, dm_leave_v1
#from src.error import AccessError, InputError
#
#@pytest.fixture
#def def_setup():
#    clear_v1()
#    owner = auth_register_v1("john.doe@unsw.com", "bruhdems", "John", "Doe")
#    user1 = auth_register_v1("patrick.liang@unsw.com", "katrick", "Patrick", "Liang")
#    user2 = auth_register_v1("john.citizen@unsw.com", "password", "John", "Citizen")
#    user3 = auth_register_v1("nangston.w@unsw.com", "nangwei", "Wynston", "Wang")
#    own_tok = owner['token']
#    own_id = owner['auth_user_id']
#    u1_tok = user1['token']
#    u1_id = user1['auth_user_id']
#    u2_tok = user2['token']
#    u2_id = user2['auth_user_id']
#    dm_id1 = dm_create_v1(owner, [u1_id, u2_id])['dm_id']
#    dm_id2 = dm_create_v1(u1_id, [u2_id])['dm_id']
#    dm_id3 = dm_create_v1(u2_id, [])['dm_id']
#    return (own_tok, own_id, u1_tok, u1_id, u2_tok, u2_id, dm_id1, dm_id2, dm_id3)
#
#def test_normal_leave(def_setup):
#    own_tok, own_id, u1_tok, u1_id, u2_tok, u2_id, dm_id1, dm_id2, dm_id3 = def_setup()
#    owner = {
#        'u_id': own_id,
#        'email': "john.doe@unsw.com",
#        'name_first': "John",
#        'name_last': "Doe",
#        'handle_str': "johndoe"
#    }
#    user1 = {
#        'u_id': u1_id,
#        'email': "patrick.liang@unsw.com",
#        'name_first': "Patrick",
#        'name_last': "Liang",
#        'handle_str': "patrickliang"
#    }
#    user2 = {
#        'u_id': u2_id,
#        'email': "john.citizen@unsw.com",
#        'name_first': "John",
#        'name_last': "Citizen",
#        'handle_str': "johncitizen"
#    }
#    dm_leave_v1(own_tok, dm_id1)
#    dm_leave_v1(u2_tok, dm_id2)
#    dm_leave_v1(u2_tok, dm_id3)
#
#    assert dm_details_v1(u1_tok, dm_id1) == {
#        'name': 'johndoe, patrickliang, johncitizen',
#        'members': [user1, user2]
#    }
#    assert dm_details_v1(u1_tok, dm_id2) == {
#        'name': 'patrickliang, johncitizen',
#        'members': [user1]
#    }
#    with pytest.raises(AccessError):
#        dm_leave_v1(u1_tok, dm_id3)
#
#def test_invalid_dm_id(def_setup):
#    own_tok, own_id, u1_tok, u1_id, u2_tok, u2_id, dm_id1, dm_id2, dm_id3 = def_setup()
#    with pytest.raises(InputError):
#        dm_leave_v1(u1_tok, dm_id1 + dm_id2 + 1)
#    with pytest.raises(InputError):
#        dm_leave_v1(u1_tok, -1)
#
#def test_valid_dm_id_not_a_member(def_setup):
#    own_tok, own_id, u1_tok, u1_id, u2_tok, u2_id, dm_id1, dm_id2, dm_id3 = def_setup()
#    user3 = auth_register_v1("nangston.w@unsw.com", "nangwei", "Wynston", "Wang")
#    u3_tok = user3['token']
#    u3_id = user3['auth_user_id']
#    with pytest.raises(AccessError):
#        dm_leave_v1(u3_tok, dm_id1)
#    with pytest.raises(AccessError):
#        dm_leave_v1(own_tok, dm_id2)
#    with pytest.raises(AccessError):
#        dm_leave_v1(u3_tok, dm_id1)
