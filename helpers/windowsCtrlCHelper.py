import sys

def handler(a,b=None):
    sys.exit(1)
def install_handler():
    if sys.platform == "win32":
        import win32api
        win32api.SetConsoleCtrlHandler(handler, True)