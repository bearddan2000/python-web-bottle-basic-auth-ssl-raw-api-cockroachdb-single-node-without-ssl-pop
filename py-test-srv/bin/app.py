import requests
from requests.auth import HTTPBasicAuth
import testify

from const import *

def fun_call(url: str, fun, auth: HTTPBasicAuth = None):
    # Additional headers.
    headers = {'Content-Type': 'application/json' } 

    if auth is not None:
        return fun(url, headers=headers, auth=auth, verify=False)
    else:
        return fun(url, headers=headers, verify=False)
    
def get_count(url: str, fun_ptr):
    
    resp = fun_call(url, fun_ptr, HTTPBasicAuth('user', 'pass'))

    return len(resp.json()['results'])

def assert_not_equal_count(url: str, fun_ptr):
    """assert that there has been something added or removed"""
    before = get_count(GET_ALL_URL, requests.get)
    after = get_count(url, fun_ptr)
    testify.assert_not_equal(before, after)
    
    return 0

def assert_equal_count(url: str, fun_ptr):
    """assert that nothing has been added or removed"""
    before = get_count(GET_ALL_URL, requests.get)
    after = get_count(url, fun_ptr)
    testify.assert_equal(before, after)
    
    return 0

def assert_changed(index: int):
    key = 'results'
    resp = fun_call(GET_ALL_URL, requests.get, HTTPBasicAuth('user', 'pass')).json()
    testify.assert_not_equal(STATIC[key][index], resp[key][index])
    return 0

def assert_url(url: str, fun_ptr, code: int = 200, auth: HTTPBasicAuth = None):
    """assert that endpoint is valid"""
    
    resp = fun_call(url, fun_ptr, auth)

    testify.assert_equal(resp.status_code, code)

    return 0

class TestGet(testify.TestCase):
    """docstring for TestGet."""

    def test_auth_get_all_url(self):
        return assert_url(GET_ALL_URL, requests.get, auth=HTTPBasicAuth('user', 'pass'))
    
    def test_unauth_get_all_url(self):
        return assert_url(GET_ALL_URL, requests.get, code=401)
    
    def test_get_all_equal_output(self):
        return assert_equal_count(GET_ALL_URL, requests.get)

if __name__ == '__main__':
    testify.run()
