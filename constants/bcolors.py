"""Console colors"""
from platform import system
if "win" in system().lower(): #works for Win7, 8, 10 ...
    from ctypes import windll
    k=windll.kernel32
    k.SetConsoleMode(k.GetStdHandle(-11),7)

PINK 		= '\033[95m'
BLUE 		= '\033[94m'
GREEN 		= '\033[92m'
YELLOW 		= '\033[93m'
RED 		= '\033[91m'
ENDC 		= '\033[0m'
BOLD 		= '\033[1m'
UNDERLINE 	= '\033[4m'
