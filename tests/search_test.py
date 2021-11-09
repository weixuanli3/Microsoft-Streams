# ''' Contains tests for search'''
# import pytest
# from src.auth import auth_register_v1
# from src.channel import channel_invite_v1, channel_join_v1, channel_messages_v1
# from src.channels import channels_create_v1
# from src.dm import dm_create_v1, dm_details_v1, dm_leave_v1, dm_messages_v1
# from src.error import InputError, AccessError
# from src.message import message_send_v1, message_senddm_v1
# from src.other import clear_v1
# from src.search import search_v1
# from src.user import user_profile_v1

# @pytest.fixture
# def def_setup():
#     clear_v1()
#     owner = auth_register_v1("john.doe@unsw.com", "bruhdems", "John", "Doe")
#     user1 = auth_register_v1("patrick.liang@unsw.com", "katrick", "Patrick", "Liang")
#     user2 = auth_register_v1("john.citizen@unsw.com", "password", "John", "Citizen")
#     return (owner, user1, user2)

# def test_invalid_token(def_setup):
#     owner, user1, user2 = def_setup
#     token = owner['token'] + user1['token'] + user2['token']
#     with pytest.raises(AccessError):
#         search_v1(token, "bruh")

# def test_invalid_query_str(def_setup):
#     owner, user1, _ = def_setup
#     own_tok = owner['token']
#     u1_tok = user1['token']
#     with pytest.raises(InputError):
#         search_v1(own_tok, "")
#     with pytest.raises(InputError):
#         search_v1(u1_tok, "a" * 1001)

# def test_correct_error_thrown(def_setup):
#     owner, _, _ = def_setup
#     own_tok = owner['token']
#     with pytest.raises(AccessError):
#         search_v1(own_tok, "")

# def test_no_matches(def_setup):
#     owner, user1, _ = def_setup
#     own_tok = owner['token']
#     u1_tok = user1['token']

#     chan_id = channels_create_v1(own_tok, "BRUHDEMS", True)['channel_id']
#     channel_join_v1(u1_tok, chan_id)
#     message_send_v1(own_tok, chan_id, "Hi Lmao how are you")
#     assert search_v1(own_tok, "asdf") == {
#         'messages': []
#     }

# def test_one_match(def_setup):
#     owner, user1, _ = def_setup
#     own_tok = owner['token']
#     u1_tok = user1['token']

#     chan_id = channels_create_v1(own_tok, "BRUHDEMS", True)['channel_id']
#     channel_join_v1(u1_tok, chan_id)
#     message_send_v1(own_tok, chan_id, "Hi Lmao how are you")
#     assert search_v1(own_tok, "lmao") == {
#         'messages': []
#     }
#     messages = channel_messages_v1(own_tok, chan_id, 0)['messages']
#     assert search_v1(own_tok, "Lmao") == {
#         'messages': messages
#     }

# def test_mult_match_one_channel(def_setup):
#     owner, user1, user2 = def_setup
#     own_tok = owner['token']
#     u1_tok = user1['token']
#     u1_id = user1['auth_user_id']
#     u2_tok = user2['token']
#     u2_id = user2['auth_user_id']
#     dm_id = dm_create_v1(own_tok, [u1_id, u2_id])['dm_id']
#     message_senddm_v1(own_tok, dm_id, "How are you all")
#     message_senddm_v1(u1_tok, dm_id, "Not too bad, you all?")
#     msg_rem = message_senddm_v1(u2_tok, dm_id, "Eh, iteration 3 is killing me")['message_id']
#     messages = dm_messages_v1(own_tok, dm_id, 0)['messages']
#     for msg in messages:
#         if msg['message_id'] == msg_rem:
#             messages.remove(msg)
#     msg_searched = search_v1(own_tok, "all")['messages']
#     for msg in messages:
#         assert msg in msg_searched

# def test_mult_match_mult_channel(def_setup):
#     owner, user1, user2 = def_setup
#     own_tok = owner['token']
#     u1_tok = user1['token']
#     u1_id = user1['auth_user_id']
#     u2_tok = user2['token']
#     u2_id = user2['auth_user_id']

