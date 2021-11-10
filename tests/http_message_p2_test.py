# '''Contains some http tests for message.py'''
# import pytest
# import requests
# import json
# import datetime as dt
# import datetime
# from datetime import datetime
# from src.error import AccessError, InputError
# from other_functions.request_helper_functions import *
# from src.config import url

# @pytest.fixture
# def default_setup():
#     clear_req()
#     u1 = auth_register_req("patrick.liang@unsw.com", "katrick", "Patrick", "Liang")
#     u2 = auth_register_req("john.citizen@unsw.com", "password", "John", "Citizen")
#     return (u1, u2)

# @pytest.fixture
# def Channel_setup(default_setup):
#     u1, u2 = default_setup
#     u1_tok = u1['token']
#     chan1_id = channels_create_req(u1_tok, "Channel 1", True)['channel_id']
#     return (u1, u2, chan1_id)


# @pytest.fixture
# def dms_setup(default_setup):
#     u1, u2 = default_setup
#     u1_tok = u1['token']
#     u2_tok = u2['token']
#     u2_id = u2['auth_user_id']
#     dm_id1 = dm_create_req(u1_tok, [u2_id])['dm_id']
#     return (u1, u2, dm_id1)

# ## NEED TO CHECK WHEN BOTH INCPUT AND ACCESS ERRORS ARE SPIT OUT

# ## The following tests are for message_share
        
# # def test_message_share_invalid_token(Channel_setup):
# #     u1, u2, chan1_id = Channel_setup
# #     channel_join_req(u2['token'], chan1_id)
# #     msg_id = message_send_req(u1['token'], chan1_id, "Hi there!")['message_id']
# #     assert message_share_req(444, msg_id, "heyo", chan1_id, -1)['code'] == AccessError.code

# # def test_message_share_idm_and_chan_id_neg(Channel_setup):
# #     u1, u2, chan1_id = Channel_setup
# #     channel_join_req(u2['token'], chan1_id)
# #     msg_id = message_send_req(u1['token'], chan1_id, "Hi there!")['message_id']
# #     assert message_share_req(u1['token'], msg_id, "heyo", -1, -1)['code'] == InputError.code    

# # def test_message_share_invalid_chan_id(Channel_setup):
# #     u1, u2, chan1_id = Channel_setup
# #     channel_join_req(u2['token'], chan1_id)
# #     msg_id = message_send_req(u1['token'], chan1_id, "Hi there!")['message_id']
# #     assert message_share_req(u1['token'], msg_id, "heyo", 33, -1)['code'] == InputError.code  

# # def test_message_share_invalid_dm_id(dms_setup):
# #     u1, u2, dm_id1 = dms_setup
# #     dm_msg_id = message_senddm_req(u1['token'], dm_id1, "Hey")['message_id']
# #     assert message_share_req(u1['token'], dm_msg_id, "heyo", -1, 66)['code'] == InputError.code

# # def test_message_share_invalid_dm_and_chan_id(dms_setup):
# #     u1, u2, dm_id1 = dms_setup
# #     dm_msg_id = message_senddm_req(u1['token'], dm_id1, "Hey")['message_id']
# #     u1_tok = u1['token']
# #     chan1_id = channels_create_req(u1_tok, "Channel 1", True)['channel_id']
# #     msg_id = message_send_req(u1['token'], chan1_id, "Hi there!")['message_id']
# #     assert message_share_req(u1['token'], msg_id, "heyo", 77, 66)['code'] == InputError.code 
# #     assert message_share_req(u1['token'], dm_msg_id, "heyo", 77, 66)['code'] == InputError.code 

# # def test_message_share_invalid_dm_msg_id(dms_setup):
# #     u1, u2, dm_id1 = dms_setup
# #     dm_msg_id = message_senddm_req(u1['token'], dm_id1, "Hey")['message_id']
# #     assert message_share_req(u1['token'], 33, "heyo", -1, dm_id1)['code'] == InputError.code

# # def test_message_share_invalid_msg_id(Channel_setup):
# #     u1, u2, chan1_id = Channel_setup
# #     channel_join_req(u2['token'], chan1_id)
# #     message_send_req(u1['token'], chan1_id, "Hi there!")['message_id']
# #     assert message_share_req(u1['token'], 44, "heyo", chan1_id, -1)['code'] == InputError.code
        
