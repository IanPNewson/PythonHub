import socket
from . import HubConfiguration
from . import Message
import threading
from .InvalidStateException import InvalidStateException


class HubClient:

    _encoding = 'ascii'
    _thread: [None, threading.Thread]
    socket: [socket.socket, None]

    def __init__(self, configuration=None):
        self.configuration = configuration or HubConfiguration.EnvironmentHubConfiguration()
        self.handlers = []
        self.socket = None
        self.running = False
        self.data = bytearray()
        self._thread = None

    def add_handler(self, typeName: str, handler :(lambda message: None)):
        self.handlers.append((typeName, handler))

    def start(self):
        if self._thread is not None or self.running:
            raise InvalidStateException('Can\'t start this HubClient; it\'s already started')

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(self.configuration.hostPort())
        self.running = True

        self._thread = threading.Thread(target=self.__loop__)
        self._thread.start()

    def __loop__(self):
        while self.running:
            byte = self.socket.recv(1)
            if byte == b'\n':
                message = self.data.decode(encoding=HubClient._encoding)
                self.data = bytearray()

                parts = message.split(chr(127))
                message = Message.Message(parts[0], parts[1:])

                for handler in self.handlers:
                    if handler[0] == message.typeName or handler[0] is None:
                        handler[1](message)
            else:
                self.data += byte

    def stop(self):
        self.running = False
        self._thread.join(timeout=10)
        self._thread = None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        return exc_type is not None
