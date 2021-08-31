from urllib.parse import quote
from utils.log import log

def url_encode(text: str):
    log("URL Encoding {text}".format(text=text))
    return quote(str(text), safe='')