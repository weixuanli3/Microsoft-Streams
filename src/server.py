'''Contains routes for the different functions'''
import sys
import signal
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import InputError
from src import config
from src.auth import auth_login_v1, auth_passwordreset_request_v1, auth_passwordreset_reset_v1, auth_register_v1, auth_logout_v1
from src.admin import admin_user_remove_id, admin_userpermission_change_v1
from src.channel import channel_invite_v1, channel_details_v1, channel_messages_v1
from src.channel import channel_join_v1, channel_leave_v1, channel_add_owner_v1, channel_remove_owner_v1
from src.channels import  channels_list_v1, channels_listall_v1, channels_create_v1
from src.dm import dm_create_v1, dm_list_v1, dm_remove_v1, dm_details_v1, dm_leave_v1, dm_messages_v1
from src.user import users_all_v1, user_profile_v1, user_profile_setname_v1, user_profile_setemail_v1, user_profile_sethandle_v1
from src.message import message_send_v1, message_edit_v1, message_senddm_v1, message_remove_v1
from src.other import clear_v1
from src.admin import admin_user_remove_id, admin_userpermission_change_v1
from src.echo import echo
import src.data_store
import json

def quit_gracefully(*args):
    '''For coverage'''
    exit(0)

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

#### NO NEED TO MODIFY ABOVE THIS POINT, EXCEPT IMPORTS

# Example
@APP.route("/echo", methods=['GET'])
def echo_route():
    value = request.args.get('value')
    return json.dumps(echo(value))

##########AUTH.PY##########
# Register a user
@APP.route("/auth/register/v2", methods=['POST'])
def auth_register():
    request_data = request.get_json(force = True)
    return json.dumps(auth_register_v1(request_data['email'], request_data['password'], request_data['name_first'], request_data['name_last']))

# Login a user
@APP.route("/auth/login/v2", methods=['POST'])
def auth_login():
    request_data = request.get_json(force = True)
    return json.dumps(auth_login_v1(request_data['email'], request_data['password']))

# Login a user
@APP.route("/auth/logout/v1", methods=['POST'])
def auth_logout():
    request_data = request.get_json(force = True)
    return json.dumps(auth_logout_v1(request_data['token']))

# Request password reset
@APP.route("/auth/passwordreset/request/v1", methods=['POST'])
def auth_pasword_reset_request():
    request_data = request.get_json(force = True)
    return json.dumps(auth_passwordreset_request_v1(request_data['email']))

# Actually change password
@APP.route("/auth/passwordreset/reset/v1", methods=['POST'])
def auth_pasword_reset():
    request_data = request.get_json(force = True)
    return json.dumps(auth_passwordreset_reset_v1(request_data['reset_code'], request_data['new_password']))

##########CHANNEL.PY##########
# Invite user to channel
@APP.route("/channel/invite/v2", methods=['POST'])
def channel_invite():
    request_data = request.get_json(force = True)
    return json.dumps(channel_invite_v1(request_data['token'], request_data['channel_id'], request_data['u_id']))

# Get channel details
@APP.route("/channel/details/v2", methods=['GET'])
def channel_details():
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    return json.dumps(channel_details_v1(token, channel_id))

# Get channel number of channel messages
@APP.route("/channel/messages/v2", methods=['GET'])
def channel_messages():
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    start = int(request.args.get('start'))
    return json.dumps(channel_messages_v1(token, channel_id, start))

# Make a particular channel
@APP.route("/channel/join/v2", methods=['POST'])
def channel_join():
    request_data = request.get_json(force = True)
    return json.dumps(channel_join_v1(request_data['token'], request_data['channel_id']))

# Leave a particular channel
@APP.route("/channel/leave/v1", methods=['POST'])
def channel_leave():
    request_data = request.get_json(force = True)
    return json.dumps(channel_leave_v1(request_data['token'], request_data['channel_id']))

# Make a particular channel
@APP.route("/channel/addowner/v1", methods=['POST'])
def channel_add_owner():
    request_data = request.get_json(force = True)
    return json.dumps(channel_add_owner_v1(request_data['token'], request_data['channel_id'], request_data['u_id']))

# Make a particular channel
@APP.route("/channel/removeowner/v1", methods=['POST'])
def channel_remove_owner():
    request_data = request.get_json(force = True)
    return json.dumps(channel_remove_owner_v1(request_data['token'], request_data['channel_id'], request_data['u_id']))


##########CHANNELS.PY##########

# List channels user part of
@APP.route("/channels/list/v2", methods=['GET'])
def channels_list():
    token = request.args.get('token')
    return json.dumps(channels_list_v1(token))

