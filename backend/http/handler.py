import http.server

class mHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass