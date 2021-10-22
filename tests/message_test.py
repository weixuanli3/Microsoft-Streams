'''Contains tests for message.py'''
import pytest

from src.auth import auth_register_v1
from src.channels import channels_create_v1, channels_list_v1, channels_listall_v1
from src.channel import channel_join_v1, channel_invite_v1
from src.dm import dm_create_v1
from src.error import InputError
from src.error import AccessError
from src.other import clear_v1
from src.message import message_send_v1, message_edit_v1, message_send_v1, message_senddm_v1, message_remove_v1

# The following tests are for message_send_v1
def test_message_send_channel_id_invalid():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    with pytest.raises(InputError): 
        message_send_v1(token1, 7643829, "Hi there!")

def test_message_send_multi_msgs():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    channel_id = channels_create_v1(token1, "Channel 1", True)['channel_id']
    msg1_id = message_send_v1(token1, channel_id, "Hi there!")['message_id']
    msg2_id = message_send_v1(token1, channel_id, "Hi there!")['message_id']
    assert msg1_id != msg2_id

def test_message_send_msg_length_too_small():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    channel_id = channels_create_v1(token1, "Channel 1", True)['channel_id']  
    with pytest.raises(InputError): 
        message_send_v1(token1, channel_id, "")

def test_message_send_msg_length_too_big():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    channel_id = channels_create_v1(token1, "Channel 1", True)['channel_id']
    with pytest.raises(InputError): 
        message_send_v1(token1, channel_id, """Altruism is the principle and moral practice of concern for 
            happiness of other human beings or other animals, resulting in a quality of life both material and spiritual. 
            It is a traditional virtue in many cultures and a core aspect of various religious traditions and secular worldviews, 
            though the concept of others toward whom concern should be directed can vary among cultures and religions. 
            In an extreme case, altruism may become a synonym of selflessness, which is the opposite of selfishness. 
            The word altrusim was popularized (and possibly coined) by the French philosopher Auguste Comte in French, 
            as altruisme, for an antonym of egoism.[1][2] He derived it from the Italian altrui, which in turn was derived from Latin 
            alteri, meaning other people or somebody else.[3] Altruism in biological observations in field populations of the day organisms 
            is an individual performing an action which is at a cost to themselves (e.g., pleasure and quality of life, time, probability of 
            survival or reproduction), but benefits, either directly or indirectly, another""")
    
def test_message_send_token_invalid():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    channel_id = channels_create_v1(token1, "Channel 1", True)['channel_id']
    with pytest.raises(AccessError): 
        message_send_v1(78534290, channel_id, "Hi there!")

def test_message_send_user_not_part_of_channel():  # NEED TO CHECK FOR GLOBAL USERS
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    token2 = auth_register_v1("jane.doe@unsw.edu.au", "password","Jane","Doe")['token']
    channel_id = channels_create_v1(token1, "Channel 1", True)['channel_id']
    with pytest.raises(AccessError): 
        message_send_v1(token2, channel_id, "Hi there!")
    
# The following tests are for message_edit_v1
def test_message_edit_msg_length_too_big():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    channel_id = channels_create_v1(token1, "Channel 1", True)['channel_id']
    msg_id = message_send_v1(token1, channel_id, "Hi there!")['message_id']
    with pytest.raises(InputError): 
        message_edit_v1(token1, msg_id, """Altruism is the principle and moral practice of concern for 
        happiness of other human beings or other animals, resulting in a quality of life both material and spiritual. 
        It is a traditional virtue in many cultures and a core aspect of various religious traditions and secular worldviews, 
        though the concept of others toward whom concern should be directed can vary among cultures and religions. 
        In an extreme case, altruism may become a synonym of selflessness, which is the opposite of selfishness. 
        The word altrusim was popularized (and possibly coined) by the French philosopher Auguste Comte in French, 
        as altruisme, for an antonym of egoism.[1][2] He derived it from the Italian altrui, which in turn was derived from Latin 
        alteri, meaning other people or somebody else.[3] Altruism in biological observations in field populations of the day organisms 
        is an individual performing an action which is at a cost to themselves (e.g., pleasure and quality of life, time, probability of 
        survival or reproduction), but benefits, either directly or indirectly, another""")

