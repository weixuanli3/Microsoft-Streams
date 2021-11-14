'''Contains tests for message.py'''
import pytest
import datetime as dt

from src.auth import auth_register_v1
from src.channels import channels_create_v1, channels_list_v1, channels_listall_v1
from src.channel import channel_join_v1, channel_invite_v1
from src.dm import dm_create_v1
from src.error import InputError
from src.error import AccessError
from src.other import clear_v1
from src.message import message_send_v1, message_edit_v1, message_send_v1, message_senddm_v1, message_remove_v1, message_share_v1
from src.message_react import message_react_v1, message_unreact_v1 
from src.message_pin import message_pin_v1, message_unpin_v1 
from src.message_later import message_sendlater_v1, message_sendlaterdm_v1

# NEED TO CHECK WHEN BOTH INPUT AND ACCESS ERRORS ARE SPIT OUT

# The following tests are for message_share

def test_message_share_invalid_token():
    clear_v1()
    token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    channel_id = channels_create_v1(token, "Channel 1", True)['channel_id']
    msg_id = message_send_v1(token, channel_id, "Hi there!")['message_id']
    with pytest.raises(AccessError):
        message_share_v1(444, msg_id, "heyo", channel_id, -1)
        
def test_message_share_idm_and_chan_id_neg():
    clear_v1()
    token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    channel_id = channels_create_v1(token, "Channel 1", True)['channel_id']
    msg_id = message_send_v1(token, channel_id, "Hi there!")['message_id']
    with pytest.raises(InputError):
        message_share_v1(token, msg_id, "heyo", -1, -1)

def test_message_share_invalid_chan_id():
    clear_v1()
    token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    channel_id = channels_create_v1(token, "Channel 1", True)['channel_id']
    msg_id = message_send_v1(token, channel_id, "Hi there!")['message_id']
    with pytest.raises(InputError):
        message_share_v1(token, msg_id, "heyo", 33, -1)
        

def test_message_share_invalid_dm_id():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    u_id2 = auth_register_v1("james.smith@aunsw.edu.au","password","James","Smith")['auth_user_id']
    dm_id = dm_create_v1(token1, [u_id2])['dm_id']
    dm_msg_id = message_senddm_v1(token1, dm_id, "Hey")['message_id']
    with pytest.raises(InputError):
        message_share_v1(token1, dm_msg_id, "heyo", -1, 66)
        
def test_message_share_invalid_dm_and_chan_id():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    u_id2 = auth_register_v1("james.smith@aunsw.edu.au","password","James","Smith")['auth_user_id']
    channel_id = channels_create_v1(token1, "Channel 1", True)['channel_id']
    dm_id = dm_create_v1(token1, [u_id2])['dm_id']
    msg_id = message_send_v1(token1, channel_id, "Hi there!")['message_id']
    dm_msg_id = message_senddm_v1(token1, dm_id, "Hey")['message_id']
    with pytest.raises(InputError):
        message_share_v1(token1, msg_id, "heyo", 77, 66)
    with pytest.raises(InputError):
        message_share_v1(token1, dm_msg_id, "heyo", 77, 66)
        
def test_message_share_invalid_dm_msg_id():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    u_id2 = auth_register_v1("james.smith@aunsw.edu.au","password","James","Smith")['auth_user_id']
    dm_id = dm_create_v1(token1, [u_id2])['dm_id']
    message_senddm_v1(token1, dm_id, "Hey")['message_id']
    with pytest.raises(InputError):
        message_share_v1(token1, 33, "heyo", -1, dm_id)
        
def test_message_share_invalid_msg_id():
    clear_v1()
    token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan_id = channels_create_v1(token, "Channel 1", True)['channel_id']
    message_send_v1(token, chan_id, "Hi there!")['message_id']
    with pytest.raises(InputError):
        message_share_v1(token, 44, "heyo", chan_id, -1)
        
