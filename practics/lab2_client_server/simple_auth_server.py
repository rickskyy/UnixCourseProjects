import time
from http.server import HTTPServer
from http.server import SimpleHTTPRequestHandler
from http.server import test as test_server
import sys
import base64

key = ""
BLOCK_TIME = 20
LIMIT_INCORRECT_ATTEMPTS = 3


class AuthHandler(SimpleHTTPRequestHandler):
    """ Main class to present webpages and authentication. """

    ip_dict = {}

    def reset_login_history(self, ip):
        self.ip_dict[ip] = [0, None]

    def handle_ip(self, ip):
        """
        Remember clients auth tries and save address with number of incorrect attempts
        ip_dict = {'<ip>': [<number_of_invalid_attempts>, <time_of_3rd_incorrect_attempt>]}
        :param ip: client ip address
        :return: False if ip is blocked, True if not
        """
        if ip in self.ip_dict:
            if self.ip_dict[ip][1] and time.time() - self.ip_dict[ip][1] < BLOCK_TIME:
                return False
            elif self.ip_dict[ip][1] and time.time() - self.ip_dict[ip][1] > BLOCK_TIME:
                self.ip_dict[ip][1] = None
            elif self.ip_dict[ip][0] == LIMIT_INCORRECT_ATTEMPTS - 1:
                self.ip_dict[ip][0] = 1
                self.ip_dict[ip][1] = time.time()
                return False
            else:
                self.ip_dict[ip][0] += 1
        else:
            self.ip_dict[ip] = [1, None]

        return True

    def do_HEAD(self):
        print("send header")
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_AUTHHEAD(self):
        print("send header")
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Test\"')
        self.send_header('Content-type', 'application/octet-stream')
        self.end_headers()

    def do_GET(self):
        global key
        ''' Present frontpage with user authentication. '''
        print("headers:" + self.headers['Authorization'])

        if 'Authorization' not in self.headers:
            self.do_AUTHHEAD()
            self.wfile.write(base64.b64decode('No auth header received'))
        elif self.headers['Authorization'] == 'Basic ' + key.decode():
            self.reset_login_history(self.address_string())
            SimpleHTTPRequestHandler.do_GET(self)
        elif self.handle_ip(self.address_string()):
            self.do_AUTHHEAD()
            self.wfile.write(base64.b64encode('Not authenticated. Login or password are incorrect'.encode()))


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("usage: simple_auth_server.py [port] [username:password]")
        sys.exit()
    key = base64.b64encode(sys.argv[2].encode())
    test_server(HandlerClass=AuthHandler, ServerClass=HTTPServer)