# # def test_message_share_more_than_100_chars(Channel_setup):
# #     u1, u2, chan1_id = Channel_setup
# #     channel_join_req(u2['token'], chan1_id)
# #     msg_id = message_send_req(u1['token'], chan1_id, "Hi there!")['message_id']
# #     assert message_share_req(u1['token'], msg_id, """
# #                         Hey Thereivbfriehuferhuifferhuierfihuerfiphuerfpihuerfphuierfpihuer
# #                         fiphuerfihuperfpppppppppppppppppppppppppppppppppppppppppppppppppppppp
# #                         pppppppppppppppppppppppppppppppppppppppppppppppppppppppppppprefihuopppp
# #                         pppppppppppiooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# #                         oooooooooooooooooooooooooooooooooooooooooooooooooooooooooiiiiiiiiiiiii
# #                         iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
# #                         iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
# #                         iiiiiiiiiiiiiiiiii HeyThereivbfriehuferhuifferhuierfihuerfiphuerfpihuer
# #                         fphuierfpihuerfiphuerfihuperfpppppppppppppppppppppppppppppppppppppppppp
# #                         pppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp
# #                         refihuopppppppppppppppiooooooooooooooooooooooooooooooooooooooooooooooooo
# #                         oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooiiiiii
# #                         iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
# #                         iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
# #                         iiiiiiiiiiiiiiiiiii""", chan1_id, -1)['code'] == InputError.code

# # def test_message_share_user_not_in_chan(Channel_setup):
# #     u1, u2, chan1_id = Channel_setup
# #     msg_id = message_send_req(u1['token'], chan1_id, "Hi there!")['message_id']
# #     assert message_share_req(u2['token'], msg_id, "heyo", chan1_id, -1)['code'] == AccessError.code

# # def test_message_share_user_not_in_dm(dms_setup):
# #     u1, u2, dm_id1 = dms_setup
# #     dm_msg_id = message_senddm_req(u1['token'], dm_id1, "Hey")['message_id']
# #     dm_msg_id2 = message_senddm_req(u2['token'], dm_id1, "Hey")['message_id']
# #     u3 = auth_register_req("gooba.smith@unsw.com", "password", "Gooba", "Smoth")
# #     assert message_share_req(u3['token'], dm_msg_id, "heyo", -1, dm_id1)['code'] == AccessError.code
# #     assert message_share_req(u3['token'], dm_msg_id2, "heyo", -1, dm_id1)['code'] == AccessError.code

# # def test_message_share_dm_valid(dms_setup):
# #     u1, u2, dm_id1 = dms_setup
# #     dm_msg_id1 = message_senddm_req(u1['token'], dm_id1, "Hey")['message_id']
# #     dm_msg_id2 = message_senddm_req(u2['token'], dm_id1, "Hey")['message_id']
# #     message_share_req(u1['token'], dm_msg_id1, "heyo", -1, dm_id1)
# #     message_share_req(u1['token'], dm_msg_id2, "heyo", -1, dm_id1)


# # def test_message_share_valid_channel(Channel_setup):
# #     u1, u2, chan1_id = Channel_setup
# #     channel_join_req(u2['token'], chan1_id)
# #     msg_id = message_send_req(u1['token'], chan1_id, "Hi there!")['message_id']
# #     message_share_req(u1['token'], msg_id, "heyo", chan1_id, -1)
    
# # The following tests are for message_react_v1

# def test_message_react_invalid_token(Channel_setup):
#     u1, u2, chan1_id = Channel_setup
#     channel_join_req(u2['token'], chan1_id)
#     msg_id = message_send_req(u1['token'], chan1_id, "Hi there!")['message_id']
#     assert message_react_req(7854, msg_id, 1)['code'] == AccessError.code

# def test_message_react_invalid_msg_id(Channel_setup):
#     u1, u2, chan1_id = Channel_setup
#     channel_join_req(u2['token'], chan1_id)
#     message_send_req(u1['token'], chan1_id, "Hi there!")['message_id']
#     assert message_react_req(u1['token'], 77, 1)['code'] == InputError.code