def test_message_share_more_than_100_chars():
    clear_v1()
    token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan_id = channels_create_v1(token, "Channel 1", True)['channel_id']
    msg_id = message_send_v1(token, chan_id, "Hi there!")['message_id']
    with pytest.raises(InputError):
        message_share_v1(token, msg_id, """
                        Hey Thereivbfriehuferhuifferhuierfihuerfiphuerfpihuerfphuierfpihuer
                        fiphuerfihuperfpppppppppppppppppppppppppppppppppppppppppppppppppppppp
                        pppppppppppppppppppppppppppppppppppppppppppppppppppppppppppprefihuopppp
                        pppppppppppiooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
                        oooooooooooooooooooooooooooooooooooooooooooooooooooooooooiiiiiiiiiiiii
                        iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
                        iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
                        iiiiiiiiiiiiiiiiii HeyThereivbfriehuferhuifferhuierfihuerfiphuerfpihuer
                        fphuierfpihuerfiphuerfihuperfpppppppppppppppppppppppppppppppppppppppppp
                        pppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp
                        refihuopppppppppppppppiooooooooooooooooooooooooooooooooooooooooooooooooo
                        oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooiiiiii
                        iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
                        iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
                        iiiiiiiiiiiiiiiiiii""", chan_id, -1)

def test_message_share_user_not_in_chan():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    token2 = auth_register_v1("James.Smith@aunsw.edu.au","password","James","Smith")['token']
    chan_id = channels_create_v1(token1, "Channel 1", True)['channel_id']
    msg_id = message_send_v1(token1, chan_id, "Hi there!")['message_id']
    with pytest.raises(AccessError):
        message_share_v1(token2, msg_id, "heyo", chan_id, -1)
        
def test_message_share_user_not_in_dm():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    u_id2 = auth_register_v1("james.smith@aunsw.edu.au","password","James","Smith")['auth_user_id']
    token3 = auth_register_v1("Tim.doe@aunsw.edu.au","password","Tim","Doe")['token']
    dm_id = dm_create_v1(token1, [u_id2])['dm_id']
    dm_msg_id = message_senddm_v1(token1, dm_id, "Hey")['message_id']
    with pytest.raises(AccessError):
        message_share_v1(token3, dm_msg_id, "heyo", -1, dm_id)
        
def test_message_share_dm_valid():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    u_id2 = auth_register_v1("james.smith@aunsw.edu.au","password","James","Smith")['auth_user_id']
    dm_id = dm_create_v1(token1, [u_id2])['dm_id']
    dm_msg_id = message_senddm_v1(token1, dm_id, "Hey")['message_id']
    message_share_v1(token1, dm_msg_id, "heyo", -1, dm_id)

def test_message_share_valid_channel():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan_id = channels_create_v1(token1, "Channel 1", True)['channel_id']
    msg_id = message_send_v1(token1, chan_id, "Hi there!")['message_id']
    message_share_v1(token1, msg_id, "heyo", chan_id, -1)

# The following tests are for message_react_v1
def test_message_react_invalid_token():
    clear_v1()
    token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan_id = channels_create_v1(token, "Channel 1", True)['channel_id']
    msg_id = message_send_v1(token, chan_id, "Hi there!")['message_id']
    with pytest.raises(AccessError):
        message_react_v1(7854, msg_id, 1)

def test_message_react_invalid_msg_id():
    clear_v1()
    token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan_id = channels_create_v1(token, "Channel 1", True)['channel_id']
    message_send_v1(token, chan_id, "Hi there!")['message_id']
    with pytest.raises(InputError):
        message_react_v1(token, 77, 1)

def test_message_react_user_not_part_of_channel():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    token2 = auth_register_v1("ann.yay@aunsw.edu.au","password","Ann","Yay")['token']
    chan_id = channels_create_v1(token1, "Channel 1", True)['channel_id']
    msg_id = message_send_v1(token1, chan_id, "Hi there!")['message_id']
    with pytest.raises(InputError):
        message_react_v1(token2, msg_id, 1)

def test_message_react_user_not_part_of_dm():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    u_id2 = auth_register_v1("ann.yay@aunsw.edu.au","password","Ann","Yay")['auth_user_id']
    token3 = auth_register_v1("will.ham@aunsw.edu.au","password","Will","Ham")['token']
    dm_id = dm_create_v1(token1, [u_id2])['dm_id']
    dm_msg_id = message_senddm_v1(token1, dm_id, "Hey")['message_id']
    with pytest.raises(InputError):
        message_react_v1(token3, dm_msg_id, 1)

