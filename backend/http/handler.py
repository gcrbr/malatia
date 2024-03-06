import http.server

class mHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def translate_path(self, path: str) -> str:
        if path.lower() in ['/', '/index.html', '/data.json', '/map.html'] or path.lower().startswith('/assets/'):
            return super().translate_path(path)
        return ''