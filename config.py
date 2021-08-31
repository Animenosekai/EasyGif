import sys

from __protected import GIPHY_API_KEY, TENOR_API_KEY

# Information
EASYGIF_VERSION = "2.0 (Beta)"
COMMAND_PREFIX = "."

# Emoji Reaction
ROGER_REACTION = "<:easygif_roger:712005159676411914>"

# Tenor Random
RANDOM_DICTIONARY = ["anime", "japan", "manga",
                     "tech", "technology", "coding", "music"]

# Request
REQUEST_CACHE_TTL = 3600
GIPHY_SEARCH_ENDPOINT = "http://api.giphy.com/v1/gifs/search?q={query}&api_key=" + \
    GIPHY_API_KEY + "&limit=100"
GIPHY_RANDOM_ENDPOINT = "https://api.giphy.com/v1/gifs/random?&api_key=" + GIPHY_API_KEY
TENOR_SEARCH_ENDPOINT = "https://g.tenor.com/v1/search?q={query}&key=" + \
    TENOR_API_KEY + "&limit=50"
TENOR_RANDOM_ENDPOINT = "https://g.tenor.com/v1/random?q={query}&key=" + \
    TENOR_API_KEY + "&limit=50"

SFW_GIPHY_SEARCH_ENDPOINT = "http://api.giphy.com/v1/gifs/search?q={query}&api_key=" + \
    GIPHY_API_KEY + "&limit=100&rating=pg13"
SFW_GIPHY_RANDOM_ENDPOINT = "https://api.giphy.com/v1/gifs/random?rating=pg13&api_key=" + GIPHY_API_KEY
SFW_TENOR_SEARCH_ENDPOINT = "https://g.tenor.com/v1/search?q={query}&key=" + \
    TENOR_API_KEY + "&limit=50&contentfilter=low"
SFW_TENOR_RANDOM_ENDPOINT = "https://g.tenor.com/v1/random?q={query}&key=" + \
    TENOR_API_KEY + "&limit=50&contentfilter=low"

# Assets
ASSETS_DOMAIN = "https://easygif-assets.netlify.app"

# Parameters
DEBUG_MODE = "-d" in sys.argv or "--debug" in sys.argv
