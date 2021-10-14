# import pytest
# from src.auth import auth_register_v1, auth_login_v1
# from src.other import clear_v1
# from src.user import users_all_v1
# from src.error import InputError

# @pytest.fixture
# def registered_user():
#     clear_v1()
#     return auth_register_v1('john.doe@unse.edu.au', '123123', 'John', 'Doe')

# #################################
# #        users/all/v1           #
# #################################

# def test_many_registered_users(registered_user):

#     auth_register_v1('john.doe1@unse.edu.au', '123123', 'John', 'Doe')
#     auth_register_v1('john.doe2@unse.edu.au', '123123', 'John', 'Doe')
#     auth_register_v1('john.doe3@unse.edu.au', '123123', 'John', 'Doe')

#     registered_user_token = registered_user['token']

#     result = users_all_v1(registered_user_token)
#     expected = {}

#     assert result == expected

# def test_invlaid_token():
#     registered_user_token = 'HMMMMM'
    
#     with pytest.raises(InputError):
#         users_all_v1(registered_user_token)

# def test_valid_test(registered_user):

#     registered_user_token = registered_user['token']

#     result = users_all_v1(registered_user_token)
#     expected = {}

#     assert result == expected

# #################################
# #       user/profile/v1         #
# #################################

# def test_profile_user_not_found():
#     pass
# def test_profile_invalid_token():
#     pass
# def test_profile_valid_test():
#     pass

# #################################
# #    user/profile/setname/v1    #
# #################################

# def test_setname_name_first_too_short():
#     pass
# def test_setname_name_last_too_short():
#     pass
# def test_setname_name_first_too_long():
#     pass
# def test_setname_name_last_too_long():
#     pass

# # Assumption we have:
# def test_setname_alphanumeric():
#     pass

# def test_setname_invlid_token():
#     pass
# def test_setname_valid_test():
#     pass


# #################################
# #     user/profile/setemail/    #
# #################################
# def test_setmail_email_not_valid():
#     pass
# def test_setmail_email_already_used():
#     pass
# def test_setmail_invlid_token():
#     pass
# def test_setmail_valid_test():
#     pass


# #################################
# #   user/profile/sethandle/v1   #
# #################################
# def test_sethandle_handle_too_short():
#     pass
# def test_sethandle_handle_too_long():
#     pass
# def test_sethandle_none_alphanumeric():
#     pass
# def test_sethandle_handle_already_used():
#     pass
# def test_sethandle_invlid_token():
#     pass
# def test_sethandle_valid_test():
#     pass