# def test_message_react_user_not_part_of_channel(Channel_setup):
#     u1, u2, chan1_id = Channel_setup
#     msg_id = message_send_req(u1['token'], chan1_id, "Hi there!")['message_id']
#     assert message_react_req(u2['token'], msg_id, 1)['code'] == InputError.code

# def test_message_react_user_not_part_of_dm(dms_setup):
#     u1, u2, dm_id1 = dms_setup
#     dm_msg_id = message_senddm_req(u1['token'], dm_id1, "Hey")['message_id']
#     dm_msg_id2 = message_senddm_req(u2['token'], dm_id1, "Hey")['message_id']
#     u3 = auth_register_req("gooba.smith@unsw.com", "password", "Gooba", "Smoth")
#     assert message_react_req(u3['token'], dm_msg_id, 1)['code'] == InputError.code
#     assert message_react_req(u3['token'], dm_msg_id2, 1)['code'] == InputError.code

# def test_message_react_invalid_react_id(Channel_setup):
#     u1, u2, chan1_id = Channel_setup
#     channel_join_req(u2['token'], chan1_id)
#     msg_id = message_send_req(u1['token'], chan1_id, "Hi there!")['message_id']
#     assert message_react_req(u1['token'], msg_id, -1)['code'] == InputError.code

# def test_message_react_already_reacted(Channel_setup):
#     u1, u2, chan1_id = Channel_setup
#     channel_join_req(u2['token'], chan1_id)
#     msg_id = message_send_req(u1['token'], chan1_id, "Hi there!")['message_id']
#     message_react_req(u1['token'], msg_id, 1)
#     assert message_react_req(u1['token'], msg_id, 1)['code'] == InputError.code

# def test_message_react_user_in_wrong_channel(Channel_setup):
#     u1, u2, chan1_id = Channel_setup
#     channel_join_req(u2['token'], chan1_id)
#     u3 = auth_register_req("tim.zoom@unsw.com", "password", "Tim", "Zoom")
#     chan2_id = channels_create_req(u3['token'], "Channel 1", True)['channel_id']
#     msg_id = message_send_req(u1['token'], chan1_id, "Hi there!")['message_id']
#     message_send_req(u3['token'], chan2_id, "Hi there!")['message_id']
#     assert message_react_req(u3['token'], msg_id, 1)['code'] == InputError.code

# def test_message_react_user_not_part_of_dm(dms_setup):
#     u1, u2, dm_id1 = dms_setup
#     dm_msg_id = message_senddm_req(u1['token'], dm_id1, "Hey")['message_id']
#     u3 = auth_register_req("gooba.smith@unsw.com", "password", "Gooba", "Smoth")
#     dm_id2 = dm_create_req(u3['token'], [u1['auth_user_id']])['dm_id']
#     message_senddm_req(u3['token'], dm_id2, "Hey")
#     assert message_react_req(u3['token'], dm_msg_id, 1)['code'] == InputError.code

# def test_message_react_valid_channel(Channel_setup):
#     u1, u2, chan1_id = Channel_setup
#     channel_join_req(u2['token'], chan1_id)
#     msg_id = message_send_req(u1['token'], chan1_id, "Hi there!")['message_id']
#     message_react_req(u1['token'], msg_id, 1)

# def test_message_react_valid_dm(dms_setup):
#     u1, u2, dm_id1 = dms_setup
#     dm_msg_id = message_senddm_req(u1['token'], dm_id1, "Hey")['message_id']
#     message_react_req(u1['token'], dm_msg_id, 1)
        
# # The following tests are for message_unreact_v1

# def test_message_unreact_invalid_token(Channel_setup):
#     u1, u2, chan1_id = Channel_setup
#     channel_join_req(u2['token'], chan1_id)
#     msg_id = message_send_req(u1['token'], chan1_id, "Hi there!")['message_id']
#     message_react_req(u1['token'], msg_id, 1)
#     assert message_unreact_req(634232476, msg_id, 1)['code'] == AccessError.code

# def test_message_unreact_invalid_msg_id(Channel_setup):
#     u1, u2, chan1_id = Channel_setup
#     channel_join_req(u2['token'], chan1_id)
#     msg_id = message_send_req(u1['token'], chan1_id, "Hi there!")['message_id']
#     message_react_req(u1['token'], msg_id, 1)
#     assert message_unreact_req(u1['token'], 435, 1)['code'] == InputError.code

