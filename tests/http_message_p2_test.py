'''Contains http tests for message functions in it3'''
import pytest
import datetime as dt
import time
import requests
import json
from src.error import AccessError, InputError
from other_functions.request_helper_functions import *
from src.config import url

## NEED TO CHECK WHEN BOTH INCPUT AND ACCESS ERRORS ARE SPIT OUT

## The following tests are for message_share
        
# def test_message_share_invalid_token(Channel_setup):
#     u1, u2, chan1_id = Channel_setup
#     channel_join_req(u2['token'], chan1_id)
#     msg_id = message_send_req(u1['token'], chan1_id, "Hi there!")['message_id']
#     assert message_share_req(444, msg_id, "heyo", chan1_id, -1)['code'] == AccessError.code

# def test_message_share_idm_and_chan_id_neg(Channel_setup):
#     u1, u2, chan1_id = Channel_setup
#     channel_join_req(u2['token'], chan1_id)
#     msg_id = message_send_req(u1['token'], chan1_id, "Hi there!")['message_id']
#     assert message_share_req(u1['token'], msg_id, "heyo", -1, -1)['code'] == InputError.code    

# def test_message_share_invalid_chan_id(Channel_setup):
#     u1, u2, chan1_id = Channel_setup
#     channel_join_req(u2['token'], chan1_id)
#     msg_id = message_send_req(u1['token'], chan1_id, "Hi there!")['message_id']
#     assert message_share_req(u1['token'], msg_id, "heyo", 33, -1)['code'] == InputError.code  

# def test_message_share_invalid_dm_id(dms_setup):
#     u1, u2, dm_id1 = dms_setup
#     dm_msg_id = message_senddm_req(u1['token'], dm_id1, "Hey")['message_id']
#     assert message_share_req(u1['token'], dm_msg_id, "heyo", -1, 66)['code'] == InputError.code

# def test_message_share_invalid_dm_and_chan_id(dms_setup):
#     u1, u2, dm_id1 = dms_setup
#     dm_msg_id = message_senddm_req(u1['token'], dm_id1, "Hey")['message_id']
#     u1_tok = u1['token']
#     chan1_id = channels_create_req(u1_tok, "Channel 1", True)['channel_id']
#     msg_id = message_send_req(u1['token'], chan1_id, "Hi there!")['message_id']
#     assert message_share_req(u1['token'], msg_id, "heyo", 77, 66)['code'] == InputError.code 
#     assert message_share_req(u1['token'], dm_msg_id, "heyo", 77, 66)['code'] == InputError.code 

# def test_message_share_invalid_dm_msg_id(dms_setup):
#     u1, u2, dm_id1 = dms_setup
#     dm_msg_id = message_senddm_req(u1['token'], dm_id1, "Hey")['message_id']
#     assert message_share_req(u1['token'], 33, "heyo", -1, dm_id1)['code'] == InputError.code

# def test_message_share_invalid_msg_id(Channel_setup):
#     u1, u2, chan1_id = Channel_setup
#     channel_join_req(u2['token'], chan1_id)
#     message_send_req(u1['token'], chan1_id, "Hi there!")['message_id']
#     assert message_share_req(u1['token'], 44, "heyo", chan1_id, -1)['code'] == InputError.code
        
# def test_message_share_more_than_100_chars(Channel_setup):
#     u1, u2, chan1_id = Channel_setup
#     channel_join_req(u2['token'], chan1_id)
#     msg_id = message_send_req(u1['token'], chan1_id, "Hi there!")['message_id']
#     assert message_share_req(u1['token'], msg_id, """
#                         Hey Thereivbfriehuferhuifferhuierfihuerfiphuerfpihuerfphuierfpihuer
#                         fiphuerfihuperfpppppppppppppppppppppppppppppppppppppppppppppppppppppp
#                         pppppppppppppppppppppppppppppppppppppppppppppppppppppppppppprefihuopppp
#                         pppppppppppiooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
#                         oooooooooooooooooooooooooooooooooooooooooooooooooooooooooiiiiiiiiiiiii
#                         iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
#                         iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
#                         iiiiiiiiiiiiiiiiii HeyThereivbfriehuferhuifferhuierfihuerfiphuerfpihuer
#                         fphuierfpihuerfiphuerfihuperfpppppppppppppppppppppppppppppppppppppppppp
#                         pppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp
#                         refihuopppppppppppppppiooooooooooooooooooooooooooooooooooooooooooooooooo
#                         oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooiiiiii
#                         iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
#                         iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
#                         iiiiiiiiiiiiiiiiiii""", chan1_id, -1)['code'] == InputError.code

