import pytest

from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.error import InputError
from src.other import clear_v1

# The following tests channel_create_v1
def test_invalid_user_id():
    clear_v1()
    with pytest.raises(InputError):
        channels_create_v1(1, "First Channel", True)

def test_empty_channel_name():
    clear_v1()
    user_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")
    with pytest.raises(InputError):
        channels_create_v1(user_id, "", True)

def test_long_channel_name():
    clear_v1()
    user_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")
    with pytest.raises(InputError):
        channels_create_v1(user_id, "Lengthofchanneltoolarge!", True)

def test_channel_name_exists():
    clear_v1()
    user1_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")
    user2_id = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")
    channels_create_v1(user1_id, "Channel 1", True)
    with pytest.raises(InputError):
        channels_create_v1(user1_id, "Channel 1", True)
    with pytest.raises(InputError):
        channels_create_v1(user2_id, "Channel 1", True)

# TODO: Check how it is successfully created
def test_channel_create_success():
    pass


