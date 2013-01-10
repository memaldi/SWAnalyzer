from django.core.validators import URLValidator
from urlparse import urlparse
import httplib
import json

url_val = URLValidator(verify_exists=False)

class CKAN:

    def __init__(self, host):
        try: 
            url_val(host)
        except:
            print host +  ' is an invalid URL!'
            exit(0)
        self.host = urlparse(host)
        self.http_connection = httplib.HTTPConnection(self.host.netloc)

    def close(self):
        self.http_connection.close()

    def get_datasets_from_group(self, group):
        self.http_connection.request('GET', '/api/rest/group/' + group)
        response = self.http_connection.getresponse()
        data = response.read()
        json_data = json.loads(data)
        return json_data['packages']
