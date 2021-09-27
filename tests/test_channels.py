import pytest

from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.channel import channel_join_v1
from src.error import InputError
from src.error import AccessError
from src.other import clear_v1
from src.channel import channel_details_v1

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


# The following tests are for channel_join
def test_join_public_channel():
    clear_v1()
    user_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")
    channel_id = channels_create_v1(1, "Channel 1", True)
    channel_join_v1(user_id, channel_id)
    
def test_join_channel_user_aready_in():
    clear_v1()
    #user_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")
    channel_id = channels_create_v1(1, "Channel 1", True)
    channel_join_v1(1, channel_id)
    with pytest.raises(InputError):
        channel_join_v1(1, channel_id)


def test_join_channel_private():
    clear_v1()
    user_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")
    channel_id = channels_create_v1(1, "Channel 1", False)
    with pytest.raises(AccessError):
        channel_join_v1(user_id, channel_id)


def test_join_channel_user_aready_in_private():
    channel_id = channels_create_v1(1, "Channel 1", False)
    with pytest.raises(InputError):
        channel_join_v1(1, channel_id)


def test_join_channel_user_does_not_exist():
    clear_v1()
    #user_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")
    channel_id = channels_create_v1(1, "Channel 1", True)
    with pytest.raises(InputError):
        channel_join_v1(4, channel_id)
    

def test_join_channel_channel_does_not_exist():
    clear_v1()
    #user_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")
    #channel_id = channels_create_v1(1, "Channel 1", True)
    with pytest.raises(InputError):
        channel_join_v1(1, 3)

# The following tests are for channel_details
    
def test_channel_details_valid_channel():
    clear_v1()
    #user_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")
    channel_id = channels_create_v1(1, "Channel 1", True)
    channel_details_v1(1, channel_id)
    
def test_channel_details_non_existant_channel():
    clear_v1()
    #user_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")
    #channel_id = channels_create_v1(1, "Channel 1", True)
    with pytest.raises(InputError):
        channel_details_v1(1, 33)
        
def test_channel_details_non_existant_channel():
    clear_v1()
    user_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")
    #channel_id = channels_create_v1(user_id, "Channel 1", True)
    with pytest.raises(AccessError):
        channel_details_v1(user_id, 1)