def test_message_edit_token_invalid():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    channel_id = channels_create_v1(token1, "Channel 1", True)['channel_id']
    msg_id = message_send_v1(token1, channel_id, "Hi there!")['message_id']
    with pytest.raises(AccessError): 
        message_edit_v1(546783, msg_id, "Hi there!")

def test_message_edit_msg_id_does_not_exist():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    channel_id = channels_create_v1(token1, "Channel 1", True)['channel_id']
    message_send_v1(token1, channel_id, "Hi there!")
    with pytest.raises(InputError): 
        message_edit_v1(token1, 5462, "Hi there!")

def test_message_edit_msg_not_part_of_channel():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    token2 = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['token']
    channel1_id = channels_create_v1(token1, "Channel 1", True)['channel_id']
    channel2_id = channels_create_v1(token2, "Channel 1", True)['channel_id']
    message_send_v1(token1, channel1_id, "Hi there!")
    msg2_id = message_send_v1(token2, channel2_id, "Hi there!")['message_id']
    with pytest.raises(InputError):
        message_edit_v1(token1, msg2_id, "Hi there!")

def test_message_edit_msg_not_part_of_DM_user_in():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    return2 = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")
    token3 = auth_register_v1("john.bob@aunsw.edu.au", "naisud", "John", "Bob")['token']
    token2 = return2['token']
    user2_id = return2['auth_user_id']
    dm1_id = dm_create_v1(token1, [user2_id])['dm_id']
    message_senddm_v1(token1, dm1_id, "Hi there!")
    msg2_id = message_senddm_v1(token2, dm1_id, "Hi there!")['message_id']
    with pytest.raises(InputError): 
        message_edit_v1(token3, msg2_id, "Hi there!")

def test_message_edit_msg_DM_valid():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    user2_id = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['auth_user_id']
    dm1_id = dm_create_v1(token1, [user2_id])['dm_id']
    msg1_id = message_senddm_v1(token1, dm1_id, "Hi there!")['message_id']
    msg2_id = message_senddm_v1(token1, dm1_id, "Hey there!")['message_id']
    message_edit_v1(token1, msg1_id, "Hi there!")
    message_edit_v1(token1, msg2_id, "Hi there!")

def test_message_edit_msg_valid():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    channel_id = channels_create_v1(token1, "Channel 1", True)['channel_id']
    msg_id = message_send_v1(token1, channel_id, "Hi there!")['message_id']
    message_edit_v1(token1, msg_id, "Hi there!")

def test_message_edit_msg_empty():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    channel_id = channels_create_v1(token1, "Channel 1", True)['channel_id']
    msg_id = message_send_v1(token1, channel_id, "Hi there!")['message_id']
    message_edit_v1(token1, msg_id, "")

def test_message_edit_dm_msg_empty():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    user2_id = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['auth_user_id']
    dm1_id = dm_create_v1(token1, [user2_id])['dm_id']
    msg_id = message_senddm_v1(token1, dm1_id, "Hi there!")['message_id']
    message_edit_v1(token1, msg_id, "")

def test_message_edit_msg_id_not_sent_by_non_owner_channel():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    token2 = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['token']
    channel_id = channels_create_v1(token1, "Channel 1", True)['channel_id']
    channel_join_v1(token2, channel_id)
    msg1_id = message_send_v1(token1, channel_id, "Hi there!")['message_id']
    with pytest.raises(AccessError): 
        message_edit_v1(token2, msg1_id, "Hi there!")

def test_message_edit_msg_id_not_sent_by_non_owner_dm():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    return2 = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")
    token2 = return2['token']
    user2_id = return2['auth_user_id']
    dm_id = dm_create_v1(token1, [user2_id])['dm_id']
    msg1_id = message_senddm_v1(token1, dm_id, "Hi there!")['message_id']
    with pytest.raises(AccessError): 
        message_edit_v1(token2, msg1_id, "Hi there!")

