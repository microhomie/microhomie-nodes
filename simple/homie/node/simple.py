from homie.node import HomieNode


class SimpleHomieNode(HomieNode):
    def __init__(self, type, property, interval=60):
        super().__init__(name=type, interval=interval)
        self.node_id = type
        self.type = type
        self.property = property
        self.value = None

    def __repr__(self):
        return "SimpleHomieNode(type={!r}, property={!r}, interval={!r})".format(
            self.type, self.property, self.interval
        )

    def __str__(self):
        return "{}/{}: {}".format(
            self.type.decode(), self.property.decode(), self.value
        )

    def get_data(self):
        """returns the data value"""
        yield (b"{}/{}".format(self.type, self.property), self.value)

    def update_data(self):
        """nothing happens on update data"""
        pass

    def get_properties(self):
        """no special properties"""
        _type = self.type
        yield (_type + b"/$name", self.name)
        yield (_type + b"/$type", _type)
        yield (_type + b"/$properties", self.property)
