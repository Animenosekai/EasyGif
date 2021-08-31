from urllib.parse import quote

def url_encode(text: str):
    return quote(str(text), safe='')