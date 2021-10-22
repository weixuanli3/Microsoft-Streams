'''Contains http tests for channels.py'''
import pytest
import requests
import json
from src.error import AccessError, InputError
from src.request_helper_functions import *
from src.config import url

# The following tests channels_create_req
def test_channels_create_invalid_auth_user_id():
    clear_req()
    assert channels_create_req(1, "First Channel", True)['code'] == AccessError.code

def test_channels_create_empty_channel_name():
    clear_req()
    token = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    assert channels_create_req(token, "", True)['code'] == InputError.code

def test_channels_create_long_channel_name():
    clear_req()
    token = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    assert channels_create_req(token, "Lengthofchanneltoolarge!", True)['code'] == InputError.code

def test_channels_create_success_public():
    clear_req()
    token = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    channels_create_req(token, "Channel 1", True)

def test_channels_create_name_white_space():
    clear_req()
    token = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    assert channels_create_req(token, " ", True)['code'] == InputError.code

def test_channels_create_success_private():
    clear_req()
    token = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    channels_create_req(token, "Channel 1", False)

# Call channels_list with no channels
def test_channels_list_no_channels():
    clear_req()
    token = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    assert channels_list_req(token) == {
        'channels': []
    }

# Call channels_listall with no channels
def test_channels_listall_no_channels_all():
    clear_req()
    token = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    assert channels_listall_req(token) == {
        'channels': []
    }

# Call channels_list with only private channels
def test_channels_list_all_private():
    clear_req()
    user_data = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")
    chan1_id = channels_create_req(user_data['token'], "Private Channel 1", False)['channel_id']
    token = auth_register_req("jade.lee@aunsw.edu.au","password","Jade","Lee")['token']
    chan2_id = channels_create_req(token, "Private Channel 2", False)['channel_id']
    channel_invite_req(token, chan2_id, user_data['auth_user_id'])
    assert channels_list_req(user_data['token']) == {
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
    clear_req()
    user_data = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")
    chan1_id = channels_create_req(user_data['token'], "Public Channel 1", True)['channel_id']
    token = auth_register_req("jade.lee@aunsw.edu.au","password","Jade","Lee")['token']
    chan2_id = channels_create_req(token, "Public Channel 2", True)['channel_id']
    channel_invite_req(token, chan2_id, user_data['auth_user_id'])
    assert channels_list_req(user_data['token']) == {
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
    clear_req()
    user_data = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")
    chan1_id = channels_create_req(user_data['token'], "Public Channel", True)['channel_id']
    token = auth_register_req("jade.lee@aunsw.edu.au","password","Jade","Lee")['token']
    chan2_id = channels_create_req(token, "Private Channel", False)['channel_id']
    channel_invite_req(token, chan2_id, user_data['auth_user_id'])
    assert channels_list_req(user_data['token']) == {
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
    clear_req()
    token = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan1_id = channels_create_req(token, "Public Channel 1", True)['channel_id']
    chan2_id = channels_create_req(token, "Public Channel 2", True)['channel_id']
    assert channels_list_req(token) == {
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
    clear_req()
    token = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan1_id = channels_create_req(token, "Public Channel 1", True)['channel_id']
    chan2_id = channels_create_req(token, "Private Channel 1", False)['channel_id']
    assert channels_list_req(token) == {
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
    clear_req()
    assert channels_list_req(0)['code'] == AccessError.code

# Call channels_listall with only private channels
def test_channels_listall_list_all_all_private():
    clear_req()
    user_data = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")
    chan1_id = channels_create_req(user_data['token'], "Private Channel 1", False)['channel_id']
    token = auth_register_req("jade.lee@aunsw.edu.au","password","Jade","Lee")['token']
    chan2_id = channels_create_req(token, "Private Channel 2", False)['channel_id']
    channel_invite_req(token, chan2_id, user_data['auth_user_id'])
    assert channels_listall_req(user_data['token']) == {
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
    clear_req()
    token1 = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan1_id = channels_create_req(token1, "Public Channel 1", False)['channel_id']
    token2 = auth_register_req("jade.lee@aunsw.edu.au","password","Jade","Lee")['token']
    chan2_id = channels_create_req(token2, "Public Channel 2", False)['channel_id']
    channel_join_req(token1, chan2_id)
    assert channels_listall_req(token1) == {
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
    clear_req()
    user_data = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")
    token = auth_register_req("jade.lee@aunsw.edu.au","password","Jade","Lee")['token']
    chan1_id = channels_create_req(token, "Public Channel 1", True)['channel_id']
    chan2_id = channels_create_req(token, "Private Channel 1", False)['channel_id']
    channel_invite_req(token, chan2_id, user_data['auth_user_id'])
    channel_join_req(user_data['token'], chan1_id)
    assert channels_listall_req(user_data['token']) == {
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
    clear_req()
    token = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan1_id = channels_create_req(token, "Private Channel 1", False)['channel_id']
    chan2_id = channels_create_req(token, "Public Channel 1", True)['channel_id']
    assert channels_listall_req(token) == {
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
    clear_req()
    assert channels_listall_req(0)['code'] == AccessError.code

# Call channels_list with both private and public channels
def test_channels_list_channels_list_default():
    clear_req()
    token1 = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan_priv = channels_create_req(token1, "Private Channel", False)['channel_id']
    chan1_id = channels_create_req(token1, "Public Channel 1", False)['channel_id']
    token2 = auth_register_req("jade.lee@aunsw.edu.au","password","Jade","Lee")['token']
    chan2_id = channels_create_req(token2, "Public Channel 2", False)['channel_id']
    channel_join_req(token1, chan2_id)
    assert channels_list_req(token1) == {
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
    assert channels_listall_req(token1) == {
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
    clear_req()
    clear_req()
    token1 = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    chan_priv = channels_create_req(token1, "Private Channel", False)['channel_id']
    chan1_id = channels_create_req(token1, "Public Channel 1", False)['channel_id']
    token2 = auth_register_req("jade.lee@aunsw.edu.au","password","Jade","Lee")['token']
    chan2_id = channels_create_req(token2, "Public Channel 2", False)['channel_id']
    channel_join_req(token1, chan2_id)
    assert channels_listall_req(token1) == {
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
    clear_req()
    token = auth_register_req("john.doe@aunsw.edu.au","password","John","Doe")['token']
    user_data = auth_register_req("jade.lee@aunsw.edu.au","password","Jade","Lee")
    priv_user1_chan_id = channels_create_req(token, "Private Channel 1", False)['channel_id']
    priv_user2_chan_id = channels_create_req(user_data['token'], "Private Channel 2", False)['channel_id']
    pub_user1_chan_id = channels_create_req(token, "Public Channel 1", True)['channel_id']
    pub_user2_chan_id = channels_create_req(user_data['token'], "Public Channel 2", True)['channel_id']
    channel_join_req(token, priv_user2_chan_id)
    channel_join_req(token, pub_user2_chan_id)
    channel_invite_req(token, priv_user1_chan_id, user_data['auth_user_id'])
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
    assert channels_list_req(token) == {
        'channels': [priv_user1_chan, priv_user2_chan, pub_user1_chan, pub_user2_chan]
    }
    assert channels_list_req(user_data['token']) == {
        'channels': [priv_user1_chan, priv_user2_chan, pub_user2_chan]
    }
    assert channels_listall_req(token) == channels_list_req(token)
    assert channels_listall_req(user_data['token']) == channels_list_req(token)