# def test_message_unreact_user_not_in_chan(Channel_setup):
#     u1, u2, chan1_id = Channel_setup
#     msg_id = message_send_req(u1['token'], chan1_id, "Hi there!")['message_id']
#     message_react_req(u1['token'], msg_id, 1)
#     assert message_unreact_req(u2['token'], msg_id, 1)['code'] == InputError.code

# def test_message_unreact_user_not_in_dm(dms_setup):
#     u1, u2, dm_id1 = dms_setup
#     dm_msg_id = message_senddm_req(u1['token'], dm_id1, "Hey")['message_id']
#     dm_msg_id2 = message_senddm_req(u2['token'], dm_id1, "Hey")['message_id']
#     u3 = auth_register_req("gooba.smith@unsw.com", "password", "Gooba", "Smoth")
#     message_unreact_req(u1['token'], dm_msg_id, 1)
#     message_unreact_req(u2['token'], dm_msg_id2, 1)
#     assert message_unreact_req(u3['token'], dm_msg_id, 1)['code'] == InputError.code
#     assert message_unreact_req(u3['token'], dm_msg_id2, 1)['code'] == InputError.code

# def test_message_unreact_invalid_react_id(Channel_setup):
#     u1, u2, chan1_id = Channel_setup
#     channel_join_req(u2['token'], chan1_id)
#     msg_id = message_send_req(u1['token'], chan1_id, "Hi there!")['message_id']
#     message_react_req(u1['token'], msg_id, 1)
#     assert message_unreact_req(u1['token'], msg_id, -1)['code'] == AccessError.code

# def test_message_unreact_user_in_wrong_channel(Channel_setup):
#     u1, u2, chan1_id = Channel_setup
#     channel_join_req(u2['token'], chan1_id)
#     u3 = auth_register_req("tim.zoom@unsw.com", "password", "Tim", "Zoom")
#     chan2_id = channels_create_req(u3['token'], "Channel 1", True)['channel_id']
#     msg_id = message_send_req(u1['token'], chan1_id, "Hi there!")['message_id']
#     message_react_req(u1['token'], msg_id, 1)
#     message_send_req(u3['token'], chan2_id, "Hi there!")['message_id']
#     assert message_unreact_req(u3['token'], msg_id, 1)['code'] == InputError.code

# def test_message_unreact_msg_not_reacted_to(Channel_setup):
#     u1, u2, chan1_id = Channel_setup
#     channel_join_req(u2['token'], chan1_id)
#     msg_id = message_send_req(u1['token'], chan1_id, "Hi there!")['message_id']
#     assert message_unreact_req(u1['token'], msg_id, 1)['code'] == InputError.code

# def test_message_unreact_valid_chan(Channel_setup):
#     u1, u2, chan1_id = Channel_setup
#     channel_join_req(u2['token'], chan1_id)
#     msg_id = message_send_req(u1['token'], chan1_id, "Hi there!")['message_id']
#     message_react_req(u1['token'], msg_id, 1)
#     message_unreact_req(u1['token'], msg_id, 1)

# def test_message_unreact_valid_dm(dms_setup):
#     u1, u2, dm_id1 = dms_setup
#     dm_msg_id = message_senddm_req(u1['token'], dm_id1, "Hey")['message_id']
#     message_react_req(u1['token'], dm_msg_id, 1)
#     message_unreact_req(u1['token'], dm_msg_id, 1)

# # The following tests are for message_pin_v1

# def test_message_pin_invalid_token(Channel_setup):
#     u1, u2, chan1_id = Channel_setup
#     channel_join_req(u2['token'], chan1_id)
#     msg_id = message_send_req(u1['token'], chan1_id, "Hi there!")['message_id']
#     assert message_pin_req(5342, msg_id)['code'] == AccessError.code

# def test_message_pin_user_in_wrong_dm(dms_setup):
#     u1, u2, dm_id1 = dms_setup
#     dm_msg_id = message_senddm_req(u1['token'], dm_id1, "Hey")['message_id']
#     u3 = auth_register_req("gooba.smith@unsw.com", "password", "Gooba", "Smoth")
#     dm_id2 = dm_create_req(u3['token'], [u1['auth_user_id']])['dm_id']
#     message_senddm_req(u3['token'], dm_id2, "Hey")
#     assert message_pin_req(u3['token'], dm_msg_id)['code'] == InputError.code