def test_message_react_invalid_react_id():
    clear_v1()
    token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan_id = channels_create_v1(token, "Channel 1", True)['channel_id']
    msg_id = message_send_v1(token, chan_id, "Hi there!")['message_id']
    with pytest.raises(InputError):
        message_react_v1(token, msg_id, -1)

def test_message_react_already_reacted():
    clear_v1()
    token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan_id = channels_create_v1(token, "Channel 1", True)['channel_id']
    msg_id = message_send_v1(token, chan_id, "Hi there!")['message_id']
    message_react_v1(token, msg_id, 1)
    with pytest.raises(InputError):
        message_react_v1(token, msg_id, 1)

def test_message_react_user_in_wrong_channel():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan_id1 = channels_create_v1(token1, "Channel 1", True)['channel_id']
    msg_id1 = message_send_v1(token1, chan_id1, "Hi there!")['message_id']
    token2 = auth_register_v1("jane.doe@aunsw.edu.au","password","Jane","Doe")['token']
    chan_id2 = channels_create_v1(token2, "Channel 1", True)['channel_id']
    message_send_v1(token2, chan_id2, "Hi there!")['message_id']
    with pytest.raises(InputError):
        message_react_v1(token2, msg_id1, 1)

def test_message_react_user_in_wrong_dm():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    u_id2 = auth_register_v1("ann.yay@aunsw.edu.au","password","Ann","Yay")['auth_user_id']
    user3 = auth_register_v1("john.wow@aunsw.edu.au","password","Ann","Wow")
    dm_id1 = dm_create_v1(token1, [u_id2])['dm_id']
    dm_msg_id1 = message_senddm_v1(token1, dm_id1, "Hey")['message_id']
    dm_id2 = dm_create_v1(token1, [user3['auth_user_id']])['dm_id']
    message_senddm_v1(token1, dm_id2, "Hey")['message_id']
    with pytest.raises(InputError):
        message_react_v1(user3['token'], dm_msg_id1, 1)

def test_message_react_valid_channel():
    clear_v1()
    token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan_id = channels_create_v1(token, "Channel 1", True)['channel_id']
    msg_id = message_send_v1(token, chan_id, "Hi there!")['message_id']
    message_react_v1(token, msg_id, 1)

def test_message_react_valid_dm():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    u_id2 = auth_register_v1("ann.yay@aunsw.edu.au","password","Ann","Yay")['auth_user_id']
    dm_id = dm_create_v1(token1, [u_id2])['dm_id']
    dm_msg_id = message_senddm_v1(token1, dm_id, "Hey")['message_id']
    message_react_v1(token1, dm_msg_id, 1)

# The following tests are for message_unreact_v1
def test_message_unreact_invalid_token():
    clear_v1()
    token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan_id = channels_create_v1(token, "Channel 1", True)['channel_id']
    msg_id = message_send_v1(token, chan_id, "Hi there!")['message_id']
    message_react_v1(token, msg_id, 1)
    with pytest.raises(AccessError):
        message_unreact_v1(634232476, msg_id, 1)

def test_message_unreact_invalid_msg_id():
    clear_v1()
    token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan_id = channels_create_v1(token, "Channel 1", True)['channel_id']
    msg_id = message_send_v1(token, chan_id, "Hi there!")['message_id']
    message_react_v1(token, msg_id, 1)
    with pytest.raises(InputError):
        message_unreact_v1(token, 435, 1)

def test_message_unreact_user_not_in_chan():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    token2 = auth_register_v1("Bob.John@aunsw.edu.au","password","Bob","John")['token']
    chan_id = channels_create_v1(token1, "Channel 1", True)['channel_id']
    msg_id = message_send_v1(token1, chan_id, "Hi there!")['message_id']
    message_react_v1(token1, msg_id, 1)
    with pytest.raises(InputError):
        message_unreact_v1(token2, msg_id, 1)

def test_message_unreact_user_not_in_dm():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    u_id2 = auth_register_v1("james.smith@aunsw.edu.au","password","James","Smith")['auth_user_id']
    token3 = auth_register_v1("Tim.doe@aunsw.edu.au","password","Tim","Doe")['token']
    dm_id = dm_create_v1(token1, [u_id2])['dm_id']
    dm_msg_id = message_senddm_v1(token1, dm_id, "Hey")['message_id']
    message_react_v1(token1, dm_msg_id, 1)
    with pytest.raises(InputError):
        message_unreact_v1(token3, dm_msg_id, 1)

