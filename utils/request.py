import json
from time import time

from config import REQUEST_CACHE_TTL
from requests import request as _http_request

from utils.exceptions import RequestError
from utils.log import log

# SCHEMA: RESPONSE_CACHE
# {
#   "<method><url>": {
#       "t": "the timestamp",
#       "d": "the data"
#   }
# }
#
RESPONSE_CACHE = {}


class Request():
    def __init__(self, url: str, method: str = "GET", cache: bool = True) -> None:
        self.url = str(url)
        self.method = str(method).upper()
        self.cache = bool(cache)
        self._cache_key = self.method + self.url
        if self.cache and self._cache_key in RESPONSE_CACHE:
            if time() - RESPONSE_CACHE[self._cache_key]["t"] <= REQUEST_CACHE_TTL:
                log("Request found in cache")
                self._response = str(RESPONSE_CACHE[self._cache_key]["d"])
            else:
                log("Request found in cache but expired")
                RESPONSE_CACHE.pop(self._cache_key, None)
                self._response = None
        else:
            self._response = None

    def _verify_response(self):
        if self._response is None:
            try:
                log("Requesting {method} {url}".format(
                    method=self.method, url=self.url))
                response = _http_request(
                    method=self.method, url=self.url)
                if response.status_code >= 400:
                    message = "{method} {url} returned HTTP {code}".format(
                        method=self.method, url=self.url, code=response.status_code)
                    raise RequestError(message)
                if self.cache:
                    RESPONSE_CACHE[self._cache_key] = {
                        "t": time(),
                        "d": response.text
                    }
                self._response = str(response.text)
            except Exception:
                message = "An error occured while requesting {method} {url}".format(
                    method=self.method, url=self.url)
                raise RequestError(message)

    @property
    def json(self):
        self._verify_response()
        try:
            return json.loads(self.text)
        except Exception:
            message = "{method} {url} did not return a JSON-encoded response".format(
                method=self.method, url=self.url)
            raise RequestError(message)

    @property
    def text(self):
        self._verify_response()
        try:
            return self._response
        except Exception:
            message = "We could not retrieve the text from the response by {method} {url}".format(
                method=self.method, url=self.url)
            raise RequestError(message)