# List all channels
@APP.route("/channels/listall/v2", methods=['GET'])
def channels_listall():
    token = request.args.get('token')
    return json.dumps(channels_listall_v1(token))

# Create a channel
@APP.route("/channels/create/v2", methods=['POST'])
def channels_create():
    request_data = request.get_json(force = True)
    return json.dumps(channels_create_v1(request_data['token'], request_data['name'], request_data['is_public']))

##########DM.PY##########

# Create a dm
@APP.route("/dm/create/v1", methods=['POST'])
def dm_create():
    request_data = request.get_json(force = True)
    return json.dumps(dm_create_v1(request_data['token'], request_data['u_ids']))

# List DMs
@APP.route("/dm/list/v1", methods=['GET'])
def dm_list():
    token = request.args.get('token')
    return json.dumps(dm_list_v1(token))

# Remove a user from the channel
@APP.route("/dm/remove/v1", methods=['DELETE'])
def dm_remove():
    request_data = request.get_json(force = True)
    return json.dumps(dm_remove_v1(request_data['token'], request_data['dm_id']))

# Give details of DM
@APP.route("/dm/details/v1", methods=['GET'])
def dm_details():
    token = request.args.get('token')
    dm_id = int(request.args.get('dm_id'))
    return json.dumps(dm_details_v1(token, dm_id))

# Make a user leave a channel
@APP.route("/dm/leave/v1", methods=['POST'])
def dm_leave():
    request_data = request.get_json(force = True)
    return json.dumps(dm_leave_v1(request_data['token'], request_data['dm_id']))

# DM messages
@APP.route("/dm/messages/v1", methods=['GET'])
def dm_messages():
    token = request.args.get('token')
    dm_id = int(request.args.get('dm_id'))
    start = int(request.args.get('start'))
    return json.dumps(dm_messages_v1(token, dm_id, start))

##########OTHER.PY##########
      
# Clear
@APP.route("/clear/v1", methods=['DELETE'])
def clear():
    return json.dumps(clear_v1())

##########ADMIN.PY##########

# Admin remove
@APP.route("/admin/user/remove/v1", methods=['DELETE'])
def admin_remove():
    request_data = request.get_json(force = True)
    return json.dumps(admin_user_remove_id(request_data['token'], request_data['u_id']))

# Admin user permisions
@APP.route("/admin/userpermission/change/v1", methods=['POST'])
def admin_change():
    request_data = request.get_json(force = True)
    return json.dumps(admin_userpermission_change_v1(request_data['token'], request_data['u_id'], request_data['permission_id']))


##########USER.PY##########

# 
@APP.route("/user/profile/v1", methods=['GET'])
def user_profile():
    token = request.args.get('token')
    u_id = int(request.args.get('u_id'))
    return json.dumps(user_profile_v1(token, u_id))

# 
@APP.route("/users/all/v1", methods=['GET'])
def users_all():
    token = request.args.get('token')
    return json.dumps(users_all_v1(token))

# 
@APP.route("/user/profile/setname/v1", methods=['PUT'])
def user_profile_setname():
    request_data = request.get_json(force = True)
    return json.dumps(user_profile_setname_v1(request_data['token'], request_data['name_first'], request_data['name_last']))

# 
@APP.route("/user/profile/setemail/v1", methods=['PUT'])
def user_profile_setemail():
    request_data = request.get_json(force = True)
    return json.dumps(user_profile_setemail_v1(request_data['token'], request_data['email']))

@APP.route("/user/profile/sethandle/v1", methods=['PUT'])
def user_profile_sethandle():
    request_data = request.get_json(force = True)
    return json.dumps(user_profile_sethandle_v1(request_data['token'], request_data['handle_str']))

##########MESSAGE.PY##########

@APP.route("/message/send/v1", methods=['POST'])
def message_send():
    request_data = request.get_json(force = True)
    return json.dumps(message_send_v1(request_data['token'], request_data['channel_id'], request_data['message']))

@APP.route("/message/edit/v1", methods=['PUT'])
def message_edit():
    request_data = request.get_json(force = True)
    return json.dumps(message_edit_v1(request_data['token'], request_data['message_id'], request_data['message']))

@APP.route("/message/remove/v1", methods=['DELETE'])
def message_delete():
    request_data = request.get_json(force = True)
    return json.dumps(message_remove_v1(request_data['token'],request_data['message_id']))

@APP.route("/message/senddm/v1", methods=['POST'])
def message_senddm():
    request_data = request.get_json(force = True)
    return json.dumps(message_senddm_v1(request_data['token'], request_data['dm_id'], request_data['message']))

##########MESSAGE.PY##########

#### NO NEED TO MODIFY BELOW THIS POINT

if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully) # For coverage
    APP.run(port=config.port) # Do not edit this port