def test_message_edit_msg_id_not_sent_by_owner():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    token2 = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['token']
    channel_id = channels_create_v1(token1, "Channel 1", True)['channel_id']
    channel_join_v1(token2, channel_id)
    message_send_v1(token1, channel_id, "Hi there!")
    msg1_id = message_send_v1(token2, channel_id, "Hi there!")['message_id']
    message_edit_v1(token1, msg1_id, "Hi there!")

# The following tests are for message_remove_v1
def test_message_remove_msg_not_part_of_channel():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    token2 = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['token']
    channel1_id = channels_create_v1(token1, "Channel 1", True)['channel_id']
    channel2_id = channels_create_v1(token2, "Channel 1", True)['channel_id']
    message_send_v1(token1, channel1_id, "Hi there!")
    msg2_id = message_send_v1(token2, channel2_id, "Hi there!")
    with pytest.raises(InputError): 
        message_remove_v1(token1, msg2_id)

def test_message_remove_msg_not_part_of_DM_user_in():
    clear_v1()
    return1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")
    token2 = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['token']
    token1 = return1['token']
    user1_id = return1['auth_user_id']
    dm1_id = dm_create_v1(token2, [user1_id])['dm_id']
    msg1_id = message_senddm_v1(token2, dm1_id, "Hi there!")
    with pytest.raises(InputError): 
        message_remove_v1(token1, msg1_id)

def test_message_remove_msg_DM_valid():
    clear_v1()
    return1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")
    return2 = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")
    token1 = return1['token']
    user2_id = return2['auth_user_id']
    dm1_id = dm_create_v1(token1, [user2_id])['dm_id']
    msg1_id = message_senddm_v1(token1, dm1_id, "Hi there!")['message_id']
    msg2_id = message_senddm_v1(token1, dm1_id, "Hey there!")['message_id']
    message_remove_v1(token1, msg2_id)
    message_remove_v1(token1, msg1_id)

def test_message_remove_valid_channel():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    token2 = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['token']
    channel_id = channels_create_v1(token1, "Channel 1", True)['channel_id']
    channel_join_v1(token2, channel_id)
    msg_id = message_send_v1(token2, channel_id, "Hi there!")['message_id']
    message_remove_v1(token2, msg_id)

def test_message_remove_token_invalid():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    channel_id = channels_create_v1(token1, "Channel 1", True)['channel_id']
    msg_id = message_send_v1(token1, channel_id, "Hi there!")['message_id']
    with pytest.raises(AccessError): 
        message_remove_v1(37480259, msg_id)

def test_message_remove_msg_id_does_not_exist():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    channel_id = channels_create_v1(token1, "Channel 1", True)['channel_id']
    message_send_v1(token1, channel_id, "Hi there!")
    with pytest.raises(InputError): 
        message_remove_v1(token1, 984735)

def test_message_remove_msg_id_not_sent_by_non_owner_channel():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    token2 = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['token']
    channel_id = channels_create_v1(token1, "Channel 1", True)['channel_id']
    channel_join_v1(token2, channel_id)
    message_send_v1(token1, channel_id, "Hi there!")
    msg1_id = message_send_v1(token1, channel_id, "Hi there!")['message_id']
    with pytest.raises(AccessError): 
        message_remove_v1(token2, msg1_id)

def test_message_remove_msg_id_not_sent_by_non_owner_dm():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    return2 = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")
    token2 = return2['token']
    user2_id = return2['auth_user_id']
    dm_id = dm_create_v1(token1, [user2_id])['dm_id']
    msg1_id = message_senddm_v1(token1, dm_id, "Hi there!")['message_id']
    with pytest.raises(AccessError): 
        message_remove_v1(token2, msg1_id)

def test_message_remove_msg_id_sent_by_owner():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    token2 = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")['token']
    channel_id = channels_create_v1(token1, "Channel 1", True)['channel_id']
    channel_join_v1(token2, channel_id)
    message_send_v1(token1, channel_id, "Hi there!")
    msg1_id = message_send_v1(token2, channel_id, "Hi there!")['message_id']
    message_remove_v1(token1, msg1_id)

