'''Contains tests for admin.py'''
import pytest

from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.channel import channel_invite_v1, channel_leave_v1, channel_messages_v1
from src.channel import channel_join_v1
from src.channel import channel_details_v1
from src.error import InputError
from src.error import AccessError
from src.other import clear_v1
from src.data_store import get_u_id

# Tests for admin/user/remove/v1


# Tests for admin/userpermission/change/v1

