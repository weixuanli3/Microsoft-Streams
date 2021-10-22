import pytest
import requests
import json
from src.error import InputError
from src.request_helper_functions import *
from src.config import url


def test_echo():
    assert echo_req("1") == "1"
    assert echo_req("abc") == "abc"
    assert echo_req("trump") == "trump"


def test_echo_except():
    assert echo_req("echo")['code'] == InputError.code