# def test_message_share_user_not_in_chan(Channel_setup):
#     u1, u2, chan1_id = Channel_setup
#     msg_id = message_send_req(u1['token'], chan1_id, "Hi there!")['message_id']
#     assert message_share_req(u2['token'], msg_id, "heyo", chan1_id, -1)['code'] == AccessError.code

# def test_message_share_user_not_in_dm(dms_setup):
#     u1, u2, dm_id1 = dms_setup
#     dm_msg_id = message_senddm_req(u1['token'], dm_id1, "Hey")['message_id']
#     dm_msg_id2 = message_senddm_req(u2['token'], dm_id1, "Hey")['message_id']
#     u3 = auth_register_req("gooba.smith@unsw.com", "password", "Gooba", "Smoth")
#     assert message_share_req(u3['token'], dm_msg_id, "heyo", -1, dm_id1)['code'] == AccessError.code
#     assert message_share_req(u3['token'], dm_msg_id2, "heyo", -1, dm_id1)['code'] == AccessError.code

# def test_message_share_dm_valid(dms_setup):
#     u1, u2, dm_id1 = dms_setup
#     dm_msg_id1 = message_senddm_req(u1['token'], dm_id1, "Hey")['message_id']
#     dm_msg_id2 = message_senddm_req(u2['token'], dm_id1, "Hey")['message_id']
#     message_share_req(u1['token'], dm_msg_id1, "heyo", -1, dm_id1)
#     message_share_req(u1['token'], dm_msg_id2, "heyo", -1, dm_id1)


# def test_message_share_valid_channel(Channel_setup):
#     u1, u2, chan1_id = Channel_setup
#     channel_join_req(u2['token'], chan1_id)
#     msg_id = message_send_req(u1['token'], chan1_id, "Hi there!")['message_id']
#     message_share_req(u1['token'], msg_id, "heyo", chan1_id, -1)

# The following tests are for message_react_req
def test_message_react_invalid_token():
    clear_req()
    token = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan_id = channels_create_req(token, "Channel 1", True)['channel_id']
    msg_id = message_send_req(token, chan_id, "Hi there!")['message_id']
    assert message_react_req(7854, msg_id, 1)['code'] == AccessError.code

def test_message_react_invalid_msg_id():
    clear_req()
    token = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan_id = channels_create_req(token, "Channel 1", True)['channel_id']
    message_send_req(token, chan_id, "Hi there!")['message_id']
    assert message_react_req(token, 77, 1)['code'] == InputError.code

def test_message_react_user_not_part_of_channel():
    clear_req()
    token1 = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    token2 = auth_register_req("ann.yay@aunsw.edu.au","password","Ann","Yay")['token']
    chan_id = channels_create_req(token1, "Channel 1", True)['channel_id']
    msg_id = message_send_req(token1, chan_id, "Hi there!")['message_id']
    assert message_react_req(token2, msg_id, 1)['code'] == InputError.code

def test_message_react_user_not_part_of_dm():
    clear_req()
    token1 = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    u_id2 = auth_register_req("ann.yay@aunsw.edu.au","password","Ann","Yay")['auth_user_id']
    token3 = auth_register_req("will.ham@aunsw.edu.au","password","Will","Ham")['token']
    dm_id = dm_create_req(token1, [u_id2])['dm_id']
    dm_msg_id = message_senddm_req(token1, dm_id, "Hey")['message_id']
    assert message_react_req(token3, dm_msg_id, 1)['code'] == InputError.code

def test_message_react_invalid_react_id():
    clear_req()
    token = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan_id = channels_create_req(token, "Channel 1", True)['channel_id']
    msg_id = message_send_req(token, chan_id, "Hi there!")['message_id']
    assert message_react_req(token, msg_id, -1)['code'] == InputError.code

