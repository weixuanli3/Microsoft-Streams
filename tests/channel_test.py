'''Contains tests for channel.py'''
import pytest

from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.channel import channel_invite_v1, channel_messages_v1
from src.channel import channel_join_v1
from src.channel import channel_details_v1
from src.error import InputError
from src.error import AccessError
from src.other import clear_v1

# The following tests are for channel_invite_v1
def test_channel_invite_channel_invalid():
    clear_v1()
    user1_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['auth_user_id']
    user2_id = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['auth_user_id']
    # channel1_id = channels_create_v1(user1_id, "Channel 1", True)['channel_id']
    with pytest.raises(InputError):
        channel_invite_v1(user1_id, 2, user2_id)

def test_channel_invite_uid_invalid():
    clear_v1()
    user1_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['auth_user_id']
    channel1_id = channels_create_v1(user1_id, "Channel 1", True)['channel_id']
    with pytest.raises(InputError):
        channel_invite_v1(user1_id, channel1_id, 22)

def test_channel_invite_uid_in_channel():
    clear_v1()
    user1_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['auth_user_id']
    user2_id = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['auth_user_id']
    channel1_id = channels_create_v1(user1_id, "Channel 1", True)['channel_id']
    channel_join_v1(user2_id, channel1_id)
    with pytest.raises(InputError):
        channel_invite_v1(user1_id, channel1_id, user2_id)

def test_channel_invite_auth_not_in_channel():
    clear_v1()
    user1_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['auth_user_id']
    user2_id = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['auth_user_id']
    user3_id = auth_register_v1("john.green@aunsw.edu.au", "codeword", "John", "Green")['auth_user_id']
    channel1_id = channels_create_v1(user1_id, "Channel 1", True)['channel_id']
    with pytest.raises(AccessError):
        channel_invite_v1(user2_id, channel1_id, user3_id)

def test_channel_invite_valid():
    clear_v1()
    user1_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['auth_user_id']
    user2_id = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['auth_user_id']
    channel1_id = channels_create_v1(user1_id, "Channel 1", True)['channel_id']
    channel_invite_v1(user1_id, channel1_id, user2_id)

def test_channel_invite_channel_id_empty():
    clear_v1()
    user1_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['auth_user_id']
    user2_id = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['auth_user_id']
    # channel1_id = channels_create_v1(user1_id, "Channel 1", True)['channel_id']
    with pytest.raises(InputError):
        channel_invite_v1(user1_id, "", user2_id)

def test_channel_invite_user_id_empty():
    clear_v1()
    user1_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['auth_user_id']
    channel1_id = channels_create_v1(user1_id, "Channel 1", True)['channel_id']
    with pytest.raises(InputError):
        channel_invite_v1(user1_id, channel1_id, "")

def test_channel_invite_no_channels():
    clear_v1()
    user1_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['auth_user_id']
    user2_id = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['auth_user_id']
    with pytest.raises(InputError):
        channel_invite_v1(user1_id, 1, user2_id)

def test_channel_invite_auth_id_invalid():
    clear_v1()
    user1_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['auth_user_id']
    channel1_id = channels_create_v1(user1_id, "Channel 1", True)['channel_id']
    with pytest.raises(AccessError):
        channel_invite_v1("", channel1_id, user1_id)

def test_channel_invite_user_invites_self():
    clear_v1()
    user1_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['auth_user_id']
    channel1_id = channels_create_v1(user1_id, "Channel 1", True)['channel_id']
    with pytest.raises(InputError):
        channel_invite_v1(user1_id, channel1_id, user1_id)

def test_channel_invite_all_invalid():
    clear_v1()
    with pytest.raises(AccessError):
        channel_invite_v1("", "", "")

    # The following tests are for channel_join
def test_channel_join_public_channel():
    clear_v1()
    user1_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['auth_user_id']
    user2_id = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['auth_user_id']
    channel_id = channels_create_v1(user1_id, "Channel 1", True)['channel_id']
    assert channel_join_v1(user2_id, channel_id) == {}

def test_channel_join_channel_user_aready_in():
    clear_v1()
    user_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['auth_user_id']
    channel_id = channels_create_v1(user_id, "Channel 1", True)['channel_id']
    with pytest.raises(InputError):
        channel_join_v1(user_id, channel_id)


def test_channel_join_channel_private():
    clear_v1()
    user1_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['auth_user_id']
    user2_id = auth_register_v1("john.smith@aunsw.edu.au","password","John","Smith")['auth_user_id']
    channel_id = channels_create_v1(user1_id, "Channel 1", False)['channel_id']
    with pytest.raises(AccessError):
        channel_join_v1(user2_id, channel_id)