def test_message_unreact_invalid_react_id():
    clear_v1()
    token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan_id = channels_create_v1(token, "Channel 1", True)['channel_id']
    msg_id = message_send_v1(token, chan_id, "Hi there!")['message_id']
    message_react_v1(token, msg_id, 1)
    with pytest.raises(InputError):
        message_unreact_v1(token, msg_id, -1)

def test_message_unreact_user_in_wrong_channel():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan_id1 = channels_create_v1(token1, "Channel 1", True)['channel_id']
    msg_id1 = message_send_v1(token1, chan_id1, "Hi there!")['message_id']
    message_react_v1(token1, msg_id1, 1)
    token2 = auth_register_v1("jane.doe@aunsw.edu.au","password","Jane","Doe")['token']
    chan_id2 = channels_create_v1(token2, "Channel 1", True)['channel_id']
    msg_id2 = message_send_v1(token2, chan_id2, "Hi there!")['message_id']
    message_react_v1(token2, msg_id2, 1)
    with pytest.raises(InputError):
        message_unreact_v1(token2, msg_id1, 1)

def test_message_unreact_msg_not_reacted_to():
    clear_v1()
    token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan_id = channels_create_v1(token, "Channel 1", True)['channel_id']
    msg_id = message_send_v1(token, chan_id, "Hi there!")['message_id']
    with pytest.raises(InputError):
        message_unreact_v1(token, msg_id, 1)

def test_message_unreact_valid_chan():
    clear_v1()
    token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan_id = channels_create_v1(token, "Channel 1", True)['channel_id']
    msg_id = message_send_v1(token, chan_id, "Hi there!")['message_id']
    message_react_v1(token, msg_id, 1)
    message_unreact_v1(token, msg_id, 1)

def test_message_unreact_valid_dm():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    u_id2 = auth_register_v1("james.smith@aunsw.edu.au","password","James","Smith")['auth_user_id']
    dm_id = dm_create_v1(token1, [u_id2])['dm_id']
    dm_msg_id = message_senddm_v1(token1, dm_id, "Hey")['message_id']
    message_react_v1(token1, dm_msg_id, 1)
    message_unreact_v1(token1, dm_msg_id, 1)

# The following tests are for message_pin_v1

def test_message_pin_invalid_token():
    clear_v1()
    token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan_id = channels_create_v1(token, "Channel 1", True)['channel_id']
    msg_id = message_send_v1(token, chan_id, "Hi there!")['message_id']
    with pytest.raises(AccessError):
        message_pin_v1(5342, msg_id)

def test_message_pin_user_in_wrong_dm():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    u_id2 = auth_register_v1("james.smith@aunsw.edu.au","password","James","Smith")['auth_user_id']
    user3 = auth_register_v1("Tim.doe@aunsw.edu.au","password","Tim","Doe")
    dm_id1 = dm_create_v1(token1, [u_id2])['dm_id']
    dm_msg_id1 = message_senddm_v1(token1, dm_id1, "Hey")['message_id']
    dm_id2 = dm_create_v1(token1, [user3['auth_user_id']])['dm_id']
    message_senddm_v1(token1, dm_id2, "Hey")['message_id']
    with pytest.raises(InputError):
        message_pin_v1(user3['token'], dm_msg_id1)

def test_message_pin_user_in_wrong_channel():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan_id1 = channels_create_v1(token1, "Channel 1", True)['channel_id']
    msg_id1 = message_send_v1(token1, chan_id1, "Hi there!")['message_id']
    token2 = auth_register_v1("jane.doe@aunsw.edu.au","password","Jane","Doe")['token']
    chan_id2 = channels_create_v1(token2, "Channel 1", True)['channel_id']
    message_send_v1(token2, chan_id2, "Hi there!")['message_id']
    with pytest.raises(InputError):
        message_pin_v1(token2, msg_id1)