def test_message_react_already_reacted_channel():
    clear_req()
    token1 = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    token2 = auth_register_req("ann.yay@aunsw.edu.au","password","Ann","Yay")['token']
    chan_id = channels_create_req(token1, "Channel 1", True)['channel_id']
    channel_join_req(token2, chan_id)
    msg_id = message_send_req(token1, chan_id, "Hi there!")['message_id']
    message_react_req(token2, msg_id, 1)
    message_react_req(token1, msg_id, 1)
    assert message_react_req(token1, msg_id, 1)['code'] == InputError.code

def test_message_react_already_reacted_dm():
    clear_req()
    token1 = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    user2 = auth_register_req("ann.yay@aunsw.edu.au","password","Ann","Yay")
    dm_id = dm_create_req(token1, [user2['auth_user_id']])['dm_id']
    message_senddm_req(token1, dm_id, "Hey")
    dm_msg_id = message_senddm_req(token1, dm_id, "Hey")['message_id']
    message_react_req(user2['token'], dm_msg_id, 1)
    message_react_req(token1, dm_msg_id, 1)
    assert message_react_req(token1, dm_msg_id, 1)['code'] == InputError.code

def test_message_react_user_in_wrong_channel():
    clear_req()
    token1 = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan_id1 = channels_create_req(token1, "Channel 1", True)['channel_id']
    msg_id1 = message_send_req(token1, chan_id1, "Hi there!")['message_id']
    token2 = auth_register_req("jane.doe@aunsw.edu.au","password","Jane","Doe")['token']
    chan_id2 = channels_create_req(token2, "Channel 1", True)['channel_id']
    message_send_req(token2, chan_id2, "Hi there!")['message_id']
    assert message_react_req(token2, msg_id1, 1)['code'] == InputError.code

def test_message_react_user_in_wrong_dm():
    clear_req()
    token1 = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    u_id2 = auth_register_req("ann.yay@aunsw.edu.au","password","Ann","Yay")['auth_user_id']
    user3 = auth_register_req("john.wow@aunsw.edu.au","password","Ann","Wow")
    dm_id1 = dm_create_req(token1, [u_id2])['dm_id']
    dm_msg_id1 = message_senddm_req(token1, dm_id1, "Hey")['message_id']
    dm_id2 = dm_create_req(token1, [user3['auth_user_id']])['dm_id']
    message_senddm_req(token1, dm_id2, "Hey")['message_id']
    assert message_react_req(user3['token'], dm_msg_id1, 1)['code'] == InputError.code

# The following tests are for message_unreact_req
def test_message_unreact_invalid_token():
    clear_req()
    token = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan_id = channels_create_req(token, "Channel 1", True)['channel_id']
    msg_id = message_send_req(token, chan_id, "Hi there!")['message_id']
    message_react_req(token, msg_id, 1)
    assert message_unreact_req(634232476, msg_id, 1)['code'] == AccessError.code

def test_message_unreact_invalid_msg_id():
    clear_req()
    token = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan_id = channels_create_req(token, "Channel 1", True)['channel_id']
    msg_id = message_send_req(token, chan_id, "Hi there!")['message_id']
    message_react_req(token, msg_id, 1)
    assert message_unreact_req(token, 435, 1)['code'] == InputError.code

def test_message_unreact_user_not_in_chan():
    clear_req()
    token1 = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    token2 = auth_register_req("Bob.John@aunsw.edu.au","password","Bob","John")['token']
    chan_id = channels_create_req(token1, "Channel 1", True)['channel_id']
    msg_id = message_send_req(token1, chan_id, "Hi there!")['message_id']
    message_react_req(token1, msg_id, 1)
    assert message_unreact_req(token2, msg_id, 1)['code'] == InputError.code

def test_message_unreact_user_not_in_dm():
    clear_req()
    token1 = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    u_id2 = auth_register_req("james.smith@aunsw.edu.au","password","James","Smith")['auth_user_id']
    token3 = auth_register_req("Tim.doe@aunsw.edu.au","password","Tim","Doe")['token']
    dm_id = dm_create_req(token1, [u_id2])['dm_id']
    dm_msg_id = message_senddm_req(token1, dm_id, "Hey")['message_id']
    message_react_req(token1, dm_msg_id, 1)
    assert message_unreact_req(token3, dm_msg_id, 1)['code'] == InputError.code

