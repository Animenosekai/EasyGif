import json
from requests import post
from __protected import REBRANDLY_API_KEY

HEADERS = {"Content-type": "application/json", "apikey": REBRANDLY_API_KEY}

def create_short_url(url: str):
    """Creates a short URL from the given URL"""
    body = {"destination": str(url), "title": "EasyGif - Redirecting you to the orginal GIF"}
    shorten_link_request = post("https://api.rebrandly.com/v1/links", data=json.dumps(body), headers=HEADERS)

    return 'https://' + json.loads(shorten_link_request.text)['shortUrl']