def test_message_pin_invalid():
    clear_v1()
    token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan_id = channels_create_v1(token, "Channel 1", True)['channel_id']
    message_send_v1(token, chan_id, "Hi there!")['message_id']
    with pytest.raises(InputError):
        message_pin_v1(token, -1)

def test_message_pin_msg_already_pinned():
    clear_v1()
    token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan_id = channels_create_v1(token, "Channel 1", True)['channel_id']
    msg_id = message_send_v1(token, chan_id, "Hi there!")['message_id']
    message_pin_v1(token, msg_id)
    with pytest.raises(InputError):
        message_pin_v1(token, msg_id)

def test_message_pin_user_not_owner_channel():
    clear_v1()
    auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    token2 = auth_register_v1("jane.doe@aunsw.edu.au","password","Jane","Doe")['token']
    token3 = auth_register_v1("jack.doe@aunsw.edu.au","password","Jack","Doe")['token']
    chan_id = channels_create_v1(token2, "Channel 1", True)['channel_id']
    channel_join_v1(token3, chan_id)
    msg_id = message_send_v1(token2, chan_id, "Hi there!")['message_id']
    with pytest.raises(AccessError):
        message_pin_v1(token3, msg_id)

def test_message_pin_global_user_not_owner_channel():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    token2 = auth_register_v1("jane.doe@aunsw.edu.au","password","Jane","Doe")['token']
    chan_id = channels_create_v1(token2, "Channel 1", True)['channel_id']
    channel_join_v1(token1, chan_id)
    msg_id = message_send_v1(token2, chan_id, "Hi there!")['message_id']
    message_pin_v1(token1, msg_id)

def test_message_pin_user_not_owner_dm():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    user2 = auth_register_v1("james.smith@aunsw.edu.au","password","James","Smith")
    dm_id = dm_create_v1(token1, [user2['auth_user_id']])['dm_id']
    dm_msg_id = message_senddm_v1(token1, dm_id, "Hey")['message_id']
    with pytest.raises(AccessError):
        message_pin_v1(user2['token'], dm_msg_id)

def test_message_pin_global_user_not_owner_dm():
    clear_v1()
    user1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")
    token2 = auth_register_v1("james.smith@aunsw.edu.au","password","James","Smith")['token']
    dm_id = dm_create_v1(token2, [user1['auth_user_id']])['dm_id']
    dm_msg_id = message_senddm_v1(token2, dm_id, "Hey")['message_id']
    with pytest.raises(AccessError):
        message_pin_v1(user1['token'], dm_msg_id)

def test_message_pin_valid_chan():
    clear_v1()
    token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan_id = channels_create_v1(token, "Channel 1", True)['channel_id']
    msg_id = message_send_v1(token, chan_id, "Hi there!")['message_id']
    message_pin_v1(token, msg_id)

def test_message_pin_valid_dm():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    u_id2 = auth_register_v1("james.smith@aunsw.edu.au","password","James","Smith")['auth_user_id']
    dm_id = dm_create_v1(token1, [u_id2])['dm_id']
    dm_msg_id = message_senddm_v1(token1, dm_id, "Hey")['message_id']
    message_pin_v1(token1, dm_msg_id)

# The following tests are for message_unpin_v1
def test_message_unpin_invalid_token():
    clear_v1()
    token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan_id = channels_create_v1(token, "Channel 1", True)['channel_id']
    msg_id = message_send_v1(token, chan_id, "Hi there!")['message_id']
    message_pin_v1(token, msg_id)
    with pytest.raises(AccessError):
        message_unpin_v1(5342, msg_id)

def test_message_unpin_user_in_wrong_dm():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    u_id2 = auth_register_v1("james.smith@aunsw.edu.au","password","James","Smith")['auth_user_id']
    user3 = auth_register_v1("Tim.doe@aunsw.edu.au","password","Tim","Doe")
    dm_id1 = dm_create_v1(token1, [u_id2])['dm_id']
    dm_msg_id1 = message_senddm_v1(token1, dm_id1, "Hey")['message_id']
    dm_id2 = dm_create_v1(token1, [user3['auth_user_id']])['dm_id']
    message_senddm_v1(token1, dm_id2, "Hey")['message_id']
    message_pin_v1(token1, dm_msg_id1)
    with pytest.raises(InputError):
        message_unpin_v1(user3['token'], dm_msg_id1)