def test_message_unreact_invalid_react_id():
    clear_req()
    token = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan_id = channels_create_req(token, "Channel 1", True)['channel_id']
    msg_id = message_send_req(token, chan_id, "Hi there!")['message_id']
    message_react_req(token, msg_id, 1)
    assert message_unreact_req(token, msg_id, -1)['code'] == InputError.code

def test_message_unreact_user_in_wrong_channel():
    clear_req()
    token1 = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan_id1 = channels_create_req(token1, "Channel 1", True)['channel_id']
    msg_id1 = message_send_req(token1, chan_id1, "Hi there!")['message_id']
    message_react_req(token1, msg_id1, 1)
    token2 = auth_register_req("jane.doe@aunsw.edu.au","password","Jane","Doe")['token']
    chan_id2 = channels_create_req(token2, "Channel 1", True)['channel_id']
    msg_id2 = message_send_req(token2, chan_id2, "Hi there!")['message_id']
    message_react_req(token2, msg_id2, 1)
    assert message_unreact_req(token2, msg_id1, 1)['code'] == InputError.code

def test_message_unreact_msg_not_reacted_to():
    clear_req()
    token = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan_id = channels_create_req(token, "Channel 1", True)['channel_id']
    msg_id = message_send_req(token, chan_id, "Hi there!")['message_id']
    assert message_unreact_req(token, msg_id, 1)['code'] == InputError.code

def test_message_unreact_valid_chan():
    clear_req()
    token = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan_id = channels_create_req(token, "Channel 1", True)['channel_id']
    message_send_req(token, chan_id, "Hi there!")
    msg_id = message_send_req(token, chan_id, "Hi there!")['message_id']
    message_react_req(token, msg_id, 1)
    message_unreact_req(token, msg_id, 1)

def test_message_unreact_valid_dm():
    clear_req()
    token1 = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    u_id2 = auth_register_req("james.smith@aunsw.edu.au","password","James","Smith")['auth_user_id']
    dm_id = dm_create_req(token1, [u_id2])['dm_id']
    message_senddm_req(token1, dm_id, "Hey")
    dm_msg_id = message_senddm_req(token1, dm_id, "Hey")['message_id']
    message_react_req(token1, dm_msg_id, 1)
    message_unreact_req(token1, dm_msg_id, 1)

# The following tests are for message_pin_req

def test_message_pin_invalid_token():
    clear_req()
    token = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan_id = channels_create_req(token, "Channel 1", True)['channel_id']
    msg_id = message_send_req(token, chan_id, "Hi there!")['message_id']
    assert message_pin_req(5342, msg_id)['code'] == AccessError.code

def test_message_pin_user_in_wrong_dm():
    clear_req()
    token1 = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    u_id2 = auth_register_req("james.smith@aunsw.edu.au","password","James","Smith")['auth_user_id']
    user3 = auth_register_req("Tim.doe@aunsw.edu.au","password","Tim","Doe")
    dm_id1 = dm_create_req(token1, [u_id2])['dm_id']
    dm_msg_id1 = message_senddm_req(token1, dm_id1, "Hey")['message_id']
    dm_id2 = dm_create_req(token1, [user3['auth_user_id']])['dm_id']
    message_senddm_req(token1, dm_id2, "Hey")['message_id']
    assert message_pin_req(user3['token'], dm_msg_id1)['code'] == InputError.code

def test_message_pin_user_in_wrong_channel():
    clear_req()
    token1 = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan_id1 = channels_create_req(token1, "Channel 1", True)['channel_id']
    msg_id1 = message_send_req(token1, chan_id1, "Hi there!")['message_id']
    token2 = auth_register_req("jane.doe@aunsw.edu.au","password","Jane","Doe")['token']
    chan_id2 = channels_create_req(token2, "Channel 1", True)['channel_id']
    message_send_req(token2, chan_id2, "Hi there!")['message_id']
    assert message_pin_req(token2, msg_id1)['code'] == InputError.code

def test_message_pin_invalid():
    clear_req()
    token = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan_id = channels_create_req(token, "Channel 1", True)['channel_id']
    message_send_req(token, chan_id, "Hi there!")['message_id']
    assert message_pin_req(token, -1)['code'] == InputError.code

