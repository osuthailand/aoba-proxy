import requests

from helpers import generalHelper

from objects import glob

from http.server import BaseHTTPRequestHandler,HTTPServer
from urllib.parse import urlencode, urljoin, urlparse, urlunparse, parse_qs
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning) # I have got enough bullshit

class ProxyHTTPRequestHandler(BaseHTTPRequestHandler):
	protocol_version = 'HTTP/1.0'
	def do_HEAD(self):
		self.do_GET(body=False)
		return
		
	def do_GET(self, body=True):
		sent = False
		try:
			initialising_url = 'https://{}{}'.format(glob.hostname, self.path)
			parsed_url = urlparse(initialising_url)
			if parse_qs(parsed_url.query) != []:
				query_hack = parse_qs(parsed_url.query)
				query_hack["u"] = [glob.username]
				query_hack["h"] = [glob.password_hashed]
			final_url = urljoin(initialising_url, urlparse(initialising_url).path)
			if parse_qs(parsed_url.query) != []:
				url = final_url + "?" + urlencode(query_hack, doseq=True)
			else:
				url = final_url
			req_header = self.parse_headers()
			if glob.verbose:
				print(req_header)
				print(url)
			if glob.certificate == "":
				resp = requests.get(url, headers=generalHelper.merge_two_dicts(req_header, generalHelper.set_header()), verify=False)
			else:
				resp = requests.get(url, headers=generalHelper.merge_two_dicts(req_header, generalHelper.set_header()), verify=certificate)
			sent = True

			self.send_response(resp.status_code)
			self.send_resp_headers(resp)
			data = resp.content
			if body:
				self.wfile.write(data)
			return
		finally:
			if not sent:
				self.send_error(404, 'error trying to proxy')

	def do_POST(self, body=True):
		sent = False
		try:
			initialising_url = 'https://{}{}'.format(glob.hostname, self.path)
			parsed_url = urlparse(initialising_url)
			query_hack = parse_qs(parsed_url.query)
			query_hack["u"] = [glob.username]
			query_hack["h"] = [glob.password_hashed]
			final_url = urljoin(initialising_url, urlparse(initialising_url).path)
			url = final_url + "?" + urlencode(query_hack, doseq=True)
			content_len = int(self.headers.getheader('content-length', 0))
			post_body = self.rfile.read(content_len)
			req_header = self.parse_headers()

			if glob.certificate == "":
				resp = requests.post(url, data=post_body, headers=merge_two_dicts(req_header, generalHelper.set_header()), verify=False)
			else:
				resp = requests.post(url, data=post_body, headers=merge_two_dicts(req_header, generalHelper.set_header()), verify=certificate)
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
		if glob.verbose:
			print ('Response Header')
		for key in respheaders:
			if key not in ['Content-Encoding', 'Transfer-Encoding', 'content-encoding', 'transfer-encoding', 'content-length', 'Content-Length']:
				if glob.verbose:
					print (key, respheaders[key])
				self.send_header(key, respheaders[key])
		self.send_header('Content-Length', len(resp.content))
		self.end_headers()