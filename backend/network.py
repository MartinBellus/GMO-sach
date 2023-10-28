import requests
from utility.constants import HTTP_URL
from utility.exceptions import NetworkException, RemoteFileNotFound
import time

POST_ATTEMPTS = 5

QUERY_ATTEMPTS = 5

TIMEOUT = 1


class NetworkQuery:
    def __init__(self, subaddres: str, type: str, filename: str, payload: str=None):
        if subaddres[-1] != "/":
            subaddres += "/"
        self.subaddres = subaddres
        self.type = type
        assert type == "GET" or type == "POST", "invalid http request type"
        self.filename = filename
        self.payload = payload

    def do_query(self) -> (bool, str):
        if self.type == "POST":
            return self.do_post()
        elif self.type == "GET":
            return self.do_get()
    
    def get_path(self):
        return HTTP_URL+self.subaddres+self.filename

    def do_post(self) -> (bool, str):
        for i in range(POST_ATTEMPTS):
            try:
                response = requests.post(
                    self.get_path(), self.payload, timeout=TIMEOUT)
                if response.status_code == 200:
                    return (True, response.raw)
                else:
                    raise NetworkException
            except requests.exceptions.Timeout:
                pass
            time.sleep(0.1 * 2**i)

        raise NetworkException

    def do_get(self) -> (bool, str):
        for i in range(QUERY_ATTEMPTS):
            try:
                response = requests.get(self.get_path(), timeout=TIMEOUT)
                if response.status_code==200:
                    return (True, response.text)
                elif response.status_code==404:
                    raise RemoteFileNotFound
                else:
                    raise NetworkException
            except requests.exceptions.Timeout:
                pass
            time.sleep(0.1 * 2**i)

        raise NetworkException