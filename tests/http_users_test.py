'''Contains http tests for users.py'''
import pytest
import requests
import json
from src.error import AccessError, InputError
from other_functions.request_helper_functions import *
from src.config import url

@pytest.fixture
def registered_user():
    clear_req()
    return auth_register_req('john.doe@unsw.edu.au', '123123', 'John', 'Doe')

def check_user_stats(stats, channels, dms, messages, involvement_rate):
    channels_joined = stats['channels_joined']
    assert channels_joined[-1]['num_channels_joined'] == channels

    dms_joined = stats['dms_joined']
    assert dms_joined[-1]['num_dms_joined'] == dms

    messages_sent = stats['messages_sent']
    assert messages_sent[-1]['num_messages_sent'] == messages

    assert stats['involvement_rate'] == involvement_rate

def check_workspace_stats(stats, channels, dms, messages, utilization_rate):
    channels_exist = stats['channels_exist']
    assert channels_exist[-1]['num_channels_exist'] == channels

    dms_exist = stats['dms_exist']
    assert dms_exist[-1]['num_dms_exist'] == dms

    messages_exist = stats['messages_exist']
    assert messages_exist[-1]['num_messages_exist'] == messages

    assert stats['utilization_rate'] == utilization_rate

"""
The following tests make some assumptions based on the gitlab doc!
 - id dictionary key is now called u_id.
 - users have a key called token.
"""

#################################
#        users/all/req           #
#################################
def test_invalid_token():
    clear_req()
    auth_register_req('jane.doe@unsw.edu.au', '123123', 'jane', 'Doe')
    registered_user_token = 'HMMMMM'
    assert users_all_req(registered_user_token)['code'] == AccessError.code

def test_valid_test(registered_user):
    token = registered_user['token']
    user_id = auth_register_req('jane.doe@unsw.edu.au', '123123', 'jane', 'Doe')['auth_user_id']
    admin_user_remove_req(token, user_id)
    result = users_all_req(token)
    expected = {
        'users':[{
            'email': 'john.doe@unsw.edu.au',
            'handle_str': 'johndoe',
            'name_first': 'John',
            'name_last': 'Doe',
            'u_id': 1,
            'profile_img_url': url + 'imgurl/default.jpg'
        }]
    }
    assert result == expected
#################################
#       user/profile/req        #
#################################
def test_profile_user_not_found(registered_user):
    registered_user_token = registered_user['token']
    assert user_profile_req(registered_user_token, 383)['code'] == InputError.code

def test_profile_invalid_token(registered_user):
    registered_user_id = registered_user['auth_user_id']
    assert user_profile_req("IUdbe", registered_user_id)['code'] == AccessError.code
# not sure how to test this at the moment
# def test_profile_valid_test(registered_user):
#     registered_user_token = registered_user['token']
#     registered_user_id = registered_user['id']
#     result = user_profile_req(registered_user_token, registered_user_id)
#     expected = {"user_id" }
#     assert result == expected
#################################
#    user/profile/setname/req    #
#################################
def test_setname_name_first_too_short(registered_user):
    registered_user_token = registered_user['token']
    assert user_profile_setname_req(registered_user_token, "", "Test")['code'] == InputError.code

def test_setname_name_last_too_short(registered_user):
    registered_user_token = registered_user['token']
    assert user_profile_setname_req(registered_user_token, "Test", "")['code'] == InputError.code

def test_setname_name_first_too_long(registered_user):
    registered_user_token = registered_user['token']
    assert user_profile_setname_req(registered_user_token, "John", "DoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoe")['code'] == InputError.code

def test_setname_name_last_too_long(registered_user):
    registered_user_token = registered_user['token']
    assert user_profile_setname_req(registered_user_token, "JohnJohnJohnJohnJohnJohnJohnJohnJohnJohnJohnJohnJohn", "Doe")['code'] == InputError.code
# Assumption we have - names cannot contain non-alphabetical characters and
# grammer that is not associated with names
# THE BELOW TEST IS NOT BLACKBOX!!!
def test_setname_alphanumeric(registered_user):
    registered_user_token = registered_user['token']
    user_profile_setname_req(registered_user_token, "Mary-Ann", "!@#Doe")
    result_first_name = users_all_req(registered_user_token)['users'][0]['name_first']
    result_last_name = users_all_req(registered_user_token)['users'][0]['name_last']
    expected = ["Mary-Ann", "Doe"]
    assert [result_first_name, result_last_name] == expected


