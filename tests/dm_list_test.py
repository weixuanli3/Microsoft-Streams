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
   user3 = auth_register_v1("nangston.w@unsw.com", "nangwei", "Wynston", "Wang")
   own_tok = owner['token']
   own_id = owner['auth_user_id']
   u1_tok = user1['token']
   u1_id = user1['auth_user_id']
   u2_tok = user2['token']
   u2_id = user2['auth_user_id']
   u3_tok = user3['token']
   u3_id = user3['auth_user_id']
   dm_id1 = dm_create_v1(owner, [u1_id, u2_id])['dm_id']
   dm_id2 = dm_create_v1(u1_id, [u2_id])['dm_id']
   return (own_tok, own_id, u1_tok, u1_id, u2_tok, u2_id, u3_tok, u3_id, dm_id1, dm_id2)

def test_dm_list_no_dms(def_setup):
   own_tok, own_id, u1_tok, u1_id, u2_tok, u2_id, u3_tok, u3_id, dm_id1, dm_id2 = def_setup()
   assert dm_list_v1(u3_tok) == {'dms': []}

# Not going to test the handle yet, as it requires dm_details_v1
def test_dm_list_one_dm(def_setup):
   own_tok, own_id, u1_tok, u1_id, u2_tok, u2_id, u3_tok, u3_id, dm_id1, dm_id2 = def_setup()
   assert dm_list_v1(own_tok)['dms'][0]['dm_id'] == dm_id1

def test_dm_list_two_dms(def_setup):
   own_tok, own_id, u1_tok, u1_id, u2_tok, u2_id, u3_tok, u3_id, dm_id1, dm_id2 = def_setup()
   assert dm_list_v1(u1_tok)['dms'][0]['dm_id'] == dm_id1
   assert dm_list_v1(u1_tok)['dms'][1]['dm_id'] == dm_id2

   assert dm_list_v1(u2_tok)['dms'][0]['dm_id'] == dm_id1
   assert dm_list_v1(u2_tok)['dms'][1]['dm_id'] == dm_id2