# def test_message_pin_user_in_wrong_channel(Channel_setup):
#     u1, u2, chan1_id = Channel_setup
#     channel_join_req(u2['token'], chan1_id)
#     u3 = auth_register_req("tim.zoom@unsw.com", "password", "Tim", "Zoom")
#     chan2_id = channels_create_req(u3['token'], "Channel 1", True)['channel_id']
#     msg_id = message_send_req(u1['token'], chan1_id, "Hi there!")['message_id']
#     message_send_req(u3['token'], chan2_id, "Hi there!")['message_id']
#     assert message_pin_req(u3['token'], msg_id)['code'] == InputError.code

# def test_message_pin_invalid_msg_id(Channel_setup):
#     u1, u2, chan1_id = Channel_setup
#     channel_join_req(u2['token'], chan1_id)
#     message_send_req(u1['token'], chan1_id, "Hi there!")['message_id']
#     assert message_pin_req(u1['token'], -1)['code'] == InputError.code

# def test_message_pin_msg_already_pinned(Channel_setup):
#     u1, u2, chan1_id = Channel_setup
#     channel_join_req(u2['token'], chan1_id)
#     msg_id = message_send_req(u1['token'], chan1_id, "Hi there!")['message_id']
#     message_pin_req(u1['token'], msg_id)
#     assert message_pin_req(u1['token'], msg_id)['code'] == InputError.code

# def test_message_pin_user_not_owner_channel(Channel_setup):
#     u1, u2, chan1_id = Channel_setup
#     channel_join_req(u2['token'], chan1_id)
#     msg_id = message_send_req(u1['token'], chan1_id, "Hi there!")['message_id']
#     assert message_pin_req(u2['token'], msg_id)['code'] == AccessError.code

# def test_message_pin_global_user_not_owner_channel(default_setup):
#     u1, u2 = default_setup
#     chan1_id = channels_create_req(u2['token'], "Channel 1", True)['channel_id']
#     channel_join_req(u1['token'], chan1_id)
#     msg_id = message_send_req(u2['token'], chan1_id, "Hi there!")['message_id']
#     message_pin_req(u1['token'], msg_id)

# def test_message_pin_user_not_owner_dm(default_setup):
#     u1, u2 = default_setup
#     dm_id1 = dm_create_req(u1['token'], u2['auth_user_id'])['dm_id']
#     dm_msg_id = message_senddm_req(u1['token'], dm_id1, "Hey")['message_id']
#     assert message_pin_req(u2['token'], dm_msg_id)['code'] == AccessError.code


# def test_message_pin_global_user_not_owner_dm(default_setup):
#     u1, u2 = default_setup
#     dm_id1 = dm_create_req(u2['token'], [u1['auth_user_id']])['dm_id']
#     dm_msg_id = message_senddm_req(u1['token'], dm_id1, "Hey")['message_id']
#     message_pin_req(u1['token'], dm_msg_id)

# def test_message_pin_valid_chan(Channel_setup):
#     u1, u2, chan1_id = Channel_setup
#     channel_join_req(u2['token'], chan1_id)
#     msg_id = message_send_req(u1['token'], chan1_id, "Hi there!")['message_id']
#     message_react_req(u1['token'], msg_id, 1)
#     message_pin_req(u1['token'], msg_id)

# def test_message_pin_valid_dm(dms_setup):
#     u1, u2, dm_id1 = dms_setup
#     dm_msg_id = message_senddm_req(u1['token'], dm_id1, "Hey")['message_id']
#     message_pin_req(u1['token'], dm_msg_id)

    
# # The following tests are for message_unpin_v1

# def test_message_unpin_invalid_token(Channel_setup):
#     u1, u2, chan1_id = Channel_setup
#     channel_join_req(u2['token'], chan1_id)
#     msg_id = message_send_req(u1['token'], chan1_id, "Hi there!")['message_id']
#     message_pin_req(u1['token'], msg_id)
#     assert message_unpin_req(5342, msg_id)['code'] == AccessError.code

