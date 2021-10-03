'''Contains tests for channels.py'''
import pytest

from src.auth import auth_register_v1
from src.channels import channels_create_v1, channels_list_v1, channels_listall_v1
from src.channel import channel_join_v1, channel_invite_v1
from src.error import InputError
from src.error import AccessError
from src.other import clear_v1

# The following tests channels_create_v1
def test_channels_create_invalid_user_id():
    clear_v1()
    with pytest.raises(AccessError):
        channels_create_v1(1, "First Channel", True)

def test_channels_create_empty_channel_name():
    clear_v1()
    user_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['auth_user_id']
    with pytest.raises(InputError):
        channels_create_v1(user_id, "", True)

def test_channels_create_long_channel_name():
    clear_v1()
    user_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['auth_user_id']
    with pytest.raises(InputError):
        channels_create_v1(user_id, "Lengthofchanneltoolarge!", True)

# def test_is_public_not_true_false():
#     clear_v1()
#     user_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['auth_user_id']
#     with pytest.raises(InputError):
#         channels_create_v1(user_id, "Lengthofchanneltoolarge!", "")

def test_channels_create_success_public():
    clear_v1()
    user_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['auth_user_id']
    # assert channels_create_v1(user_id, "Channel 1", True) == {'channel_id': 1}
    channels_create_v1(user_id, "Channel 1", True)

def test_channels_create_success_private():
    clear_v1()
    user_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['auth_user_id']
    # assert channels_create_v1(user_id, "Channel 1", False) == {'channel_id': 1}
    channels_create_v1(user_id, "Channel 1", False)


#Call channels_list with no channels
def test_channels_list_no_channels():
    clear_v1()
    user1_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['auth_user_id']
    assert channels_list_v1(user1_id) == {
        'channels': []
    }

#Call channels_listall with no channels
def test_channels_listall_no_channels_all():
    clear_v1()
    user1_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['auth_user_id']
    assert channels_listall_v1(user1_id) == {
        'channels': []
    }

#Call channels_list with only private channels
def test_channels_list_all_private():
    clear_v1()
    user1_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['auth_user_id']
    chan1_id = channels_create_v1(user1_id, "Private Channel", False)['channel_id']
    user2_id = auth_register_v1("jade.lee@aunsw.edu.au","password","Jade","Lee")['auth_user_id']
    chan2_id = channels_create_v1(user2_id, "Private Channel 2", False)['channel_id']
    channel_invite_v1(user2_id, chan2_id, user1_id)
    assert channels_list_v1(user1_id) == {
        'channels': [
            {
                'channel_id': chan1_id,
                'name': 'Private Channel',
            },
            {
                'channel_id': chan2_id,
                'name': 'Private Channel 2',
            }
        ]
    }

