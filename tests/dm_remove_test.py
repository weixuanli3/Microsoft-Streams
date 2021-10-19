import pytest
from src.auth import auth_register_v1
from src.dm import dm_create_v1, dm_list_v1, dm_remove_v1
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
   own_id = owner['auth_user_id']
   u1_tok = user1['token']
   u1_id = user1['auth_user_id']
   u2_tok = user2['token']
   u2_id = user2['auth_user_id']
   u3_tok = user3['token']
   u3_id = user3['auth_user_id']
   dm_id1 = dm_create_v1(owner, u1_id, u2_id)['dm_id']
   dm_id2 = dm_create_v1(u1_id, [u2_id])['dm_id']
   return (own_tok, own_id, u1_tok, u1_id, u2_tok, u2_id, u3_tok, u3_id, dm_id1, dm_id2)

def test_valid_removal(def_setup):
   own_tok, own_id, u1_tok, u1_id, u2_tok, u2_id, u3_tok, u3_id, dm_id1, dm_id2 = def_setup()
   dm_remove_v1(own_tok, dm_id1)
   dm_remove_v1(u1_tok, dm_id2)

def test_invalid_dm_id(def_setup):
   own_tok, own_id, u1_tok, u1_id, u2_tok, u2_id, u3_tok, u3_id, dm_id1, dm_id2 = def_setup()
   dm_id3 = dm_id1 + dm_id2 + 3123
   with pytest.raises(InputError):
       dm_remove_v1(own_tok, dm_id3)
   with pytest.raises(InputError):
       dm_remove_v1(u1_tok, dm_id3)
   with pytest.raises(InputError):
       dm_remove_v1(u2_tok, dm_id3)
   with pytest.raises(InputError):
       dm_remove_v1(u3_tok, dm_id3)


def test_valid_dm_id_not_owner(def_setup):
   own_tok, own_id, u1_tok, u1_id, u2_tok, u2_id, u3_tok, u3_id, dm_id1, dm_id2 = def_setup()
   with pytest.raises(AccessError):
       dm_remove_v1(own_tok, dm_id2)
   with pytest.raises(AccessError):
       dm_remove_v1(u1_tok, dm_id1)
   with pytest.raises(AccessError):
       dm_remove_v1(u2_tok, dm_id1)
   with pytest.raises(AccessError):
       dm_remove_v1(u3_tok, dm_id2)