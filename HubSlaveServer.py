from .HubClient import HubClient
from . import HubConfiguration
from . import Message
from .HubServer import HubServer


class HubSlaveServer():

    server: HubServer
    client: HubClient

    def __init__(self, master_configuration, slave_configuration=None):
        self.client = HubClient(master_configuration)
        self.server = HubServer(slave_configuration)

        self.client.add_handler(typeName=None, handler=self.send)

    def send(self, message: Message):
        data = message.to_bytes(self.server.encoding)
        for connection in self.server.connections:
            connection[0].sendall(data)

    def start(self):
        self.client.start()
        self.server.start()

    def __enter__(self):
        self.client.start()
        self.server.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.stop()
        self.server.stop()
        return exc_type is not None
