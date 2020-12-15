from os import error
from environment.EnvironmentConstants import EnvironmentVariables as ev
from rest.DataRequest import send_json_data_to_db
import pytest
import requests

xfail = pytest.mark.xfail

content: str = 'This content is for testing'
test_endpoint: str = 'http://127.0.0.1:54321/update'

class Test:
    @xfail(strict=True, raises=EnvironmentError)
    def test_environment_error_is_thrown(self):
        retval = send_json_data_to_db(content, endpoint_name=test_endpoint)

        assert retval.__eq__(False)