def test_message_unpin_user_in_wrong_channel():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan_id1 = channels_create_v1(token1, "Channel 1", True)['channel_id']
    msg_id1 = message_send_v1(token1, chan_id1, "Hi there!")['message_id']
    token2 = auth_register_v1("jane.doe@aunsw.edu.au","password","Jane","Doe")['token']
    chan_id2 = channels_create_v1(token2, "Channel 1", True)['channel_id']
    message_send_v1(token2, chan_id2, "Hi there!")['message_id']
    message_pin_v1(token1, msg_id1)
    with pytest.raises(InputError):
        message_unpin_v1(token2, msg_id1)

def test_message_unpin_invalid():
    clear_v1()
    token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan_id = channels_create_v1(token, "Channel 1", True)['channel_id']
    msg_id = message_send_v1(token, chan_id, "Hi there!")['message_id']
    message_pin_v1(token, msg_id)
    with pytest.raises(InputError):
        message_unpin_v1(token, -1)

def test_message_unpin_msg_not_pinned():
    clear_v1()
    token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan_id = channels_create_v1(token, "Channel 1", True)['channel_id']
    msg_id = message_send_v1(token, chan_id, "Hi there!")['message_id']
    message_pin_v1(token, msg_id)
    message_unpin_v1(token, msg_id)
    with pytest.raises(InputError):
        message_unpin_v1(token, msg_id)

def test_message_unpin_user_not_owner_channel():
    clear_v1()
    auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    token2 = auth_register_v1("jane.doe@aunsw.edu.au","password","Jane","Doe")['token']
    token3 = auth_register_v1("jack.doe@aunsw.edu.au","password","Jack","Doe")['token']
    chan_id = channels_create_v1(token2, "Channel 1", True)['channel_id']
    channel_join_v1(token3, chan_id)
    msg_id = message_send_v1(token2, chan_id, "Hi there!")['message_id']
    message_pin_v1(token2, msg_id)
    with pytest.raises(AccessError):
        message_unpin_v1(token3, msg_id)
        
def test_message_unpin_global_user_not_owner_channel():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    token2 = auth_register_v1("jane.doe@aunsw.edu.au","password","Jane","Doe")['token']
    chan_id = channels_create_v1(token2, "Channel 1", True)['channel_id']
    channel_join_v1(token1, chan_id)
    msg_id = message_send_v1(token2, chan_id, "Hi there!")['message_id']
    message_pin_v1(token1, msg_id)
    message_unpin_v1(token1, msg_id)

def test_message_unpin_user_not_owner_dm():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    user2 = auth_register_v1("james.smith@aunsw.edu.au","password","James","Smith")
    dm_id = dm_create_v1(token1, [user2['auth_user_id']])['dm_id']
    dm_msg_id = message_senddm_v1(token1, dm_id, "Hey")['message_id']
    message_pin_v1(token1, dm_msg_id)
    with pytest.raises(AccessError):
        message_unpin_v1(user2['token'], dm_msg_id)

def test_message_unpin_global_user_not_owner_dm():
    clear_v1()
    user1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")
    token2 = auth_register_v1("james.smith@aunsw.edu.au","password","James","Smith")['token']
    dm_id = dm_create_v1(token2, [user1['auth_user_id']])['dm_id']
    dm_msg_id = message_senddm_v1(token2, dm_id, "Hey")['message_id']
    message_pin_v1(token2, dm_msg_id)
    with pytest.raises(AccessError):
        message_unpin_v1(user1['token'], dm_msg_id)

def test_message_unpin_valid_chan():
    clear_v1()
    token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan_id = channels_create_v1(token, "Channel 1", True)['channel_id']
    msg_id = message_send_v1(token, chan_id, "Hi there!")['message_id']
    message_pin_v1(token, msg_id)
    message_unpin_v1(token, msg_id)

def test_message_unpin_valid_dm():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    u_id2 = auth_register_v1("james.smith@aunsw.edu.au","password","James","Smith")['auth_user_id']
    dm_id = dm_create_v1(token1, [u_id2])['dm_id']
    dm_msg_id = message_senddm_v1(token1, dm_id, "Hey")['message_id']
    message_pin_v1(token1, dm_msg_id)
    message_unpin_v1(token1, dm_msg_id)

