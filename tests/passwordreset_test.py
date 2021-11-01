# '''Contains tests for passwordreset function in auth.py'''

# import pytest

# from src.other import clear_v1
# from src.auth import auth_passwordreset_request_v1, auth_passwordreset_reset_v1
# from src.error import InputError

# @pytest.fixture
# def setup():
#     clear_v1()
#     return auth_register_v1("john.doe1@unsw.edu.au","password","John","Doe")

# #------------------------------------------------------------
# # This block of code deals with the auth_passwordreset_request_v1 function

# # nothing should happen when email is invalid or valid
# def test_request_email(setup):
#     assert auth_passwordreset_request_v1("john.doe1@unsw.edu.au") == {}
#     assert auth_passwordreset_request_v1("roy.lin@unsw.edu.au") == {}

# #------------------------------------------------------------
# # This block of code deals with the auth_password_reset_v1 function

# def test_reset_valid(setup):
#     reset_code = 
#     auth_passwordreset_reset_v1(reset_code, "newpassword")

# def test_reset_code_invalid():
#     clear_v1()
#     with pytest.raises(InputError):
#         auth_passwordreset_reset_v1(123832, "newpassword")

# def test_reset_password_invalid(setup):
#     reset_code = 
#     with pytest.raises(InputError):
#         auth_passwordreset_reset_v1(reset_code, "short")
