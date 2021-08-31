import sys

from config import DEBUG_MODE, EASYGIF_VERSION

if "-v" in sys.argv or "--version" in sys.argv:
    print(f"EasyGif {EASYGIF_VERSION}")
    quit()

if "-h" in sys.argv or "--help" in sys.argv:
    print()
    print("                EASYGIF SERVER HELP CENTER")
    print()
    print(f"EasyGif {EASYGIF_VERSION}")
    print(f"DEBUG_MODE: {DEBUG_MODE}")
    print("""
The main server for EasyGif.

Args:
    --clear-log                     Clears the 'easygif.log' file
    -h, --help                      Shows the EasyGif Server Help Center and exits
    -d, --debug                     Launches EasyGif Server in DEBUG_MODE (note: --debug enables a higher debug level)
    -v, --version                   Shows the Server version and exits
""")
    quit()


from __protected import DISCORD_BOT_TOKEN
from easygif import client
from utils.log import log

log("Running the Discord Bot")
client.run(DISCORD_BOT_TOKEN)
