import pytest

from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.channel import channel_invite_v1
from src.channel import channel_join_v1
from src.error import InputError
from src.error import AccessError
from src.other import clear_v1

# The following tests are for channel_invite_v1
def test_channel_invite_channel_invalid():
    clear_v1()
    user1_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['auth_user_id']
    user2_id = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['auth_user_id']
    channels_create_v1(user1_id, "Channel 1", True)
    with pytest.raises(InputError):
        channel_invite_v1(user1_id, "Channel 2", user2_id)

def test_channel_invite_uid_invalid():
    clear_v1()
    user1_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['auth_user_id']
    channels_create_v1(user1_id, "Channel 1", True)
    with pytest.raises(InputError):
        channel_invite_v1(user1_id, "Channel 1", user2_id)

def test_channel_invite_uid_in_channel():
    clear_v1()
    user1_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['auth_user_id']
    user2_id = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['auth_user_id']
    channels_create_v1(user1_id, "Channel 1", True)
    channel_join_v1(user2_id, "channel 1")
    with pytest.raises(InputError):
        channel_invite_v1(user1_id, "Channel 1", user2_id)

def test_channel_invite_auth_not_in_channel():
    clear_v1()
    user1_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['auth_user_id']
    user2_id = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['auth_user_id']
    user3_id = auth_register_v1("john.green@aunsw.edu.au", "codeword", "John", "Green")['auth_user_id']
    channels_create_v1(user1_id, "Channel 1", True)
    with pytest.raises(AccessError):
        channel_invite_v1(user2_id, "Channel 2", user3_id)

def test_channel_invite_valid():
    clear_v1()
    user1_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['auth_user_id']
    user2_id = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['auth_user_id']
    channels_create_v1(user1_id, "Channel 1", True)
    channel_invite_v1(user1_id, "Channel 1", user2_id) == {}

