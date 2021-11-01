'''Contains tests for channels.py'''
import pytest

from src.auth import auth_register_v1
from src.channels import channels_create_v1, channels_list_v1, channels_listall_v1
from src.channel import channel_join_v1, channel_invite_v1
from src.error import InputError
from src.error import AccessError
from src.other import clear_v1

# The following tests channels_create_v1
def test_channels_create_invalid_auth_user_id():
    clear_v1()
    with pytest.raises(AccessError):
        channels_create_v1(1, "First Channel", True)

def test_channels_create_empty_channel_name():
    clear_v1()
    token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    with pytest.raises(InputError):
        channels_create_v1(token, "", True)

def test_channels_create_long_channel_name():
    clear_v1()
    token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    with pytest.raises(InputError):
        channels_create_v1(token, "Lengthofchanneltoolarge!", True)

def test_channels_create_success_public():
    clear_v1()
    token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    channels_create_v1(token, "Channel 1", True)

def test_channels_create_name_white_space():
    clear_v1()
    token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    with pytest.raises(InputError):
        channels_create_v1(token, " ", True)

def test_channels_create_success_private():
    clear_v1()
    token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    channels_create_v1(token, "Channel 1", False)

# Call channels_list with no channels
def test_channels_list_no_channels():
    clear_v1()
    token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    assert channels_list_v1(token) == {
        'channels': []
    }

# Call channels_listall with no channels
def test_channels_listall_no_channels_all():
    clear_v1()
    token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    assert channels_listall_v1(token) == {
        'channels': []
    }

# Call channels_list with only private channels
def test_channels_list_all_private():
    clear_v1()
    user_data = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")
    chan1_id = channels_create_v1(user_data['token'], "Private Channel 1", False)['channel_id']
    token = auth_register_v1("jade.lee@aunsw.edu.au","password","Jade","Lee")['token']
    chan2_id = channels_create_v1(token, "Private Channel 2", False)['channel_id']
    channel_invite_v1(token, chan2_id, user_data['auth_user_id'])
    assert channels_list_v1(user_data['token']) == {
        'channels': [
            {
                'channel_id': chan1_id,
                'name': 'Private Channel 1',
            },
            {
                'channel_id': chan2_id,
                'name': 'Private Channel 2',
            }
        ]
    }

# Call channels_list with only public channels
def test_channels_list_all_public():
    clear_v1()
    user_data = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")
    chan1_id = channels_create_v1(user_data['token'], "Public Channel 1", True)['channel_id']
    token = auth_register_v1("jade.lee@aunsw.edu.au","password","Jade","Lee")['token']
    chan2_id = channels_create_v1(token, "Public Channel 2", True)['channel_id']
    channel_invite_v1(token, chan2_id, user_data['auth_user_id'])
    assert channels_list_v1(user_data['token']) == {
        'channels': [
            {
                'channel_id': chan1_id,
                'name': 'Public Channel 1',
            },
            {
                'channel_id': chan2_id,
                'name': 'Public Channel 2',
            }
        ]
    }

# Call channels_list with only joined channels
def test_channels_list_valid():
    clear_v1()
    user_data = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")
    chan1_id = channels_create_v1(user_data['token'], "Public Channel", True)['channel_id']
    token = auth_register_v1("jade.lee@aunsw.edu.au","password","Jade","Lee")['token']
    chan2_id = channels_create_v1(token, "Private Channel", False)['channel_id']
    channel_invite_v1(token, chan2_id, user_data['auth_user_id'])
    assert channels_list_v1(user_data['token']) == {
        'channels': [
            {
                'channel_id': chan1_id,
                'name': 'Public Channel',
            },
            {
                'channel_id': chan2_id,
                'name': 'Private Channel',
            }
        ]
    }

# Call channels_list with only created channels
def test_channels_list_created():
    clear_v1()
    token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan1_id = channels_create_v1(token, "Public Channel 1", True)['channel_id']
    chan2_id = channels_create_v1(token, "Public Channel 2", True)['channel_id']
    assert channels_list_v1(token) == {
        'channels': [
            {
                'channel_id': chan1_id,
                'name': 'Public Channel 1',
            },
            {
                'channel_id': chan2_id,
                'name': 'Public Channel 2',
            }
        ]
    }

# Call channels_list with both public and private channels
def test_channels_list_public_private():
    clear_v1()
    token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan1_id = channels_create_v1(token, "Public Channel 1", True)['channel_id']
    chan2_id = channels_create_v1(token, "Private Channel 1", False)['channel_id']
    assert channels_list_v1(token) == {
        'channels': [
            {
                'channel_id': chan1_id,
                'name': 'Public Channel 1',
            },
            {
                'channel_id': chan2_id,
                'name': 'Private Channel 1'
            }
        ]
    }

def test_channels_list_invalid_user():
    clear_v1()
    with pytest.raises(AccessError):
        channels_list_v1(0)

# Call channels_listall with only private channels
def test_channels_listall_list_all_all_private():
    clear_v1()
    user_data = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")
    chan1_id = channels_create_v1(user_data['token'], "Private Channel 1", False)['channel_id']
    token = auth_register_v1("jade.lee@aunsw.edu.au","password","Jade","Lee")['token']
    chan2_id = channels_create_v1(token, "Private Channel 2", False)['channel_id']
    channel_invite_v1(token, chan2_id, user_data['auth_user_id'])
    assert channels_listall_v1(user_data['token']) == {
        'channels': [
            {
                'channel_id': chan1_id,
                'name': 'Private Channel 1',
            },
            {
                'channel_id': chan2_id,
                'name': 'Private Channel 2',
            }
        ]
   }

