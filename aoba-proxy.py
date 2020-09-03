import argparse
import sys

from constants import bcolors

from handlers import proxyHTTPRequestHandler

from helpers import configHelper
from helpers import consoleHelper
from helpers import generalHelper

from objects import glob

from http.server import HTTPServer

glob.conf = configHelper.config("config.ini")
glob.verbose = generalHelper.stringToBool(glob.conf.config["console"]["verbose"])

if glob.conf.default:
	# We have generated a default config.ini, quit server
	consoleHelper.printWarning()
	consoleHelper.printColored("[!] config.ini not found. A default one has been generated.", bcolors.YELLOW)
	consoleHelper.printColored("[!] Please edit your config.ini and run the server again.", bcolors.YELLOW)
	sys.exit()

if not glob.conf.checkConfig():
	consoleHelper.printError()
	consoleHelper.printColored("[!] Invalid config.ini. Please configure it properly", bcolors.RED)
	consoleHelper.printColored("[!] Delete your config.ini to generate a default one", bcolors.RED)
	sys.exit()

def parse_args(argv=sys.argv[1:]):
	parser = argparse.ArgumentParser(description='Aoba Proxy Server')
	parser.add_argument('--port', dest='port', type=int, default=32767,
						help='serve HTTP requests on specified port (default: 32767)')
	args = parser.parse_args(argv)
	return args

def main(argv=sys.argv[1:]):
	args = parse_args(argv)
	hostname = configHelper.config("config.ini").config["server"]["host"]
	consoleHelper.printServerStartHeader(True)
	consoleHelper.printColored("{}Proxying {} and hosting on 127.0.0.1:{}...".format(bcolors.UNDERLINE, hostname, args.port), bcolors.GREEN)
	if glob.verbose:
		consoleHelper.printColored("WARNING! VERBOSE MODE IS ON!", bcolors.YELLOW)
	server_address = ('127.0.0.1', args.port)
	httpd = HTTPServer(server_address, proxyHTTPRequestHandler.ProxyHTTPRequestHandler)
	httpd.timeout = 30
	httpd.serve_forever()

if __name__ == '__main__':
	main()
