from http.server import BaseHTTPRequestHandler,HTTPServer
import argparse, os, random, sys, requests

from socketserver import ThreadingMixIn
import threading

import hashlib
from urllib.parse import urljoin, urlparse, parse_qs
from helpers import configHelper

conf = configHelper.config("config.ini")
if conf.default:
	# We have generated a default config.ini, quit server
	print("[!] config.ini not found. A default one has been generated.")
	print("[!] Please edit your config.ini and run the server again.")
	sys.exit()

if not conf.checkConfig():
	print("[!] Invalid config.ini. Please configure it properly!")
	print("[!] Delete your config.ini to generate a default one.")
	sys.exit()
else:
	print("[/] Done!")

hostname = conf.config["server"]["host"] # Server IP
username = conf.config["server"]["username"] # Username
password = conf.config["server"]["password"] # Plain Password
certificate = conf.config["server"]["certificate"] # Cert Path
password_hashed = hashlib.md5(str(password).encode('utf-8')).hexdigest()

def merge_two_dicts(x, y):
	z = x.copy()
	z.update(y)
	return z

def set_header():
	headers = {
		'User-Agent': 'osu!',
		'Host': 'osu.ppy.sh',
		'Accept-Encoding': 'gzip, deflate'
	}

	return headers

class ProxyHTTPRequestHandler(BaseHTTPRequestHandler):
	protocol_version = 'HTTP/1.0'
	def do_HEAD(self):
		self.do_GET(body=False)
		return
		
	def do_GET(self, body=True):
		sent = False
		try:
			initialising_url = 'https://{}{}'.format(hostname, self.path)
			parsed_url = urlparse(initialising_url)
			get_query = parse_qs(parsed_url.query)
			#print(get_query)
			final_url = urljoin(initialising_url, urlparse(initialising_url).path)
			url = final_url + '?u={}&h={}&r={}&q={}&m={}&p={}'.format(username, password_hashed, get_query["r"][0], get_query["q"][0], get_query["m"][0], get_query["p"][0])
			req_header = self.parse_headers()

			print(req_header)
			print(url)
			if certificate == "":
				resp = requests.get(url, headers=merge_two_dicts(req_header, set_header()), verify=False)
			else:
				resp = requests.get(url, headers=merge_two_dicts(req_header, set_header()), verify=certificate)
			sent = True

			self.send_response(resp.status_code)
			self.send_resp_headers(resp)
			beatmap = resp.content
			if body:
				self.wfile.write(beatmap)
			return
		finally:
			if not sent:
				self.send_error(404, 'error trying to proxy')

	def do_POST(self, body=True):
		sent = False
		try:
			initialising_url = 'https://{}{}'.format(hostname, self.path)
			parsed_url = urlparse(initialising_url)
			get_query = parse_qs(parsed_url.query)
			#print(get_query)
			final_url = urljoin(initialising_url, urlparse(initialising_url).path)
			url = final_url + '?u={}&h={}&r={}&q={}&m={}&p={}'.format(username, password_hashed, get_query["r"][0], get_query["q"][0], get_query["m"][0], get_query["p"][0])
			content_len = int(self.headers.getheader('content-length', 0))
			post_body = self.rfile.read(content_len)
			req_header = self.parse_headers()

			if certificate == "":
				resp = requests.post(url, data=post_body, headers=merge_two_dicts(req_header, set_header()), verify=False)
			else:
				resp = requests.post(url, data=post_body, headers=merge_two_dicts(req_header, set_header()), verify=certificate)
			sent = True

			self.send_response(resp.status_code)
			self.send_resp_headers(resp)
			if body:
				self.wfile.write(resp.content)
			return
		finally:
			if not sent:
				self.send_error(404, 'error trying to proxy')

	def parse_headers(self):
		req_header = {}
		for line in self.headers:
			line_parts = [o.strip() for o in line.split(':', 1)]
			if len(line_parts) == 2:
				req_header[line_parts[0]] = line_parts[1]
		return req_header

	def send_resp_headers(self, resp):
		respheaders = resp.headers
		print ('Response Header')
		for key in respheaders:
			if key not in ['Content-Encoding', 'Transfer-Encoding', 'content-encoding', 'transfer-encoding', 'content-length', 'Content-Length']:
				print (key, respheaders[key])
				self.send_header(key, respheaders[key])
		self.send_header('Content-Length', len(resp.content))
		self.end_headers()

def parse_args(argv=sys.argv[1:]):
	parser = argparse.ArgumentParser(description='Aoba''s p100 storage server')
	parser.add_argument('--port', dest='port', type=int, default=32768,
						help='serve HTTP requests on specified port (default: random)')
	parser.add_argument('--hostname', dest='hostname', type=str, default='163.172.255.98',
						help='hostname to be processd (default: 163.172.255.98)')
	args = parser.parse_args(argv)
	return args

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
	pass

def main(argv=sys.argv[1:]):
		global hostname
		args = parse_args(argv)
		hostname = args.hostname
		print('aoba-mirror-server {} port {}...'.format(args.hostname, args.port))
		server_address = ('127.0.0.1', args.port)
		httpd = ThreadedHTTPServer(server_address, ProxyHTTPRequestHandler)
		#httpd = HTTPServer(server_address, ProxyHTTPRequestHandler)
		print('running on gatari proxy owo')
		httpd.timeout = 30
		httpd.serve_forever()

if __name__ == '__main__':
	main()