# Call channels_listall with only public channels
def test_channels_listall_list_all_all_public():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan1_id = channels_create_v1(token1, "Public Channel 1", False)['channel_id']
    token2 = auth_register_v1("jade.lee@aunsw.edu.au","password","Jade","Lee")['token']
    chan2_id = channels_create_v1(token2, "Public Channel 2", False)['channel_id']
    channel_join_v1(token1, chan2_id)
    assert channels_listall_v1(token1) == {
        'channels': [
            {
                'channel_id': chan1_id,
                'name': 'Public Channel 1',
            },
            {
                'channel_id': chan2_id,
                'name': 'Public Channel 2',
            }
        ]
    }

# Call channels_listall with only joined channels
def test_channels_listall_list_all_joined():
    clear_v1()
    user_data = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")
    token = auth_register_v1("jade.lee@aunsw.edu.au","password","Jade","Lee")['token']
    chan1_id = channels_create_v1(token, "Public Channel 1", True)['channel_id']
    chan2_id = channels_create_v1(token, "Private Channel 1", False)['channel_id']
    channel_invite_v1(token, chan2_id, user_data['auth_user_id'])
    channel_join_v1(user_data['token'], chan1_id)
    assert channels_listall_v1(user_data['token']) == {
        'channels': [
            {
                'channel_id': chan1_id,
                'name': 'Public Channel 1',
            },
            {
                'channel_id': chan2_id,
                'name': 'Private Channel 1',
            }
        ]
    }

# Call channels_listall with only created channels
def test_channels_listall_created():
    clear_v1()
    token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan1_id = channels_create_v1(token, "Private Channel 1", False)['channel_id']
    chan2_id = channels_create_v1(token, "Public Channel 1", True)['channel_id']
    assert channels_listall_v1(token) == {
        'channels': [
            {
                'channel_id': chan1_id,
                'name': 'Private Channel 1',
            },
            {
                'channel_id': chan2_id,
                'name': 'Public Channel 1',
            }
        ]
    }

def test_channels_listall_invalid_user():
    clear_v1()
    with pytest.raises(AccessError):
        channels_listall_v1(0)

# Call channels_list with both private and public channels
def test_channels_list_channels_list_default():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan_priv = channels_create_v1(token1, "Private Channel", False)['channel_id']
    chan1_id = channels_create_v1(token1, "Public Channel 1", False)['channel_id']
    token2 = auth_register_v1("jade.lee@aunsw.edu.au","password","Jade","Lee")['token']
    chan2_id = channels_create_v1(token2, "Public Channel 2", False)['channel_id']
    channel_join_v1(token1, chan2_id)
    assert channels_list_v1(token1) == {
        'channels': [
            {
                'channel_id': chan_priv,
                'name': 'Private Channel',
            },
            {
                'channel_id': chan1_id,
                'name': 'Public Channel 1',
            },
            {
                'channel_id': chan2_id,
                'name': 'Public Channel 2',
            }
        ]
    }
    assert channels_listall_v1(token1) == {
        'channels': [
            {
                'channel_id': chan_priv,
                'name': 'Private Channel',
            },
            {
                'channel_id': chan1_id,
                'name': 'Public Channel 1',
            },
            {
                'channel_id': chan2_id,
                'name': 'Public Channel 2',
            }
        ]
    }

# Regular channels_listall
def test_channels_listall_default():
    clear_v1()
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan_priv = channels_create_v1(token1, "Private Channel", False)['channel_id']
    chan1_id = channels_create_v1(token1, "Public Channel 1", False)['channel_id']
    token2 = auth_register_v1("jade.lee@aunsw.edu.au","password","Jade","Lee")['token']
    chan2_id = channels_create_v1(token2, "Public Channel 2", False)['channel_id']
    channel_join_v1(token1, chan2_id)
    assert channels_listall_v1(token1) == {
        'channels': [
            {
                'channel_id': chan_priv,
                'name': 'Private Channel',
            },
            {
                'channel_id': chan1_id,
                'name': 'Public Channel 1',
            },
            {
                'channel_id': chan2_id,
                'name': 'Public Channel 2',
            }
        ]
    }

# Call channels_list and channels_listall when we have multiple users
def test_channels_list_and_listall_multiple_users():
    clear_v1()
    token = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    user_data = auth_register_v1("jade.lee@aunsw.edu.au","password","Jade","Lee")
    priv_user1_chan_id = channels_create_v1(token, "Private Channel 1", False)['channel_id']
    priv_user2_chan_id = channels_create_v1(user_data['token'], "Private Channel 2", False)['channel_id']
    pub_user1_chan_id = channels_create_v1(token, "Public Channel 1", True)['channel_id']
    pub_user2_chan_id = channels_create_v1(user_data['token'], "Public Channel 2", True)['channel_id']
    channel_join_v1(token, priv_user2_chan_id)
    channel_join_v1(token, pub_user2_chan_id)
    channel_invite_v1(token, priv_user1_chan_id, user_data['auth_user_id'])
    priv_user1_chan = {
        'channel_id': priv_user1_chan_id,
        'name': "Private Channel 1"
    }
    priv_user2_chan = {
        'channel_id': priv_user2_chan_id,
        'name': "Private Channel 2"
    }
    pub_user1_chan = {
        'channel_id': pub_user1_chan_id,
        'name': "Public Channel 1"
    }
    pub_user2_chan = {
        'channel_id': pub_user2_chan_id,
        'name': "Public Channel 2"
    }
    assert channels_list_v1(token) == {
        'channels': [priv_user1_chan, priv_user2_chan, pub_user1_chan, pub_user2_chan]
    }
    assert channels_list_v1(user_data['token']) == {
        'channels': [priv_user1_chan, priv_user2_chan, pub_user2_chan]
    }
    assert channels_listall_v1(token) == channels_list_v1(token)
    assert channels_listall_v1(user_data['token']) == channels_list_v1(token)
