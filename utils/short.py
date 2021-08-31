import json
from utils.log import log
from requests import post
from __protected import REBRANDLY_API_KEY

HEADERS = {"Content-type": "application/json", "apikey": REBRANDLY_API_KEY}

def create_short_url(url: str):
    """Creates a short URL from the given URL"""
    log("Creating a short link for {url}".format(url=url))
    body = {"destination": str(url), "title": "EasyGif - Redirecting you to the orginal GIF"}
    shorten_link_request = post("https://api.rebrandly.com/v1/links", data=json.dumps(body), headers=HEADERS)

    result = 'https://' + json.loads(shorten_link_request.text)['shortUrl']
    log("Short Link Result: {result}".format(result=result))
    return result