def test_message_pin_msg_already_pinned():
    clear_req()
    token = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan_id = channels_create_req(token, "Channel 1", True)['channel_id']
    msg_id = message_send_req(token, chan_id, "Hi there!")['message_id']
    message_pin_req(token, msg_id)
    assert message_pin_req(token, msg_id)['code'] == InputError.code

def test_message_pin_user_not_owner_channel():
    clear_req()
    auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    token2 = auth_register_req("jane.doe@aunsw.edu.au","password","Jane","Doe")['token']
    token3 = auth_register_req("jack.doe@aunsw.edu.au","password","Jack","Doe")['token']
    chan_id = channels_create_req(token2, "Channel 1", True)['channel_id']
    channel_join_req(token3, chan_id)
    msg_id = message_send_req(token2, chan_id, "Hi there!")['message_id']
    assert message_pin_req(token3, msg_id)['code'] == AccessError.code

def test_message_pin_global_user_not_owner_channel():
    clear_req()
    token1 = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    token2 = auth_register_req("jane.doe@aunsw.edu.au","password","Jane","Doe")['token']
    chan_id = channels_create_req(token2, "Channel 1", True)['channel_id']
    channel_join_req(token1, chan_id)
    msg_id = message_send_req(token2, chan_id, "Hi there!")['message_id']
    message_pin_req(token1, msg_id)

def test_message_pin_user_not_owner_dm():
    clear_req()
    token1 = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    user2 = auth_register_req("james.smith@aunsw.edu.au","password","James","Smith")
    dm_id = dm_create_req(token1, [user2['auth_user_id']])['dm_id']
    dm_msg_id = message_senddm_req(token1, dm_id, "Hey")['message_id']
    assert message_pin_req(user2['token'], dm_msg_id)['code'] == AccessError.code

def test_message_pin_global_user_not_owner_dm():
    clear_req()
    user1 = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")
    token2 = auth_register_req("james.smith@aunsw.edu.au","password","James","Smith")['token']
    dm_id = dm_create_req(token2, [user1['auth_user_id']])['dm_id']
    dm_msg_id = message_senddm_req(token2, dm_id, "Hey")['message_id']
    assert message_pin_req(user1['token'], dm_msg_id)['code'] == AccessError.code

def test_message_pin_valid_chan():
    clear_req()
    token = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan_id = channels_create_req(token, "Channel 1", True)['channel_id']
    msg_id = message_send_req(token, chan_id, "Hi there!")['message_id']
    message_pin_req(token, msg_id)

def test_message_pin_valid_dm():
    clear_req()
    token1 = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    u_id2 = auth_register_req("james.smith@aunsw.edu.au","password","James","Smith")['auth_user_id']
    dm_id = dm_create_req(token1, [u_id2])['dm_id']
    dm_msg_id = message_senddm_req(token1, dm_id, "Hey")['message_id']
    message_pin_req(token1, dm_msg_id)

# The following tests are for message_unpin_req
def test_message_unpin_invalid_token():
    clear_req()
    token = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan_id = channels_create_req(token, "Channel 1", True)['channel_id']
    msg_id = message_send_req(token, chan_id, "Hi there!")['message_id']
    message_pin_req(token, msg_id)
    assert message_unpin_req(5342, msg_id)['code'] == AccessError.code

def test_message_unpin_user_in_wrong_dm():
    clear_req()
    token1 = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    u_id2 = auth_register_req("james.smith@aunsw.edu.au","password","James","Smith")['auth_user_id']
    user3 = auth_register_req("Tim.doe@aunsw.edu.au","password","Tim","Doe")
    dm_id1 = dm_create_req(token1, [u_id2])['dm_id']
    dm_msg_id1 = message_senddm_req(token1, dm_id1, "Hey")['message_id']
    dm_id2 = dm_create_req(token1, [user3['auth_user_id']])['dm_id']
    message_senddm_req(token1, dm_id2, "Hey")['message_id']
    message_pin_req(token1, dm_msg_id1)
    assert message_unpin_req(user3['token'], dm_msg_id1)['code'] == InputError.code

