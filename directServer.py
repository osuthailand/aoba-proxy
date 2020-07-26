from http.server import BaseHTTPRequestHandler,HTTPServer
import argparse, os, random, sys, requests

import hashlib

hostname = '163.172.255.98' #Gatari IP
username = 'Unknown' #Gatari Username
password = 'apekiller39' #Gatari Password
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

            url = 'https://{}{}?u={}&h={}&vv=2'.format(hostname, self.path, username, password_hashed)
            req_header = self.parse_headers()

            print(req_header)
            print(url)
            resp = requests.get(url, headers=merge_two_dicts(req_header, set_header()), verify=False)
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
            url = 'https://{}{}?u={}&h={}&vv=2'.format(hostname, self.path, username, password_hashed)
            content_len = int(self.headers.getheader('content-length', 0))
            post_body = self.rfile.read(content_len)
            req_header = self.parse_headers()

            resp = requests.post(url, data=post_body, headers=merge_two_dicts(req_header, set_header()), verify=False)
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
    parser.add_argument('--port', dest='port', type=int, default=32767,
                        help='serve HTTP requests on specified port (default: random)')
    parser.add_argument('--hostname', dest='hostname', type=str, default='163.172.255.98',
                        help='hostname to be processd (default: 163.172.255.98)')
    args = parser.parse_args(argv)
    return args

def main(argv=sys.argv[1:]):
        global hostname
        args = parse_args(argv)
        hostname = args.hostname
        print('aoba-mirror-server {} port {}...'.format(args.hostname, args.port))
        server_address = ('127.0.0.1', args.port)
        httpd = HTTPServer(server_address, ProxyHTTPRequestHandler)
        print('running on gatari proxy owo')
        httpd.timeout = 30
        httpd.serve_forever()

#if __name__ == '__main__':
main()
