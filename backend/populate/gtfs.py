import requests
import zipfile
import io

class GTFS:
    def __init__(self):
        self.data = {}
    
    def parse_csv(self, csv):
        content = []
        csv = csv.splitlines()
        format = csv[0].split(',')
        for line in csv[1:]:
            data = {}
            fields = line.split(',')
            for i in range(0, len(format)):
                data[format[i]] = fields[i]
            content.append(data)
        return content

    def import_from_buffer(self, buffer):
        zip = zipfile.ZipFile(buffer)
        for file in zip.namelist():
            name = file[:-4]
            content = zip.read(file).decode('utf-8')
            self.data[name] = self.parse_csv(content)

    def import_from_url(self, url):
        raw = requests.get(url).content
        self.import_from_buffer(io.BytesIO(raw))

    def get(self, key):
        return self.data[key]