#Call channels_list with only public channels
def test_channels_list_all_public():
    clear_v1()
    user1_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['auth_user_id']
    chan1_id = channels_create_v1(user1_id, "Public Channel 1", True)['channel_id']
    user2_id = auth_register_v1("jade.lee@aunsw.edu.au","password","Jade","Lee")['auth_user_id']
    chan2_id = channels_create_v1(user2_id, "Public Channel 2", True)['channel_id']
    channel_join_v1(user1_id, chan2_id)
    assert channels_list_v1(user1_id) == {
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

#Call channels_list with only joined channels
def test_channels_list_joined():
    clear_v1()
    user1_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['auth_user_id']
    user2_id = auth_register_v1("jade.lee@aunsw.edu.au","password","Jade","Lee")['auth_user_id']
    chan1_id = channels_create_v1(user2_id, "Public Channel 1", True)['channel_id']
    chan2_id = channels_create_v1(user2_id, "Private Channel 1", False)['channel_id']
    channel_invite_v1(user2_id, chan2_id, user1_id)
    channel_join_v1(user1_id, chan1_id)
    assert channels_list_v1(user1_id) == {
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

#Call channels_list with only created channels
def test_channels_list_created():
    clear_v1()
    user1_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['auth_user_id']
    chan1_id = channels_create_v1(user1_id, "Public Channel 1", True)['channel_id']
    chan2_id = channels_create_v1(user1_id, "Public Channel 2", True)['channel_id']
    assert channels_list_v1(user1_id) == {
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

#Call channels_list with both public and private channels
def test_channels_list_public_private():
    clear_v1()
    user1_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['auth_user_id']
    chan1_id = channels_create_v1(user1_id, "Public Channel 1", True)['channel_id']
    chan2_id = channels_create_v1(user1_id, "Private Channel 1", False)['channel_id']
    assert channels_list_v1(user1_id) == {
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

#Call channels_listall with only private channels
def test_channels_listall_list_all_all_private():
    clear_v1()
    user1_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['auth_user_id']
    chan1_id = channels_create_v1(user1_id, "Private Channel 1", False)['channel_id']
    user2_id = auth_register_v1("jade.lee@aunsw.edu.au","password","Jade","Lee")['auth_user_id']
    chan2_id = channels_create_v1(user2_id, "Private Channel 2", False)['channel_id']
    channel_invite_v1(user2_id, chan2_id, user1_id)
    assert channels_listall_v1(user1_id) == {
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

#Call channels_listall with only public channels
def test_channels_listall_list_all_all_public():
    clear_v1()
    user1_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['auth_user_id']
    chan1_id = channels_create_v1(user1_id, "Public Channel 1", True)['channel_id']
    user2_id = auth_register_v1("jade.lee@aunsw.edu.au","password","Jade","Lee")['auth_user_id']
    chan2_id = channels_create_v1(user2_id, "Public Channel 2", True)['channel_id']
    channel_join_v1(user1_id, chan2_id)
    assert channels_listall_v1(user1_id) == {
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

#Call channels_listall with only joined channels
def test_channels_listall_list_all_joined():
    clear_v1()
    user1_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['auth_user_id']
    user2_id = auth_register_v1("jade.lee@aunsw.edu.au","password","Jade","Lee")['auth_user_id']
    chan1_id = channels_create_v1(user2_id, "Public Channel 1", True)['channel_id']
    chan2_id = channels_create_v1(user2_id, "Private Channel 1", False)['channel_id']
    channel_invite_v1(user2_id, chan2_id, user1_id)
    channel_join_v1(user1_id, chan1_id)
    assert channels_listall_v1(user1_id) == {
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

#Call channels_listall with only created channels
def test_channels_listall_created():
    clear_v1()
    user1_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['auth_user_id']
    chan1_id = channels_create_v1(user1_id, "Private Channel 1", False)['channel_id']
    chan2_id = channels_create_v1(user1_id, "Public Channel 1", True)['channel_id']
    assert channels_listall_v1(user1_id) == {
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

#Call channels_list with both private and public channels
def test_channels_list_channels_list_default():
    clear_v1()
    user1_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['auth_user_id']
    user2_id = auth_register_v1("jade.lee@aunsw.edu.au","password","Jade","Lee")['auth_user_id']
    chan_priv = channels_create_v1(user1_id, "Private Channel", False)['channel_id']
    chan1_id = channels_create_v1(user1_id, "Public Channel 1", True)['channel_id']
    chan2_id = channels_create_v1(user2_id, "Public Channel 2", True)['channel_id']
    channel_join_v1(user1_id, chan2_id)
    assert channels_list_v1(user1_id) == {
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
    assert channels_listall_v1(user1_id) == {
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

#Regular channels_listall
def test_channels_listall_default():
    clear_v1()
    user1_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['auth_user_id']
    user2_id = auth_register_v1("jade.lee@aunsw.edu.au","password","Jade","Lee")['auth_user_id']
    chan_priv_id = channels_create_v1(user1_id, "Private Channel", False)['channel_id']
    chan1_id = channels_create_v1(user1_id, "Public Channel 1", True)['channel_id']
    chan2_id = channels_create_v1(user2_id, "Public Channel 2", True)['channel_id']
    channel_join_v1(user1_id, chan2_id)
    assert channels_listall_v1(user1_id) == {
        'channels': [
            {
                'channel_id': chan_priv_id,
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
    user1_id = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['auth_user_id']
    user2_id = auth_register_v1("jade.lee@aunsw.edu.au","password","Jade","Lee")['auth_user_id']
    priv_user1_chan_id = channels_create_v1(user1_id, "Private Channel 1", False)['channel_id']
    priv_user2_chan_id = channels_create_v1(user2_id, "Private Channel 2", False)['channel_id']
    pub_user1_chan_id = channels_create_v1(user1_id, "Public Channel 1", True)['channel_id']
    pub_user2_chan_id = channels_create_v1(user2_id, "Public Channel 2", True)['channel_id']
    channel_join_v1(user1_id, priv_user2_chan_id)
    channel_join_v1(user1_id, pub_user2_chan_id)
    channel_invite_v1(user1_id, priv_user1_chan_id, user2_id)
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
    assert channels_list_v1(user1_id) == {
        'channels': [priv_user1_chan, priv_user2_chan, pub_user1_chan, pub_user2_chan]
    }
    assert channels_list_v1(user2_id) == {
        'channels': [priv_user1_chan, priv_user2_chan, pub_user2_chan]
    }
    assert channels_listall_v1(user1_id) == channels_list_v1(user1_id)
    assert channels_listall_v1(user2_id) == channels_list_v1(user1_id)
    