def test_message_unpin_user_in_wrong_channel():
    clear_req()
    token1 = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan_id1 = channels_create_req(token1, "Channel 1", True)['channel_id']
    msg_id1 = message_send_req(token1, chan_id1, "Hi there!")['message_id']
    token2 = auth_register_req("jane.doe@aunsw.edu.au","password","Jane","Doe")['token']
    chan_id2 = channels_create_req(token2, "Channel 1", True)['channel_id']
    message_send_req(token2, chan_id2, "Hi there!")['message_id']
    message_pin_req(token1, msg_id1)
    assert message_unpin_req(token2, msg_id1)['code'] == InputError.code

def test_message_unpin_invalid():
    clear_req()
    token = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan_id = channels_create_req(token, "Channel 1", True)['channel_id']
    msg_id = message_send_req(token, chan_id, "Hi there!")['message_id']
    message_pin_req(token, msg_id)
    assert message_unpin_req(token, -1)['code'] == InputError.code

def test_message_unpin_msg_not_pinned():
    clear_req()
    token = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan_id = channels_create_req(token, "Channel 1", True)['channel_id']
    msg_id = message_send_req(token, chan_id, "Hi there!")['message_id']
    message_pin_req(token, msg_id)
    message_unpin_req(token, msg_id)
    assert message_unpin_req(token, msg_id)['code'] == InputError.code

def test_message_unpin_user_not_owner_channel():
    clear_req()
    auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    token2 = auth_register_req("jane.doe@aunsw.edu.au","password","Jane","Doe")['token']
    token3 = auth_register_req("jack.doe@aunsw.edu.au","password","Jack","Doe")['token']
    chan_id = channels_create_req(token2, "Channel 1", True)['channel_id']
    channel_join_req(token3, chan_id)
    msg_id = message_send_req(token2, chan_id, "Hi there!")['message_id']
    message_pin_req(token2, msg_id)
    assert message_unpin_req(token3, msg_id)['code'] == AccessError.code

def test_message_unpin_global_user_not_owner_channel():
    clear_req()
    token1 = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    token2 = auth_register_req("jane.doe@aunsw.edu.au","password","Jane","Doe")['token']
    chan_id = channels_create_req(token2, "Channel 1", True)['channel_id']
    channel_join_req(token1, chan_id)
    msg_id = message_send_req(token2, chan_id, "Hi there!")['message_id']
    message_pin_req(token1, msg_id)
    message_unpin_req(token1, msg_id)

def test_message_unpin_user_not_owner_dm():
    clear_req()
    token1 = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    user2 = auth_register_req("james.smith@aunsw.edu.au","password","James","Smith")
    dm_id = dm_create_req(token1, [user2['auth_user_id']])['dm_id']
    dm_msg_id = message_senddm_req(token1, dm_id, "Hey")['message_id']
    message_pin_req(token1, dm_msg_id)
    assert message_unpin_req(user2['token'], dm_msg_id)['code'] == AccessError.code

def test_message_unpin_global_user_not_owner_dm():
    clear_req()
    user1 = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")
    token2 = auth_register_req("james.smith@aunsw.edu.au","password","James","Smith")['token']
    dm_id = dm_create_req(token2, [user1['auth_user_id']])['dm_id']
    dm_msg_id = message_senddm_req(token2, dm_id, "Hey")['message_id']
    message_pin_req(token2, dm_msg_id)
    assert message_unpin_req(user1['token'], dm_msg_id)['code'] == AccessError.code

def test_message_unpin_valid_chan():
    clear_req()
    token = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan_id = channels_create_req(token, "Channel 1", True)['channel_id']
    message_send_req(token, chan_id, "Hi there!")
    msg_id = message_send_req(token, chan_id, "Hi there!")['message_id']
    message_pin_req(token, msg_id)
    message_unpin_req(token, msg_id)

def test_message_unpin_valid_dm():
    clear_req()
    token1 = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    u_id2 = auth_register_req("james.smith@aunsw.edu.au","password","James","Smith")['auth_user_id']
    dm_id = dm_create_req(token1, [u_id2])['dm_id']
    dm_msg_id = message_senddm_req(token1, dm_id, "Hey")['message_id']
    message_senddm_req(token1, dm_id, "Hey")
    message_pin_req(token1, dm_msg_id)
    message_unpin_req(token1, dm_msg_id)

# # The following test are for message_send_later_req