#     dm_id1 = dm_create_v1(own_tok, [u1_id, u2_id])['dm_id']
#     message_senddm_v1(own_tok, dm_id1, "How are you all")
#     message_senddm_v1(u1_tok, dm_id1, "Not too bad, you all?")
#     msg_rem1 = message_senddm_v1(u2_tok, dm_id1, "Eh, iteration 3 is killing me")['message_id']

#     dm_id2 = dm_create_v1(own_tok, [u1_id])['dm_id']
#     message_senddm_v1(own_tok, dm_id2, "all of this is killing me")
#     message_senddm_v1(u1_tok, dm_id2, "wouldnt say all, just most")
#     msg_rem2 = message_senddm_v1(own_tok, dm_id2, "nah this is cbbs")['message_id']

#     messages1 = dm_messages_v1(own_tok, dm_id1, 0)['messages']
#     messages2 = dm_messages_v1(u1_tok, dm_id2, 0)['messages']

#     for msg in messages1:
#         if msg['message_id'] == msg_rem1:
#             messages1.remove(msg)
    
#     for msg in messages2:
#         if msg['message_id'] == msg_rem2:
#             messages2.remove(msg)

#     msg_searched = search_v1(own_tok, "all")['messages']
#     for msg in messages1:
#         assert msg in msg_searched
#     for msg in messages2:
#         assert msg in msg_searched

# def test_mult_match_dm_and_channel(def_setup):
#     owner, user1, user2 = def_setup
#     own_tok = owner['token']
#     u1_tok = user1['token']
#     u1_id = user1['auth_user_id']
#     u2_tok = user2['token']

#     channel_id = channels_create_v1(own_tok, "bruhdems", True)['channel_id']
#     channel_join_v1(u1_tok, channel_id)
#     channel_join_v1(u2_tok, channel_id)
#     message_send_v1(own_tok, channel_id, "How are you all")
#     message_send_v1(u1_tok, channel_id, "Not too bad, you all?")
#     msg_rem1 = message_send_v1(u2_tok, channel_id, "Eh, iteration 3 is killing me")['message_id']

#     dm_id = dm_create_v1(own_tok, [u1_id])['dm_id']
#     message_senddm_v1(own_tok, dm_id, "all of this is killing me")
#     message_senddm_v1(u1_tok, dm_id, "wouldnt say all, just most")
#     msg_rem2 = message_senddm_v1(own_tok, dm_id, "nah this is cbbs")['message_id']

#     messages1 = channel_messages_v1(own_tok, channel_id, 0)['messages']
#     messages2 = dm_messages_v1(u1_tok, dm_id, 0)['messages']

#     for msg in messages1:
#         if msg['message_id'] == msg_rem1:
#             messages1.remove(msg)
    
#     for msg in messages2:
#         if msg['message_id'] == msg_rem2:
#             messages2.remove(msg)

#     msg_searched = search_v1(own_tok, "all")['messages']
#     for msg in messages1:
#         assert msg in msg_searched
#     for msg in messages2:
#         assert msg in msg_searched

# def test_left_channel(def_setup):
#     owner, user1, user2 = def_setup
#     own_tok = owner['token']
#     u1_tok = user1['token']
#     u1_id = user1['auth_user_id']
#     u2_tok = user2['token']
#     u2_id = user2['auth_user_id']
#     dm_id = dm_create_v1(own_tok, [u1_id, u2_id])['dm_id']
#     message_senddm_v1(own_tok, dm_id, "How are you all")
#     message_senddm_v1(u1_tok, dm_id, "Not too bad, you all?")
#     msg_rem = message_senddm_v1(u2_tok, dm_id, "Eh, iteration 3 is killing me")['message_id']
#     messages = dm_messages_v1(own_tok, dm_id, 0)['messages']
#     dm_leave_v1(own_tok, dm_id)
#     for msg in messages:
#         if msg['message_id'] == msg_rem:
#             messages.remove(msg)
#     assert search_v1(own_tok, "all")['messages'] == []