# def test_message_unpin_user_in_wrong_dm(dms_setup):
#     u1, u2, dm_id1 = dms_setup
#     dm_msg_id = message_senddm_req(u1['token'], dm_id1, "Hey")['message_id']
#     u3 = auth_register_req("gooba.smith@unsw.com", "password", "Gooba", "Smoth")
#     dm_id2 = dm_create_req(u3['token'], [u1['auth_user_id']])['dm_id']
#     message_senddm_req(u3['token'], dm_id2, "Hey")
#     message_pin_req(u1['token'], dm_msg_id)
#     assert message_unpin_req(u3['token'], dm_msg_id)['code'] == InputError.code

# def test_message_unpin_user_in_wrong_channel(Channel_setup):
#     u1, u2, chan1_id = Channel_setup
#     channel_join_req(u2['token'], chan1_id)
#     u3 = auth_register_req("tim.zoom@unsw.com", "password", "Tim", "Zoom")
#     chan2_id = channels_create_req(u3['token'], "Channel 1", True)['channel_id']
#     msg_id = message_send_req(u1['token'], chan1_id, "Hi there!")['message_id']
#     message_send_req(u3['token'], chan2_id, "Hi there!")['message_id']
#     message_pin_req(u1['token'], msg_id)
#     assert message_unpin_req(u3['token'], msg_id)['code'] == InputError.code

# def test_message_unpin_invalid(Channel_setup):
#     u1, u2, chan1_id = Channel_setup
#     channel_join_req(u2['token'], chan1_id)
#     msg_id = message_send_req(u1['token'], chan1_id, "Hi there!")['message_id']
#     message_pin_req(u1['token'], msg_id)
#     assert message_unpin_req(u1['token'], -1)['code'] == InputError.code

# def test_message_unpin_msg_not_pinned(Channel_setup):
#     u1, u2, chan1_id = Channel_setup
#     channel_join_req(u2['token'], chan1_id)
#     msg_id = message_send_req(u1['token'], chan1_id, "Hi there!")['message_id']
#     assert message_unpin_req(u1['token'], msg_id)['code'] == InputError.code

# def test_message_unpin_user_not_owner_channel(Channel_setup):
#     u1, u2, chan1_id = Channel_setup
#     channel_join_req(u2['token'], chan1_id)
#     msg_id = message_send_req(u1['token'], chan1_id, "Hi there!")['message_id']
#     message_pin_req(u1['token'], msg_id)
#     assert message_pin_req(u2['token'], msg_id)['code'] == AccessError.code

# def test_message_unpin_global_user_not_owner_channel(default_setup):
#     u1, u2 = default_setup
#     chan1_id = channels_create_req(u2['token'], "Channel 1", True)['channel_id']
#     channel_join_req(u1['token'], chan1_id)
#     msg_id = message_send_req(u2['token'], chan1_id, "Hi there!")['message_id']
#     message_pin_req(u2['token'], msg_id)
#     message_unpin_req(u1['token'], msg_id)

# def test_message_unpin_user_not_owner_dm(default_setup):
#     u1, u2 = default_setup
#     dm_id1 = dm_create_req(u1['token'], u2['auth_user_id'])['dm_id']
#     dm_msg_id = message_senddm_req(u1['token'], dm_id1, "Hey")['message_id']
#     message_pin_req(u1['token'], dm_msg_id)
#     assert message_unpin_req(u2['token'], dm_msg_id)['code'] == AccessError.code

# def test_message_unpin_global_user_not_owner_dm(default_setup):
#     u1, u2 = default_setup
#     dm_id1 = dm_create_req(u2['token'], [u1['auth_user_id']])['dm_id']
#     dm_msg_id = message_senddm_req(u1['token'], dm_id1, "Hey")['message_id']
#     message_pin_req(u2['token'], dm_msg_id)
#     assert message_unpin_req(u1['token'], dm_msg_id)['code'] == AccessError.code

# def test_message_unpin_valid_chan(Channel_setup):
#     u1, u2, chan1_id = Channel_setup
#     channel_join_req(u2['token'], chan1_id)
#     msg_id = message_send_req(u1['token'], chan1_id, "Hi there!")['message_id']
#     message_react_req(u1['token'], msg_id, 1)
#     message_pin_req(u1['token'], msg_id)
#     message_unpin_req(u1['token'], msg_id)
    
