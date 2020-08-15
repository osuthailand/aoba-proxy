from platform import system
import hashlib
from helpers import configHelper

hostname = configHelper.config("config.ini").config["server"]["host"]
username = configHelper.config("config.ini").config["server"]["username"]
password = configHelper.config("config.ini").config["server"]["password"]
certificate = configHelper.config("config.ini").config["server"]["certificate"]
password_hashed = hashlib.md5(str(password).encode('utf-8')).hexdigest() # Hashed Password

conf = None

verbose = False
if "win" in system().lower(): #works for Win7, 8, 10 ...
	win = True
else:
	win = False