def test_message_sendlater_channel_id_invalid():
    clear_req()
    token1 = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    time_sent = dt.datetime.timestamp(dt.datetime.now() + dt.timedelta(seconds=5))
    assert message_sendlater_req(token1, -1, "Boss", time_sent)['code'] == InputError.code

def test_message_sendlater_multi_msgs():
    clear_req()
    token1 = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    channels_create_req(token1, "Channel", True)
    channel_id = channels_create_req(token1, "Channel 1", True)['channel_id']
    time_sent1 = dt.datetime.timestamp(dt.datetime.now() + dt.timedelta(seconds=1))
    msg1_id = message_sendlater_req(token1, channel_id, "Hi there!", time_sent1)['message_id']
    time_sent2 = dt.datetime.timestamp(dt.datetime.now() + dt.timedelta(seconds=1))
    msg2_id = message_sendlater_req(token1, channel_id, "Hi there!", time_sent2)['message_id']
    time.sleep(2)
    assert msg1_id != msg2_id

def test_message_sendlater_sent_in_past():
    clear_req()
    token1 = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    channel_id = channels_create_req(token1, "Channel 1", True)['channel_id']
    time_sent = dt.datetime.timestamp(dt.datetime.now() - dt.timedelta(seconds=5))
    assert message_sendlater_req(token1, channel_id, "Hi there!", time_sent)['code'] == InputError.code

def test_message_sendlater_msg_length_too_small():
    clear_req()
    token1 = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    channel_id = channels_create_req(token1, "Channel 1", True)['channel_id']
    time_sent = (dt.datetime.timestamp(dt.datetime.now() + dt.timedelta(seconds=5)))
    assert message_sendlater_req(token1, channel_id, "", time_sent)['code'] == InputError.code

def test_message_sendlater_msg_length_too_big():
    clear_req()
    token1 = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    channel_id = channels_create_req(token1, "Channel 1", True)['channel_id']
    time_sent = dt.datetime.timestamp(dt.datetime.now() + dt.timedelta(seconds=5))
    assert message_sendlater_req(token1, channel_id, """Altruism is the principle and moral practice of concern for 
            happiness of other human beings or other animals, resulting in a quality of life both material and spiritual. 
            It is a traditional virtue in many cultures and a core aspect of various religious traditions and secular worldviews, 
            though the concept of others toward whom concern should be directed can vary among cultures and religions. 
            In an extreme case, altruism may become a synonym of selflessness, which is the opposite of selfishness. 
            The word altrusim was popularized (and possibly coined) by the French philosopher Auguste Comte in French, 
            as altruisme, for an antonym of egoism.[1][2] He derived it from the Italian altrui, which in turn was derived from Latin 
            alteri, meaning other people or somebody else.[3] Altruism in biological observations in field populations of the day organisms 
            is an individual performing an action which is at a cost to themselves (e.g., pleasure and quality of life, time, probability of 
            survival or reproduction), but benefits, either directly or indirectly, another""", time_sent)['code'] == InputError.code
    
def test_message_send_token_invalid():
    clear_req()
    token1 = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    channel_id = channels_create_req(token1, "Channel 1", True)['channel_id']
    time_sent = dt.datetime.timestamp(dt.datetime.now() + dt.timedelta(seconds=5))
    assert message_sendlater_req(78534290, channel_id, "Hi there!", time_sent)['code'] == AccessError.code

def test_message_send_user_not_part_of_channel():  # NEED TO CHECK FOR GLOBAL USERS
    clear_req()
    token1 = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    token2 = auth_register_req("jane.doe@unsw.edu.au", "password","Jane","Doe")['token']
    channel_id = channels_create_req(token1, "Channel 1", True)['channel_id']
    time_sent = dt.datetime.timestamp(dt.datetime.now() + dt.timedelta(seconds=5))
    assert message_sendlater_req(token2, channel_id, "Hi there!", time_sent)['code'] == AccessError.code

# # The following test are for message_sendlaterdm_req

def test_message_sendlaterdm_dm_id_invalid():
    clear_req()
    token1 = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    time_sent = dt.datetime.timestamp(dt.datetime.now() + dt.timedelta(seconds=5))
    assert message_sendlaterdm_req(token1, -1, "Boss", time_sent)['code'] == InputError.code