# The following tests are for message_senddm
def test_message_senddm_msg_DM_not_part_of():
    clear_v1()
    return1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")
    return2 = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")
    return3 = auth_register_v1("john.bob@aunsw.edu.au", "naisud", "John", "Bob")
    token1 = return1['token']
    token3 = return3['token']
    user2_id = return2['auth_user_id']
    dm1_id = dm_create_v1(token1, [user2_id])['dm_id']
    with pytest.raises(AccessError): 
        message_senddm_v1(token3, dm1_id, "Hi there!")


def test_message_senddm_send_multi_msgs():
    clear_v1()
    return1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")
    return2 = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")
    token1 = return1['token']
    user2_id = return2['auth_user_id']
    dm1_id = dm_create_v1(token1, [user2_id])['dm_id']
    msg1_id = message_senddm_v1(token1, dm1_id, "Hi there!")['message_id']
    msg2_id = message_senddm_v1(token1, dm1_id, "Hi there!")['message_id']
    assert msg1_id != msg2_id

def test_message_senddm_send_single_msg():
    clear_v1()
    return1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")
    return2 = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")
    token1 = return1['token']
    user2_id = return2['auth_user_id']
    dm1_id = dm_create_v1(token1, [user2_id])['dm_id']
    dm2_id = dm_create_v1(token1, [user2_id])['dm_id']
    message_senddm_v1(token1, dm1_id, "Hi there!")
    message_senddm_v1(token1, dm2_id, "Hi there!")

def test_message_senddm_token_invalid():
    clear_v1()
    token1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")['token']
    return2 = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")
    user2_id = return2['auth_user_id']
    dm1_id = dm_create_v1(token1, [user2_id])['dm_id']
    with pytest.raises(AccessError):
        message_senddm_v1(42342, dm1_id, "Hi there!")

def test_invalid_dm_id():
    clear_v1()
    return1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")
    token1 = return1['token']
    with pytest.raises(InputError):
        message_senddm_v1(token1, 434, "Hi there!")

def test_message_senddm_msg_length_too_small():
    clear_v1()
    return1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")
    return2 = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")
    token1 = return1['token']
    user2_id = return2['auth_user_id']
    dm1_id = dm_create_v1(token1, [user2_id])['dm_id']
    with pytest.raises(InputError):
        message_senddm_v1(token1, dm1_id, "")

def test_message_senddm_msg_length_too_big():
    clear_v1()
    return1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")
    return2 = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")
    token1 = return1['token']
    user2_id = return2['auth_user_id']
    dm1_id = dm_create_v1(token1, [user2_id])['dm_id']
    with pytest.raises(InputError):
        message_senddm_v1(token1, dm1_id,  """Altruism is the principle and moral practice of concern for 
            happiness of other human beings or other animals, resulting in a quality of life both material and spiritual. 
            It is a traditional virtue in many cultures and a core aspect of various religious traditions and secular worldviews, 
            though the concept of others toward whom concern should be directed can vary among cultures and religions. 
            In an extreme case, altruism may become a synonym of selflessness, which is the opposite of selfishness. 
            The word altrusim was popularized (and possibly coined) by the French philosopher Auguste Comte in French, 
            as altruisme, for an antonym of egoism.[1][2] He derived it from the Italian altrui, which in turn was derived from Latin 
            alteri, meaning other people or somebody else.[3] Altruism in biological observations in field populations of the day organisms 
            is an individual performing an action which is at a cost to themselves (e.g., pleasure and quality of life, time, probability of 
            survival or reproduction), but benefits, either directly or indirectly, another""")

def test_message_senddm_user_not_part_of_DM():  # I assume global owners can’t do this either
    clear_v1()
    return1 = auth_register_v1("john.doe@aunsw.edu.au","password","John","Doe")
    return2 = auth_register_v1("john.smith@aunsw.edu.au", "naisud", "John", "Smith")
    return3 = auth_register_v1("john.green@aunsw.edu.au", "naisud", "John", "Green")
    token1 = return1['token']
    token3 = return3['token']
    user2_id = return2['auth_user_id']
    dm1_id = dm_create_v1(token1, [user2_id])['dm_id']
    with pytest.raises(AccessError):
        message_senddm_v1(token3, dm1_id, "Hi there!")
