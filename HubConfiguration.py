import os


class HubConfiguration:

    host: [str, None]
    port: [int, None]

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def get_host(self):
        return self.host

    def get_port(self):
        return self.port

    def hostPort(self):
        return self.host, self.port


class EnvironmentHubConfiguration(HubConfiguration):

    def __init__(self, hostKeyName='HUB_HOST', portKeyName='HUB_PORT'):
        host = os.getenv(hostKeyName)
        port = int(os.getenv(portKeyName))

        HubConfiguration.__init__(self, host, port)