def test_message_sendlaterdm_multi_msgs():
    clear_req()
    token1 = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    u_id2 = auth_register_req("james.smith@aunsw.edu.au","password","James","Smith")['auth_user_id']
    dm_create_req(token1, [u_id2])
    dm_id = dm_create_req(token1, [u_id2])['dm_id']
    time_sent1 = dt.datetime.timestamp(dt.datetime.now() + dt.timedelta(seconds=1))
    msg1_id = message_sendlaterdm_req(token1, dm_id, "Hi there!", time_sent1)['message_id']
    time_sent2 = dt.datetime.timestamp(dt.datetime.now() + dt.timedelta(seconds=1))
    msg2_id = message_sendlaterdm_req(token1, dm_id, "Hi there!", time_sent2)['message_id']
    time.sleep(2)
    assert msg1_id != msg2_id

def test_message_sendlaterdm_sent_in_past():
    clear_req()
    token1 = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    u_id2 = auth_register_req("james.smith@aunsw.edu.au","password","James","Smith")['auth_user_id']
    dm_id = dm_create_req(token1, [u_id2])['dm_id']
    time_sent = dt.datetime.timestamp(dt.datetime.now() - dt.timedelta(seconds=5))
    assert message_sendlaterdm_req(token1, dm_id, "Hi there!", time_sent)['code'] == InputError.code

def test_message_sendlaterdm_msg_length_too_small():
    clear_req()
    token1 = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    u_id2 = auth_register_req("james.smith@aunsw.edu.au","password","James","Smith")['auth_user_id']
    dm_id = dm_create_req(token1, [u_id2])['dm_id']
    time_sent = (dt.datetime.timestamp(dt.datetime.now() + dt.timedelta(seconds=5)))
    assert message_sendlaterdm_req(token1, dm_id, "", time_sent)['code'] == InputError.code

def test_message_sendlaterdm_msg_length_too_big():
    clear_req()
    token1 = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    u_id2 = auth_register_req("james.smith@aunsw.edu.au","password","James","Smith")['auth_user_id']
    dm_id = dm_create_req(token1, [u_id2])['dm_id']
    time_sent = dt.datetime.timestamp(dt.datetime.now() + dt.timedelta(seconds=5))
    assert message_sendlaterdm_req(token1, dm_id, """Altruism is the principle and moral practice of concern for 
            happiness of other human beings or other animals, resulting in a quality of life both material and spiritual. 
            It is a traditional virtue in many cultures and a core aspect of various religious traditions and secular worldviews, 
            though the concept of others toward whom concern should be directed can vary among cultures and religions. 
            In an extreme case, altruism may become a synonym of selflessness, which is the opposite of selfishness. 
            The word altrusim was popularized (and possibly coined) by the French philosopher Auguste Comte in French, 
            as altruisme, for an antonym of egoism.[1][2] He derived it from the Italian altrui, which in turn was derived from Latin 
            alteri, meaning other people or somebody else.[3] Altruism in biological observations in field populations of the day organisms 
            is an individual performing an action which is at a cost to themselves (e.g., pleasure and quality of life, time, probability of 
            survival or reproduction), but benefits, either directly or indirectly, another""", time_sent)['code'] == InputError.code
    
def test_message_senddm_token_invalid():
    clear_req()
    token1 = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    u_id2 = auth_register_req("james.smith@aunsw.edu.au","password","James","Smith")['auth_user_id']
    dm_id = dm_create_req(token1, [u_id2])['dm_id']
    time_sent = dt.datetime.timestamp(dt.datetime.now() + dt.timedelta(seconds=5))
    assert message_sendlaterdm_req(78534290, dm_id, "Hi there!", time_sent)['code'] == AccessError.code

def test_message_send_user_not_part_of_dm():  # NEED TO CHECK FOR GLOBAL USERS
    clear_req()
    token1 = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    u_id2 = auth_register_req("james.smith@aunsw.edu.au","password","James","Smith")['auth_user_id']
    token3 = auth_register_req("jane.doe@unsw.edu.au", "password","Jane","Doe")['token']
    dm_id = dm_create_req(token1, [u_id2])['dm_id']
    time_sent = dt.datetime.timestamp(dt.datetime.now() + dt.timedelta(seconds=5))
    assert message_sendlaterdm_req(token3, dm_id, "Hi there!", time_sent)['code'] == AccessError.code