def test_channel_join_channel_user_aready_in_private():
    clear_v1()
    # user1_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['auth_user_id']
    user2_id = auth_register_v1("john.smith@aunsw.edu.au","password","John","Smith")['auth_user_id']
    channel_id = channels_create_v1(user2_id, "Channel 1", False)['channel_id']
    with pytest.raises(InputError):
        channel_join_v1(user2_id, channel_id)


def test_channel_join_channel_user_does_not_exist():
    clear_v1()
    user_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['auth_user_id']
    channel_id = channels_create_v1(user_id, "Channel 1", True)['channel_id']
    with pytest.raises(AccessError):
        channel_join_v1(4, channel_id)

def test_channel_join_channel_channel_does_not_exist():
    clear_v1()
    user_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['auth_user_id']
    with pytest.raises(InputError):
        channel_join_v1(user_id, 3333)

def test_channel_join_channel_user_id_empty():
    clear_v1()
    user_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['auth_user_id']
    channel_id = channels_create_v1(user_id, "Channel 1", True)['channel_id']
    with pytest.raises(AccessError):
        channel_join_v1("", channel_id)

def test_channel_join_channel_channel_id_empty():
    clear_v1()
    user_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['auth_user_id']
    # channel_id = channels_create_v1(user_id, "Channel 1", True)['channel_id']
    with pytest.raises(InputError):
        channel_join_v1(user_id, "")

def test_channel_join_global_user_joins_private():
    clear_v1()
    user1_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['auth_user_id']
    user2_id = auth_register_v1("john.smith@aunsw.edu.au","password","John","Smith")['auth_user_id']
    channel_id = channels_create_v1(user2_id, "Channel 1", False)['channel_id']
    channel_join_v1(user1_id, channel_id)

def test_channel_join_all_invalid():
    clear_v1()
    with pytest.raises(AccessError):
        channel_join_v1("", "")

# The following tests are for channel_details

def test_channel_details_valid_channel():
    clear_v1()
    user1_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['auth_user_id']
    user2_id = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['auth_user_id']
    channel_id = channels_create_v1(user1_id, "Channel 1", True)['channel_id']
    channel_join_v1(user2_id, channel_id)
    assert (channel_details_v1(user1_id, channel_id) == {
        'name' : 'Channel 1',
        'is_public' : True,
        'owner_members' : [{'email': 'john.doe@aunsw.edu.au', 'handle_str': 'johndoe', 'name_first': 'John', 'name_last': 'Doe', 'u_id': user1_id}],
        'all_members' : [{'email': 'john.doe@aunsw.edu.au', 'handle_str': 'johndoe', 'name_first': 'John', 'name_last': 'Doe', 'u_id': user1_id}, {'email': 'john.smith@aunsw.edu.au', 'handle_str': 'johnsmith', 'name_first': 'John', 'name_last': 'Smith', 'u_id': user2_id}],
    })

def test_channel_details_valid_private_channel():
    clear_v1()
    user1_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['auth_user_id']
    channel_id = channels_create_v1(user1_id, "Channel 1", False)['channel_id']
    assert (channel_details_v1(user1_id, channel_id) == {
        'name' : 'Channel 1',
        'is_public' : False,
        'owner_members' : [{'email': 'john.doe@aunsw.edu.au', 'handle_str': 'johndoe', 'name_first': 'John', 'name_last': 'Doe', 'u_id': user1_id}],
        'all_members' : [{'email': 'john.doe@aunsw.edu.au', 'handle_str': 'johndoe', 'name_first': 'John', 'name_last': 'Doe', 'u_id': user1_id}],
    })
    
def test_channel_details_non_existant_channel():
    clear_v1()
    user_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['auth_user_id']
    with pytest.raises(InputError):
        channel_details_v1(user_id, 33)

def test_channel_details_not_in_channel():
    clear_v1()
    user1_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['auth_user_id']
    user2_id = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['auth_user_id']
    channel_id = channels_create_v1(user1_id, "Channel 1", True)['channel_id']
    with pytest.raises(AccessError):
        channel_details_v1(user2_id, channel_id)

def test_channel_details_user_id_invalid():
    clear_v1()
    user1_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['auth_user_id']
    channel_id = channels_create_v1(user1_id, "Channel 1", True)['channel_id']
    with pytest.raises(AccessError):
        channel_details_v1("", channel_id)

def test_channel_details_channel_id_invalid():
    clear_v1()
    user1_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['auth_user_id']
    with pytest.raises(InputError):
        channel_details_v1(user1_id, "")

