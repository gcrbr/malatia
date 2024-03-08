import http.server
import glob
import os

class mHandler(http.server.SimpleHTTPRequestHandler):
    http_path = 'interface'
    allowed = []
    def log_message(self, format, *args):
        pass

    def get_allowed_paths(self):
        if not self.allowed:
            for path in glob.glob('interface/**', recursive=True):
                self.allowed.append(path[len(self.http_path):])
        return self.allowed

    def get_cwd(self):
        return os.getcwd() + '/' + self.http_path

    def translate_path(self, path: str) -> str:
        if path in self.get_allowed_paths():
            return self.get_cwd() + path
        if path == '/data.json':
            return os.getcwd() + '/data.json'
        return ''