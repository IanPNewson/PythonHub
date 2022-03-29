import socket
from threading import Thread
from Modules.Hub import HubDataReceiver, HubConfiguration, Message


class HubServer(HubDataReceiver.HubDataReceiver):

    connections: list[socket]
    _thread: [None, Thread]
    running: bool
    sock: socket
    _buffers: dict

    def __init__(self, configuration: [HubConfiguration, None] = None):
        HubDataReceiver.HubDataReceiver.__init__(self, configuration)

        self._thread = None
        self.running = False
        self.connections = []
        self._buffers = {}

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(self.configuration.hostPort())

    def start(self):
        self.running = True

        self._thread = Thread(target=self.__loop__)
        self._thread.start()

    def __loop__(self):
        self.sock.listen(1)

        while True:
            # Wait for a connection
            print('waiting for a connection')
            connection, client_address = self.sock.accept()

            thr = Thread(target=lambda: self.__listener_loop__(connection, client_address))
            thr.start()

            self.connections.append((connection, client_address, thr))
            self._buffers[client_address] = bytearray()

    def __listener_loop__(self, skt: socket, client_address: str):
        while True:
            data = skt.recv(1)

            if data == Message.Message.TERMINATOR:
                pass
            else:
                self._buffers[client_address] += data

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