def test_channel_details_user_id_and_channel_id_invalid():
    clear_v1()
    # user1_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['auth_user_id']
    # channel_id = channels_create_v1(user1_id, "Channel 1", True)['channel_id']
    with pytest.raises(AccessError):
        channel_details_v1("", "")

def test_channel_details_all_invalid():
    clear_v1()
    with pytest.raises(AccessError):
        channel_details_v1("", "")

# The following tests are for channel_messages
def test_channel_messages_invalid_channel():
    clear_v1()
    user_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['auth_user_id']
    with pytest.raises(InputError):
        channel_messages_v1(user_id, 33, 0)

def test_channel_messages_start_too_large():
    clear_v1()
    user_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['auth_user_id']
    channel_id = channels_create_v1(user_id, "Channel 1", True)['channel_id']
    with pytest.raises(InputError):
        channel_messages_v1(user_id, channel_id, 33)

def test_channel_messages_user_not_member():
    clear_v1()
    user1_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['auth_user_id']
    user2_id = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['auth_user_id']
    channel_id = channels_create_v1(user1_id, "Channel 1", True)['channel_id']
    with pytest.raises(AccessError):
        channel_messages_v1(user2_id, channel_id, 0)

def test_channel_messages_no_channel_id():
    clear_v1()
    # user1_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['auth_user_id']
    user2_id = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['auth_user_id']
    # channel_id = channels_create_v1(user1_id, "Channel 1", True)['channel_id']
    with pytest.raises(InputError):
        channel_messages_v1(user2_id, "", 0)

def test_channel_messages_start_empty():
    clear_v1()
    user1_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['auth_user_id']
    user2_id = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['auth_user_id']
    channel_id = channels_create_v1(user1_id, "Channel 1", True)['channel_id']
    with pytest.raises(AccessError):
        channel_messages_v1(user2_id, channel_id, "")

def test_channel_messages_invalid_user():
    clear_v1()
    user1_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['auth_user_id']
    channel_id = channels_create_v1(user1_id, "Channel 1", True)['channel_id']
    with pytest.raises(AccessError):
        channel_messages_v1(2, channel_id, 0)

def test_channel_messages_all_invalid():
    clear_v1()
    with pytest.raises(AccessError):
        channel_messages_v1("", "", 0)

# the following tests are for channel_addowner
# def test_channel_addowner_channel_invalid():
#     clear_v1()
#     token = auth_register_v2("john.doe@aunsw.edu.au","password","John","Doe")['token']
#     user_id = auth_register_v2("jade.lee@aunsw.edu.au","password","Jade","Lee")['user_id']
#     with pytest.raises(InputError):
#         channel_addowner_v1(token, 1, user_id)

# def test_channel_addowner_user_invalid():
#     clear_v1()
#     token = auth_register_v2("john.doe@aunsw.edu.au","password","John","Doe")['token']
#     chan_id = channels_create_v2(token, "Channel", True)['channel_id']
#     with pytest.raises(InputError):
#         channel_addowner_v1(token, chan_id, 1)

# def test_channel_addowner_user_not_member():
#     clear_v1()
#     token = auth_register_v2("john.doe@aunsw.edu.au","password","John","Doe")['token']
#     user_id = auth_register_v2("jade.lee@aunsw.edu.au","password","Jade","Lee")['user_id']
#     chan_id = channels_create_v2(token, "Channel", True)['channel_id']
#     with pytest.raises(InputError):
#         channel_addowner_v1(token, chan_id, user_id)

# def test_channel_addowner_user_valid_then_user_already_owner():
#     clear_v1()
#     token = auth_register_v2("john.doe@aunsw.edu.au","password","John","Doe")['token']
#     user_data = auth_register_v2("jade.lee@aunsw.edu.au","password","Jade","Lee")
#     chan_id = channels_create_v2(token, "Channel", True)['channel_id']
#     channel_join_v2(user_data['token'], chan_id)
#     assert channel_addowner_v1(token, chan_id, user_data[user_id]) == {}
#     with pytest.raises(InputError):
#         channel_addowner_v1(token, chan_id, user_data['user_id'])

# def test_channel_addowner_token_not_member():
#     clear_v1()
#     token = auth_register_v2("john.doe@aunsw.edu.au","password","John","Doe")['token']
#     user_id = auth_register_v2("jade.lee@aunsw.edu.au","password","Jade","Lee")['user_id']
#     chan_id = channels_create_v2(token, "Channel", True)['channel_id']
#     channel_join_v2(user_data['token'], chan_id)
#     with pytest.raises(AccessError):
#         channel_addowner_v1(1, chan_id, user_id)

