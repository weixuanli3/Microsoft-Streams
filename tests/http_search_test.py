''' Contains tests for search'''
import pytest
from other_functions.request_helper_functions import *
from src.error import InputError, AccessError

@pytest.fixture
def def_setup():
    clear_req()
    owner = auth_register_req("john.doe@unsw.com", "bruhdems", "John", "Doe")
    user1 = auth_register_req("patrick.liang@unsw.com", "katrick", "Patrick", "Liang")
    user2 = auth_register_req("john.citizen@unsw.com", "password", "John", "Citizen")
    return (owner, user1, user2)

def test_invalid_token(def_setup):
    owner, user1, user2 = def_setup
    token = owner['token'] + user1['token'] + user2['token']
    assert search_req(token, "bruh")['code'] == AccessError.code

def test_invalid_query_str(def_setup):
    owner, user1, _ = def_setup
    own_tok = owner['token']
    u1_tok = user1['token']
    assert search_req(own_tok, "")['code'] == InputError.code
    assert search_req(u1_tok, "a" * 1001)['code'] == InputError.code

def test_correct_error_thrown(def_setup):
    _, _, _ = def_setup
    assert search_req(123, "")['code'] == AccessError.code

def test_no_matches(def_setup):
    owner, user1, _ = def_setup
    own_tok = owner['token']
    u1_tok = user1['token']

    chan_id = channels_create_req(own_tok, "BRUHDEMS", True)['channel_id']
    channel_join_req(u1_tok, chan_id)
    message_send_req(own_tok, chan_id, "Hi Lmao how are you")
    assert search_req(own_tok, "asdf") == {
        'messages': []
    }

def test_one_match(def_setup):
    owner, user1, _ = def_setup
    own_tok = owner['token']
    u1_tok = user1['token']

    chan_id = channels_create_req(own_tok, "BRUHDEMS", True)['channel_id']
    channel_join_req(u1_tok, chan_id)
    message_send_req(own_tok, chan_id, "Hi Lmao how are you")
    assert search_req(own_tok, "lmao") == {
        'messages': []
    }
    messages = channel_messages_req(own_tok, chan_id, 0)['messages']
    assert search_req(own_tok, "Lmao") == {
        'messages': messages
    }

def test_mult_match_one_channel(def_setup):
    owner, user1, user2 = def_setup
    own_tok = owner['token']
    u1_tok = user1['token']
    u1_id = user1['auth_user_id']
    u2_tok = user2['token']
    u2_id = user2['auth_user_id']
    dm_id = dm_create_req(own_tok, [u1_id, u2_id])['dm_id']
    message_senddm_req(own_tok, dm_id, "How are you all")
    message_senddm_req(u1_tok, dm_id, "Not too bad, you all?")
    msg_rem = message_senddm_req(u2_tok, dm_id, "Eh, iteration 3 is killing me")['message_id']
    messages = dm_messages_req(own_tok, dm_id, 0)['messages']
    for msg in messages:
        if msg['message_id'] == msg_rem:
            messages.remove(msg)
    msg_searched = search_req(own_tok, "all")['messages']
    for msg in messages:
        assert msg in msg_searched

def test_mult_match_mult_channel(def_setup):
    owner, user1, user2 = def_setup
    own_tok = owner['token']
    u1_tok = user1['token']
    u1_id = user1['auth_user_id']
    u2_tok = user2['token']
    u2_id = user2['auth_user_id']

    dm_id1 = dm_create_req(own_tok, [u1_id, u2_id])['dm_id']
    message_senddm_req(own_tok, dm_id1, "How are you all")
    message_senddm_req(u1_tok, dm_id1, "Not too bad, you all?")
    msg_rem1 = message_senddm_req(u2_tok, dm_id1, "Eh, iteration 3 is killing me")['message_id']

    dm_id2 = dm_create_req(own_tok, [u1_id])['dm_id']
    message_senddm_req(own_tok, dm_id2, "all of this is killing me")
    message_senddm_req(u1_tok, dm_id2, "wouldnt say all, just most")
    msg_rem2 = message_senddm_req(own_tok, dm_id2, "nah this is cbbs")['message_id']

    messages1 = dm_messages_req(own_tok, dm_id1, 0)['messages']
    messages2 = dm_messages_req(u1_tok, dm_id2, 0)['messages']

    for msg in messages1:
        if msg['message_id'] == msg_rem1:
            messages1.remove(msg)
    
    for msg in messages2:
        if msg['message_id'] == msg_rem2:
            messages2.remove(msg)

    msg_searched = search_req(own_tok, "all")['messages']
    for msg in messages1:
        assert msg in msg_searched
    for msg in messages2:
        assert msg in msg_searched

def test_mult_match_dm_and_channel(def_setup):
    owner, user1, user2 = def_setup
    own_tok = owner['token']
    u1_tok = user1['token']
    u1_id = user1['auth_user_id']
    u2_tok = user2['token']

    channels_create_req(u2_tok, "No one's Channel", True)

    channel_id = channels_create_req(own_tok, "bruhdems", True)['channel_id']
    channel_join_req(u1_tok, channel_id)
    channel_join_req(u2_tok, channel_id)
    message_send_req(own_tok, channel_id, "How are you all")
    message_send_req(u1_tok, channel_id, "Not too bad, you all?")
    msg_rem1 = message_send_req(u2_tok, channel_id, "Eh, iteration 3 is killing me")['message_id']

    dm_id = dm_create_req(own_tok, [u1_id])['dm_id']
    message_senddm_req(own_tok, dm_id, "all of this is killing me")
    message_senddm_req(u1_tok, dm_id, "wouldnt say all, just most")
    msg_rem2 = message_senddm_req(own_tok, dm_id, "nah this is cbbs")['message_id']

    messages1 = channel_messages_req(own_tok, channel_id, 0)['messages']
    messages2 = dm_messages_req(u1_tok, dm_id, 0)['messages']

    for msg in messages1:
        if msg['message_id'] == msg_rem1:
            messages1.remove(msg)
    
    for msg in messages2:
        if msg['message_id'] == msg_rem2:
            messages2.remove(msg)

    msg_searched = search_req(own_tok, "all")['messages']
    for msg in messages1:
        assert msg in msg_searched
    for msg in messages2:
        assert msg in msg_searched

def test_left_channel(def_setup):
    owner, user1, user2 = def_setup
    own_tok = owner['token']
    u1_tok = user1['token']
    u1_id = user1['auth_user_id']
    u2_tok = user2['token']
    u2_id = user2['auth_user_id']
    dm_id = dm_create_req(own_tok, [u1_id, u2_id])['dm_id']
    message_senddm_req(own_tok, dm_id, "How are you all")
    message_senddm_req(u1_tok, dm_id, "Not too bad, you all?")
    msg_rem = message_senddm_req(u2_tok, dm_id, "Eh, iteration 3 is killing me")['message_id']
    messages = dm_messages_req(own_tok, dm_id, 0)['messages']
    dm_leave_req(own_tok, dm_id)
    for msg in messages:
        if msg['message_id'] == msg_rem:
            messages.remove(msg)
    assert search_req(own_tok, "all")['messages'] == []