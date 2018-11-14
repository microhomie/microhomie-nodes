import urequests

from homie.node import HomieNode


class HTTP(HomieNode):
    def __init__(
        self, url, headers={}, method="GET", name="HTTP request", interval=60
    ):
        super().__init__(name=name, interval=interval)
        self.node_id = b"http"
        self.url = url
        self.headers = headers
        self.method = method
        self.response = ""

    def __repr__(self):
        return (
            "HTTP(url={!r}, headers={!r}, method={!r}, name={!r}, "
            "interval={!r})".format(
                self.url, self.headers, self.method, self.name, self.interval
            )
        )

    def __str__(self):
        return "HTTP: url = {}".format(self.url)

    def get_properties(self):
        yield (b"http/$name", self.name)
        yield (b"http/$type", b"http")
        yield (b"http/$properties", b"response")

    def update_data(self):
        self.response = urequests.request(
            self.method, self.url, headers=self.headers
        )

    def get_data(self):
        yield (b"http/response", self.response.text)