def test_setname_invlid_token(registered_user):
    assert user_profile_setname_req("dOEID", "Janet", "Doe")['code'] == AccessError.code

def test_setname_valid_test(registered_user):
    auth_register_req('jane.doe@unsw.edu.au', '123123', 'jane', 'Doe')
    registered_user_token = registered_user['token']
    registered_user_id = registered_user['auth_user_id']
    returned = user_profile_setname_req(registered_user_token, "Janet", "Doe")
    assert returned == {}
    result_first_name = user_profile_req(registered_user_token, registered_user_id)['user']['name_first']
    result_last_name = user_profile_req(registered_user_token, registered_user_id)['user']['name_last']
    expected = ["Janet", "Doe"]
    assert [result_first_name, result_last_name] == expected
#################################
#     user/profile/setemail/    #
#################################
def test_setmail_email_not_valid(registered_user):
    registered_user_token = registered_user['token']
    assert user_profile_setemail_req(registered_user_token, "john.doe.unsw.edu.au")['code'] == InputError.code

def test_setmail_email_already_used(registered_user):
    registered_user_token = registered_user['token']
    auth_register_req('john.doe1@unsw.edu.au', '123123', 'John', 'Doe')
    assert user_profile_setemail_req(registered_user_token, "john.doe1@unsw.edu.au")['code'] == InputError.code

def test_setmail_invlid_token(registered_user):
    assert user_profile_setemail_req("EFSE", "john.doe1@unsw.edu.au")['code'] == AccessError.code

def test_setmail_valid_test(registered_user):
    auth_register_req('jane.doe@unsw.edu.au', '123123', 'jane', 'Doe')
    registered_user_token = registered_user['token']
    registered_user_id = registered_user['auth_user_id']
    returned = user_profile_setemail_req(registered_user_token, "janet.doe@unsw.ed.au")
    assert returned == {}
    result = user_profile_req(registered_user_token, registered_user_id)['user']['email']
    expected = "janet.doe@unsw.ed.au"
    assert result == expected
#################################
#   user/profile/sethandle/req   #
#################################
def test_sethandle_handle_too_short(registered_user):
    registered_user_token = registered_user['token']
    assert user_profile_sethandle_req(registered_user_token, "12")['code'] == InputError.code

def test_sethandle_handle_too_long(registered_user):
    registered_user_token = registered_user['token']
    assert user_profile_sethandle_req(registered_user_token, "123456789101112131415")['code'] == InputError.code

def test_sethandle_none_alphanumeric(registered_user):
    registered_user_token = registered_user['token']
  
    assert user_profile_sethandle_req(registered_user_token, "johnDoe#@")['code'] == InputError.code
def test_sethandle_handle_already_used(registered_user):
    registered_user2_token = auth_register_req('john.doe1@unsw.edu.au', '123123', 'John', 'Doe')['token']
    # Make sure that user1 has the handle "johndoe". This is done to keep the test blackbox
    assert user_profile_sethandle_req(registered_user2_token, "johndoe")['code'] == InputError.code

def test_sethandle_invlid_token(registered_user):
    assert user_profile_sethandle_req("EFSE", "johnDoe12")['code'] == AccessError.code

def test_sethandle_valid_test(registered_user):
    auth_register_req('jane.doe@unsw.edu.au', '123123', 'jane', 'Doe')
    registered_user_token = registered_user['token']
    registered_user_id = registered_user['auth_user_id']
    returned = user_profile_sethandle_req(registered_user_token, "johnDoe")
    assert returned == {}
    result = user_profile_req(registered_user_token, registered_user_id)['user']['handle_str']
    expected = "johnDoe"
    assert result == expected

#################################
#   user/profile/uploadphoto    #
#################################
# Not really sure how to test these blackbox :(
def test_user_profile_uploadphoto_not_found(registered_user):
    tok = registered_user['token']
    user_id = registered_user['auth_user_id']
    default_image_url = user_profile_req(tok, user_id)['user']['profile_img_url']
    non_jpg = "http://www.cse.unsw.edu.au/~richardb/index_files/RichardBuckland-200.png"
    resp = user_profile_uploadphoto_req(tok, non_jpg, 0, 0, 150 , 150)
    assert resp['code'] == InputError.code
    
    non_link = "http:theresnowaythisisalink"
    resp = user_profile_uploadphoto_req(tok, non_link, 0, 0, 150 , 150)
    assert resp['code'] == InputError.code

    non_http_link = "https://cdn.motor1.com/images/mgl/RPrgg/s1/bmw-m4-competition-kith-design-study-edition-lead-image.webp"
    resp = user_profile_uploadphoto_req(tok, non_http_link, 0, 0, 150 , 150)
    assert resp['code'] == InputError.code

    assert default_image_url == user_profile_req(tok, user_id)['user']['profile_img_url']

