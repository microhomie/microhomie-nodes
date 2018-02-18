from homie.node import HomieNode
from homie import Property, utils
import urequests

class HTTP(HomieNode):
    def __init__(self, url, headers={}, method='GET', interval=60):
        super().__init__(interval=interval)
        
        self.url = url
        self.headers = headers
        self.method = method
        self.response = ''

    def __str__(self):
        return 'HTTP: url = {}'.format(self.url)

    def get_node_id(self):
        return [b'http']

    def get_properties(self):
        return (
            Property(b'http/$properties', b'response', True),
            )

    def update_data(self):
        self.response = urequests.request(self.method, self.url, headers=self.headers)


    def get_data(self):
        return (
            Property(b'http/response', self.response.text, True),
        )
