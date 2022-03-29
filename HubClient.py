import socket
from . import Message
import threading
from .HubDataReceiver import HubDataReceiver
from .InvalidStateException import InvalidStateException


class HubClient(HubDataReceiver):

    _thread: [None, threading.Thread]
    socket: [socket.socket, None]

    def __init__(self, configuration=None):
        HubDataReceiver.__init__(self, configuration)

        self.handlers = []
        self.socket = None
        self.running = False
        self.data = bytearray()
        self._thread = None

    def add_handler(self, typeName: [str, None], handler :(lambda message: None)):
        self.handlers.append((typeName, handler))

    def send(self, message: Message):
        if self.socket is None or not self.running:
            raise InvalidStateException(f'Cannot send a message as this hub is not connected')

        data = message.to_bytes(HubDataReceiver.encoding)

        self.socket.send(data)

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
                message = self.parse_message(self.data)
                self.data = bytearray()

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
