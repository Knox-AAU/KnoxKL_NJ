from environment.EnvironmentConstants import EnvironmentVariables as ev
from rest.DataRequest import sendTripleToDb
import pytest
import requests

xfail = pytest.mark.xfail

content: str = 'This content is for testing'
test_endpoint: str = 'http://127.0.0.1:54321/update'

class Test:

    def test_no_connection(self):
        retval = sendTripleToDb(content, endpoint=test_endpoint)

        assert retval.__eq__(False)