def test_user_profile_uploadphoto_invalid_coordinate(registered_user):
    tok = registered_user['token']
    jpg_link = 'http://cgi.cse.unsw.edu.au/~jas/home/pics/jas.jpg'

    resp = user_profile_uploadphoto_req(tok, jpg_link, 150, 150, 0, 0)
    assert resp['code'] == InputError.code

    resp = user_profile_uploadphoto_req(tok, jpg_link, -3, 0, 420, 420)
    assert resp['code'] == InputError.code

def test_user_profile_uploadphoto_invalid_token(registered_user):
    tok = registered_user['token']
    jpg_link = 'http://cgi.cse.unsw.edu.au/~jas/home/pics/jas.jpg'

    resp = user_profile_uploadphoto_req(tok + "asdfgasdf", jpg_link, 150, 150, 0, 0)
    assert resp['code'] == AccessError.code

def test_user_profile_uploadphoto_success(registered_user):
    user1 = auth_register_req("patrick.liang@unsw.com", "katrick", "Patrick", "Liang")

    reg_img_link = 'http://cgi.cse.unsw.edu.au/~morri/morriphoto.jpg'
    u1_img_link = 'http://cgi.cse.unsw.edu.au/~jas/home/pics/jas.jpg'
    
    user_profile_uploadphoto_req(registered_user['token'], reg_img_link, 0, 0, 3957, 3029)
    user_profile_uploadphoto_req(user1['token'], u1_img_link, 0, 0, 158, 199)


#################################
#   user/stats                  #
#################################
def test_user_stats_invalid_token(registered_user):
    assert user_stats_req(123)['code'] == AccessError.code

def test_user_stats_zero(registered_user):
    output = user_stats_req(registered_user['token'])['user_stats']
    check_user_stats(output, 0, 0, 0, 0)

def test_user_stats_success_channels_joined(registered_user):
    user1 = auth_register_req("patrick.liang@unsw.com", "katrick", "Patrick", "Liang")

    chan_id = channels_create_req(registered_user['token'], "Channel 1", True)['channel_id']
    channel_join_req(user1['token'], chan_id)
    channels_create_req(user1['token'], "channel 2", True)

    output1 = user_stats_req(user1['token'])['user_stats']
    check_user_stats(output1, 2, 0, 0, 1)

    output2 = user_stats_req(registered_user['token'])['user_stats']
    check_user_stats(output2, 1, 0, 0, 0.5)

def test_user_stats_success_dms_joined(registered_user):
    user1 = auth_register_req("patrick.liang@unsw.com", "katrick", "Patrick", "Liang")

    chan_id = channels_create_req(registered_user['token'], "Channel 1", True)['channel_id']
    channel_join_req(user1['token'], chan_id)
    channels_create_req(user1['token'], "channel 2", True)

    dm_create_req(registered_user['token'], [user1['auth_user_id']])

    output1 = user_stats_req(user1['token'])['user_stats']
    check_user_stats(output1, 2, 1, 0, 1)

    output2 = user_stats_req(registered_user['token'])['user_stats']
    check_user_stats(output2, 1, 1, 0, 2/3)

def test_user_stats_success_messages(registered_user):
    user1 = auth_register_req("patrick.liang@unsw.com", "katrick", "Patrick", "Liang")

    chan_id = channels_create_req(registered_user['token'], "Channel 1", True)['channel_id']
    channel_join_req(user1['token'], chan_id)
    channels_create_req(user1['token'], "channel 2", True)

    message_send_req(registered_user['token'], chan_id, "bruh 1")
    message_send_req(registered_user['token'], chan_id, "bruh 2")

    output1 = user_stats_req(user1['token'])['user_stats']
    check_user_stats(output1, 2, 0, 0, 1/2)

    output2 = user_stats_req(registered_user['token'])['user_stats']
    check_user_stats(output2, 1, 0, 2, 3/4)

