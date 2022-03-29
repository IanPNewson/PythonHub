import sys
from threading import Thread
import socket
from typing import List, Any

from .HubClient import HubClient
from . import HubConfiguration


class HubSlaveServer(HubClient):

    connections: list[socket]
    slaveConfiguration: HubConfiguration
    _thread: [None, Thread]
    running: bool
    sock: socket

    def __init__(self, slaveConfiguration, masterConfiguration=None):
        HubClient.__init__(self, masterConfiguration)

        self.slaveConfiguration = slaveConfiguration
        self._thread = None
        self.running = False
        self.connections = []

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(self.slaveConfiguration.hostPort())

    def start(self):
        HubClient.start(self)
        self.start_listening()

    def start_listening(self):
        self.running = True

        self._thread = Thread(target=self.__loop__)
        self._thread.start()

    def __loop__(self):
        self.sock.listen(1)

        while True:
            # Wait for a connection
            print('waiting for a connection')
            connection, client_address = self.sock.accept()

    def stop(self):
        self.running = False
        self._thread.join(timeout=10)
        self._thread = None