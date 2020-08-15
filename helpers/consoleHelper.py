from constants import bcolors

def printServerStartHeader(asciiArt=True):
	"""
	Print server start message
	:return:
	"""
	if asciiArt:
		print("{}                                                                             ".format(bcolors.GREEN))
		print("    ___            __                     ____                                 ")
		print("   /   |  ____    / /_   ____ _          / __ \\   _____  ____    _  __   __  __")
		print("  / /| | / __ \\  / __ \\ / __ `/         / /_/ /  / ___/ / __ \\  | |/_/  / / / /")
		print(" / ___ |/ /_/ / / /_/ // /_/ /         / ____/  / /    / /_/ / _>  <   / /_/ / ")
		print("/_/  |_|\\____/ /_.___/ \\__,_/         /_/      /_/     \\____/ /_/|_|   \\__, /  ")
		print("                                                                      /____/   ")
		print("                                                                             {}".format(bcolors.ENDC))

	printColored("> Welcome to Aoba Proxy", bcolors.GREEN)
	printColored("> Press CTRL+C to exit\n", bcolors.GREEN)

def printNoNl(string):
	"""
	Print a string without \n at the end

	:param string: string to print
	:return:
	"""
	print(string, end="")

def printColored(string, color):
	"""
	Print a colored string

	:param string: string to print
	:param color: ANSI color code
	:return:
	"""
	print("{}{}{}".format(color, string, bcolors.ENDC))

def printError():
	"""
	Print a red "Error"

	:return:
	"""
	printColored("Error", bcolors.RED)

def printDone():
	"""
	Print a green "Done"

	:return:
	"""
	printColored("Done", bcolors.GREEN)

def printWarning():
	"""
	Print a yellow "Warning"

	:return:
	"""
	printColored("Warning", bcolors.YELLOW)
