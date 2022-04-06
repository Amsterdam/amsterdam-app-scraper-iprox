import socket
import time
from GenericFunctions.Logger import Logger


class IsReachable:
    def __init__(self, backend_host='api_server', backend_port=8000):
        self.backend_host = backend_host
        self.backend_port = backend_port
        self.logger = Logger()
        self.timeout = 60

    def check(self):
        once = True
        for i in range(self.timeout):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(1)
                    s.connect((self.backend_host, self.backend_port))
                print('{host}:{port} is reachable'.format(host=self.backend_host, port=self.backend_port))
                return True
            except Exception as error:
                if once is True:
                    self.logger.error(error)
                    once = False
                time.sleep(1)
        print('{host}:{port} is unreachable'.format(host=self.backend_host, port=self.backend_port))
        return False