# # The following test are for message_send_later_v1

def test_message_sendlater_channel_id_invalid():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    time_sent = dt.datetime.timestamp(dt.datetime.now() + dt.timedelta(seconds=5))
    with pytest.raises(InputError): 
        message_sendlater_v1(token1, -1, "Boss", time_sent)

def test_message_sendlater_multi_msgs():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    channel_id = channels_create_v1(token1, "Channel 1", True)['channel_id']
    time_sent1 = dt.datetime.timestamp(dt.datetime.now() + dt.timedelta(seconds=1))
    msg1_id = message_sendlater_v1(token1, channel_id, "Hi there!", time_sent1)['message_id']
    time_sent2 = dt.datetime.timestamp(dt.datetime.now() + dt.timedelta(seconds=1))
    msg2_id = message_sendlater_v1(token1, channel_id, "Hi there!", time_sent2)['message_id']
    assert msg1_id != msg2_id

def test_message_sendlater_msent_in_past():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    channel_id = channels_create_v1(token1, "Channel 1", True)['channel_id']
    time_sent = dt.datetime.timestamp(dt.datetime.now() - dt.timedelta(seconds=5))
    with pytest.raises(InputError):
        message_sendlater_v1(token1, channel_id, "Hi there!", time_sent)

def test_message_sendlater_msg_length_too_small():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    channel_id = channels_create_v1(token1, "Channel 1", True)['channel_id']
    time_sent = (dt.datetime.timestamp(dt.datetime.now() + dt.timedelta(seconds=5)))
    with pytest.raises(InputError): 
        message_sendlater_v1(token1, channel_id, "", time_sent)

def test_message_sendlater_msg_length_too_big():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    channel_id = channels_create_v1(token1, "Channel 1", True)['channel_id']
    time_sent = dt.datetime.timestamp(dt.datetime.now() + dt.timedelta(seconds=5))
    with pytest.raises(InputError): 
        message_sendlater_v1(token1, channel_id, """Altruism is the principle and moral practice of concern for 
            happiness of other human beings or other animals, resulting in a quality of life both material and spiritual. 
            It is a traditional virtue in many cultures and a core aspect of various religious traditions and secular worldviews, 
            though the concept of others toward whom concern should be directed can vary among cultures and religions. 
            In an extreme case, altruism may become a synonym of selflessness, which is the opposite of selfishness. 
            The word altrusim was popularized (and possibly coined) by the French philosopher Auguste Comte in French, 
            as altruisme, for an antonym of egoism.[1][2] He derived it from the Italian altrui, which in turn was derived from Latin 
            alteri, meaning other people or somebody else.[3] Altruism in biological observations in field populations of the day organisms 
            is an individual performing an action which is at a cost to themselves (e.g., pleasure and quality of life, time, probability of 
            survival or reproduction), but benefits, either directly or indirectly, another""", time_sent)
    
def test_message_send_token_invalid():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    channel_id = channels_create_v1(token1, "Channel 1", True)['channel_id']
    time_sent = dt.datetime.timestamp(dt.datetime.now() + dt.timedelta(seconds=5))
    with pytest.raises(AccessError): 
        message_sendlater_v1(78534290, channel_id, "Hi there!", time_sent)

def test_message_send_user_not_part_of_channel():  # NEED TO CHECK FOR GLOBAL USERS
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    token2 = auth_register_v1("jane.doe@unsw.edu.au", "password","Jane","Doe")['token']
    channel_id = channels_create_v1(token1, "Channel 1", True)['channel_id']
    time_sent = dt.datetime.timestamp(dt.datetime.now() + dt.timedelta(seconds=5))
    with pytest.raises(AccessError): 
        message_sendlater_v1(token2, channel_id, "Hi there!", time_sent)

# # The following test are for message_sendlaterdm_v1

def test_message_sendlaterdm_dm_id_invalid():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    time_sent = dt.datetime.timestamp(dt.datetime.now() + dt.timedelta(seconds=5))
    with pytest.raises(InputError): 
        message_sendlaterdm_v1(token1, -1, "Boss", time_sent)