# def test_message_unpin_valid_dm():
#     clear_v1()
#     token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
#     u_id2 = auth_register_v1("james.smith@aunsw.edu.au","password","James","Smith")['auth_user_id']
#     dm_id = dm_create_v1(token1, [u_id2])['dm_id']
#     dm_msg_id = message_senddm_v1(token1, dm_id, "Hey")['message_id']
#     message_pin_v1(token1, dm_msg_id)
#     message_unpin_v1(token1, dm_msg_id)

# def test_message_unpin_valid_dm(dms_setup):
#     u1, u2, dm_id1 = dms_setup
#     dm_msg_id = message_senddm_req(u1['token'], dm_id1, "Hey")['message_id']
#     message_pin_req(u1['token'], dm_msg_id)
#     message_unpin_req(u1['token'], dm_msg_id)


# # The following test are for message_send_later_v1

# def test_message_sendlater_invalid_token(Channel_setup):
#     u1, u2, chan1_id = Channel_setup
#     channel_join_req(u2['token'], chan1_id)
#     assert message_sendlater_req(3434, chan1_id, "Boss", datetime.timestamp(datetime.now()))['code'] == AccessError.code
    

# def test_message_sendlater_channel_id_invalid():
#     u1 = auth_register_req("patrick.liang@unsw.com", "katrick", "Patrick", "Liang")
#     assert message_sendlater_req(u1['token'], -1, "Boss", datetime.timestamp(datetime.now()))['code'] == InputError.code

# def test_message_sendlater_multi_msgs(Channel_setup):
#     u1, u2, chan1_id = Channel_setup
#     channel_join_req(u2['token'], chan1_id)
#     msg_id1 = message_sendlater_req(u1['token'], chan1_id, "Boss", datetime.timestamp(datetime.now()))['message_id']
#     msg_id2 = message_sendlater_req(u1['token'], chan1_id, "Boss", datetime.timestamp(datetime.now()))['message_id']
#     assert msg1_id != msg2_id

# def test_message_sendlater_sent_in_past(Channel_setup):
#     u1, u2, chan1_id = Channel_setup
#     channel_join_req(u2['token'], chan1_id)
#     assert message_sendlater_req(u1['token'], chan1_id, "Boss", dt.datetime(2000, 1, 1).timestamp())['code'] == InputError.code

# # def test_message_sendlater_msg_length_too_small(Channel_setup):
# #     u1, u2, chan1_id = Channel_setup
# #     channel_join_req(u2['token'], chan1_id)
# #     assertmessage_sendlater_req(u1['token'], chan1_id, "", datetime.timestamp(datetime.now()))['code'] == InputError.code

# def test_message_sendlater_msg_length_too_big(Channel_setup):
#     u1, u2, chan1_id = Channel_setup
#     channel_join_req(u2['token'], chan1_id)
#     assert message_sendlater_req(u1['token'], chan1_id, """Altruism is the principle and moral practice of concern for 
#             happiness of other human beings or other animals, resulting in a quality of life both material and spiritual. 
#             It is a traditional virtue in many cultures and a core aspect of various religious traditions and secular worldviews, 
#             though the concept of others toward whom concern should be directed can vary among cultures and religions. 
#             In an extreme case, altruism may become a synonym of selflessness, which is the opposite of selfishness. 
#             The word altrusim was popularized (and possibly coined) by the French philosopher Auguste Comte in French, 
#             as altruisme, for an antonym of egoism.[1][2] He derived it from the Italian altrui, which in turn was derived from Latin 
#             alteri, meaning other people or somebody else.[3] Altruism in biological observations in field populations of the day organisms 
#             is an individual performing an action which is at a cost to themselves (e.g., pleasure and quality of life, time, probability of 
#             survival or reproduction), but benefits, either directly or indirectly, another""", datetime.timestamp(datetime.now()))['code'] == InputError.code

# def test_message_send_user_not_part_of_channel(default_setup): # NEED TO CHECK FOR GLOBAL USERS
#     u1, u2 = default_setup
#     chan1_id = channels_create_req(u1['token'], "Channel 1", True)['channel_id']
#     assert message_sendlater_req(u2['token'], chan1_id, "Boss", datetime.timestamp(datetime.now()))['code'] == AccessError.code
