import socket
import threading
from Modules.Hub import HubConfiguration
from Modules.Hub.Message import Message


class HubDataReceiver:

    encoding = 'ascii'
    _thread: [None, threading.Thread]
    socket: [socket.socket, None]
    configuration: HubConfiguration

    def __init__(self, configuration: [HubConfiguration, None] = None):
        self.configuration = configuration or HubConfiguration.EnvironmentHubConfiguration()

    def parse_message(self, data: bytearray):
        message = data.decode(HubDataReceiver.encoding)

        parts = message.split(chr(127))
        message = Message(parts[0], parts[1:])

        return message