def test_message_sendlaterdm_multi_msgs():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    u_id2 = auth_register_v1("james.smith@aunsw.edu.au","password","James","Smith")['auth_user_id']
    dm_id = dm_create_v1(token1, [u_id2])['dm_id']
    time_sent1 = dt.datetime.timestamp(dt.datetime.now() + dt.timedelta(seconds=1))
    msg1_id = message_sendlaterdm_v1(token1, dm_id, "Hi there!", time_sent1)['message_id']
    time_sent2 = dt.datetime.timestamp(dt.datetime.now() + dt.timedelta(seconds=1))
    msg2_id = message_sendlaterdm_v1(token1, dm_id, "Hi there!", time_sent2)['message_id']
    assert msg1_id != msg2_id

def test_message_sendlaterdm_sent_in_past():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    u_id2 = auth_register_v1("james.smith@aunsw.edu.au","password","James","Smith")['auth_user_id']
    dm_id = dm_create_v1(token1, [u_id2])['dm_id']
    time_sent = dt.datetime.timestamp(dt.datetime.now() - dt.timedelta(seconds=5))
    with pytest.raises(InputError):
        message_sendlaterdm_v1(token1, dm_id, "Hi there!", time_sent)

def test_message_sendlaterdm_msg_length_too_small():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    u_id2 = auth_register_v1("james.smith@aunsw.edu.au","password","James","Smith")['auth_user_id']
    dm_id = dm_create_v1(token1, [u_id2])['dm_id']
    time_sent = (dt.datetime.timestamp(dt.datetime.now() + dt.timedelta(seconds=5)))
    with pytest.raises(InputError): 
        message_sendlaterdm_v1(token1, dm_id, "", time_sent)

def test_message_sendlaterdm_msg_length_too_big():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    u_id2 = auth_register_v1("james.smith@aunsw.edu.au","password","James","Smith")['auth_user_id']
    dm_id = dm_create_v1(token1, [u_id2])['dm_id']
    time_sent = dt.datetime.timestamp(dt.datetime.now() + dt.timedelta(seconds=5))
    with pytest.raises(InputError): 
        message_sendlaterdm_v1(token1, dm_id, """Altruism is the principle and moral practice of concern for 
            happiness of other human beings or other animals, resulting in a quality of life both material and spiritual. 
            It is a traditional virtue in many cultures and a core aspect of various religious traditions and secular worldviews, 
            though the concept of others toward whom concern should be directed can vary among cultures and religions. 
            In an extreme case, altruism may become a synonym of selflessness, which is the opposite of selfishness. 
            The word altrusim was popularized (and possibly coined) by the French philosopher Auguste Comte in French, 
            as altruisme, for an antonym of egoism.[1][2] He derived it from the Italian altrui, which in turn was derived from Latin 
            alteri, meaning other people or somebody else.[3] Altruism in biological observations in field populations of the day organisms 
            is an individual performing an action which is at a cost to themselves (e.g., pleasure and quality of life, time, probability of 
            survival or reproduction), but benefits, either directly or indirectly, another""", time_sent)
    
def test_message_senddm_token_invalid():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    u_id2 = auth_register_v1("james.smith@aunsw.edu.au","password","James","Smith")['auth_user_id']
    dm_id = dm_create_v1(token1, [u_id2])['dm_id']
    time_sent = dt.datetime.timestamp(dt.datetime.now() + dt.timedelta(seconds=5))
    with pytest.raises(AccessError): 
        message_sendlaterdm_v1(78534290, dm_id, "Hi there!", time_sent)

def test_message_send_user_not_part_of_dm():  # NEED TO CHECK FOR GLOBAL USERS
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    u_id2 = auth_register_v1("james.smith@aunsw.edu.au","password","James","Smith")['auth_user_id']
    token3 = auth_register_v1("jane.doe@unsw.edu.au", "password","Jane","Doe")['token']
    dm_id = dm_create_v1(token1, [u_id2])['dm_id']
    time_sent = dt.datetime.timestamp(dt.datetime.now() + dt.timedelta(seconds=5))
    with pytest.raises(AccessError): 
        message_sendlaterdm_v1(token3, dm_id, "Hi there!", time_sent)