# def test_channel_addowner_token_not_owner():
#     clear_v1()
#     token1 = auth_register_v2("john.doe@aunsw.edu.au","password","John","Doe")['token']
#     token2 = auth_register_v2("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['token']
#     user_id = auth_register_v2("jade.lee@aunsw.edu.au","password","Jade","Lee")['user_id']
#     chan_id = channels_create_v2(token1, "Channel", True)['channel_id']
#     channel_join_v2(user_data['token'], chan_id)
#     with pytest.raises(AccessError):
#         channel_addowner_v1(token2, chan_id, user_id)

 the following tests are for channel_removeowner
# def test_channel_removeowner_channel_invalid():
#     clear_v1()
#     token = auth_register_v2("john.doe@aunsw.edu.au","password","John","Doe")['token']
#     user_id = auth_register_v2("jade.lee@aunsw.edu.au","password","Jade","Lee")['user_id']
#     with pytest.raises(InputError):
#         channel_addowner_v1(token, 1, user_id)

# def test_channel_removeowner_user_invalid():
#     clear_v1()
#     token = auth_register_v2("john.doe@aunsw.edu.au","password","John","Doe")['token']
#     chan_id = channels_create_v2(token, "Channel", True)['channel_id']
#     with pytest.raises(InputError):
#         channel_removeowner_v1(token, chan_id, 1)

# def test_channel_removeowner_user_not_member():
#     clear_v1()
#     token = auth_register_v2("john.doe@aunsw.edu.au","password","John","Doe")['token']
#     user_id = auth_register_v2("jade.lee@aunsw.edu.au","password","Jade","Lee")['user_id']
#     chan_id = channels_create_v2(token, "Channel", True)['channel_id']
#     with pytest.raises(InputError):
#         channel_removeowner_v1(token, chan_id, user_id)

# def test_channel_removeowner_user_valid_then_user_not_owner():
#     clear_v1()
#     token = auth_register_v2("john.doe@aunsw.edu.au","password","John","Doe")['token']
#     user_data = auth_register_v2("jade.lee@aunsw.edu.au","password","Jade","Lee")
#     chan_id = channels_create_v2(token, "Channel", True)['channel_id']
#     channel_join_v2(user_data['token'], chan_id)
#     channel_addowner_v1(token, chan_id, user_data[user_id])
#     assert channel_removeowner_v1(token, chan_id, user_data[user_id]) == {}
#     with pytest.raises(InputError):
#         channel_removeowner_v1(token, chan_id, user_data['user_id'])

# def test_channel_removeowner_token_not_member():
#     clear_v1()
#     token = auth_register_v2("john.doe@aunsw.edu.au","password","John","Doe")['token']
#     user_data = auth_register_v2("jade.lee@aunsw.edu.au","password","Jade","Lee")
#     chan_id = channels_create_v2(token, "Channel", True)['channel_id']
#     channel_join_v2(user_data['token'], chan_id)
#     with pytest.raises(AccessError):
#         channel_removeowner_v1(1, chan_id, user_data['user_id'])

# def test_channel_removeowner_token_not_owner():
#     clear_v1()
#     token1 = auth_register_v2("john.doe@aunsw.edu.au","password","John","Doe")['token']
#     token2 = auth_register_v2("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['token']
#     user_data = auth_register_v2("jade.lee@aunsw.edu.au","password","Jade","Lee")
#     chan_id = channels_create_v2(token1, "Channel", True)['channel_id']
#     channel_join_v2(user_data['token'], chan_id)
#     channel_addowner_v1(token, chan_id, user_data['user_id'])
#     with pytest.raises(AccessError):
#         channel_removeowner_v1(token2, chan_id, user_data['user_id'])

# def test_channel_removeowner_user_only_owner():
#     clear_v1()
#     user_data = auth_register_v2("john.doe@aunsw.edu.au","password","John","Doe")
#     chan_id = channels_create_v2(user_data['user_id'], "Channel", True)['channel_id']
#     with pytest.raises(InputError):
#         channel_removeowner_v1(user_data['token'], chan_id, user_data['user_id'])

# def test_channel_removeowner_token_not_member():
#     clear_v1()
#     user1_data = auth_register_v2("john.doe@aunsw.edu.au","password","John","Doe")
#     user2_data = auth_register_v2("jade.lee@aunsw.edu.au","password","Jade","Lee")
#     chan_id = channels_create_v2(user1_data['token'], "Channel", True)['channel_id']
#     channel_join_v2(user2_data['token'], chan_id)
#     channel_addowner_v1(user1_data['token'], chan_id, user2_data['user_id'])
#     assert channel_removeowner_v1(user1_data['token'], chan_id, user1_data['user_id']) == {}