def test_user_stats_remove_dm(registered_user):
    user1 = auth_register_req("patrick.liang@unsw.com", "katrick", "Patrick", "Liang")

    channels_create_req(registered_user['token'], "Channel 2", True)

    dm_id = dm_create_req(registered_user['token'], [user1['auth_user_id']])['dm_id']

    dm_remove_req(registered_user['token'], dm_id)

    output = user_stats_req(registered_user['token'])['user_stats']
    check_user_stats(output, 1, 0, 0, 1)

def test_user_stats_remove_message(registered_user):
    auth_register_req("patrick.liang@unsw.com", "katrick", "Patrick", "Liang")

    chan_id = channels_create_req(registered_user['token'], "Channel 2", True)['channel_id']
    msg_id = message_send_req(registered_user['token'], chan_id, "bruh removed")['message_id']
    message_remove_req(registered_user['token'], msg_id)

    output = user_stats_req(registered_user['token'])['user_stats']
    check_user_stats(output, 1, 0, 1, 1)

#################################
#   users/stats                 #
#################################

def test_users_stats_invalid_token(registered_user):
    assert users_stats_req('123')['code'] == AccessError.code

def test_users_stats_one_user(registered_user):
    output = users_stats_req(registered_user['token'])['workspace_stats']
    check_workspace_stats(output, 0, 0, 0, 0)

def test_users_stats_remove_user(registered_user):
    user1 = auth_register_req("patrick.liang@unsw.com", "katrick", "Patrick", "Liang")
    auth_register_req("john.citizen@unsw.com", "password", "John", "Citizen")

    chan_id = channels_create_req(registered_user['token'], "Channel 1", True)['channel_id']
    channels_create_req(registered_user['token'], "Channel 2", True)
    channels_create_req(registered_user['token'], "Channel 3", True)

    channel_join_req(user1['token'], chan_id)

    output = users_stats_req(registered_user['token'])['workspace_stats']
    check_workspace_stats(output, 3, 0, 0, 2/3)

    admin_user_remove_req(registered_user['token'], user1['auth_user_id'])

    output = users_stats_req(registered_user['token'])['workspace_stats']
    check_workspace_stats(output, 3, 0, 0, 1/2)

def test_users_stats_mult_user_channels(registered_user):
    user1 = auth_register_req("patrick.liang@unsw.com", "katrick", "Patrick", "Liang")
    auth_register_req("john.citizen@unsw.com", "password", "John", "Citizen")

    chan_id = channels_create_req(registered_user['token'], "Channel 1", True)['channel_id']
    channels_create_req(registered_user['token'], "Channel 2", True)
    channels_create_req(registered_user['token'], "Channel 3", True)

    channel_join_req(user1['token'], chan_id)

    output = users_stats_req(registered_user['token'])['workspace_stats']
    check_workspace_stats(output, 3, 0, 0, 2/3)

def test_users_stats_mult_user_dms(registered_user):
    user1 = auth_register_req("patrick.liang@unsw.com", "katrick", "Patrick", "Liang")
    user2 = auth_register_req("john.citizen@unsw.com", "password", "John", "Citizen")
    auth_register_req("alex.nguyen@unsw.com", "bigsausage", "Alex", "Nguyen")

    channels_create_req(registered_user['token'], "Channel 2", True)

    dm_create_req(registered_user['token'], [user1['auth_user_id'], user2['auth_user_id']])

    output = users_stats_req(registered_user['token'])['workspace_stats']
    check_workspace_stats(output, 1, 1, 0, 3/4)

def test_users_stats_mult_user_messages(registered_user):
    user1 = auth_register_req("patrick.liang@unsw.com", "katrick", "Patrick", "Liang")
    user2 = auth_register_req("john.citizen@unsw.com", "password", "John", "Citizen")
    auth_register_req("alex.nguyen@unsw.com", "bigsausage", "Alex", "Nguyen")

    chan_id = channels_create_req(registered_user['token'], "Channel 2", True)['channel_id']

    message_send_req(registered_user['token'], chan_id, "bruh 1")
    message_send_req(registered_user['token'], chan_id, "bruh 2")
    message_send_req(registered_user['token'], chan_id, "bruh 3")

    dm_create_req(registered_user['token'], [user1['auth_user_id'], user2['auth_user_id']])

    output = users_stats_req(registered_user['token'])['workspace_stats']
    check_workspace_stats(output, 1, 1, 3, 3/4)
    clear_req()