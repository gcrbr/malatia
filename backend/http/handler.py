import http.server
import glob
import os

class mHandler(http.server.SimpleHTTPRequestHandler):
    slash = '\\' if os.name == 'nt' else '/'
    main_path = slash.join(__file__.split('/')[:-3])
    http_path = main_path + slash + 'interface'
    allowed = []
    def log_message(self, format, *args):
        pass

    def get_allowed_paths(self):
        if not self.allowed:
            for path in glob.glob(self.http_path + self.slash + '**', recursive=True):
                self.allowed.append(path[len(self.http_path):])
        return self.allowed

    def translate_path(self, path: str) -> str:
        if path in self.get_allowed_paths():
            return self.http_path + path
        if path == self.slash + 'data.json':
            return self.main_path + self.slash + 'data.json'
        return ''