from Modules.Hub import HubSlaveServer
from Modules.Hub.HubConfiguration import *
from absl import app
from absl import flags

flags.DEFINE_string('master_host', default=None, required=True, help='Host name for the master server, likely on '
                                                                     'another machine')
flags.DEFINE_integer('master_port', default=None, required=True, help='Port for the master server, likely on '
                                                                      'another machine')
flags.DEFINE_string('slave_host', required=False, default=None, help='Host name for this server, if not provided '
                                                                     'comes from env HUB_HOST')
flags.DEFINE_integer('slave_port', required=False, default=None, help='Port for this server, if not provided comes '
                                                                      'from env HUB_PORT')


def main(args):
    master_config = HubConfiguration(flags.FLAGS.master_host, flags.FLAGS.master_port)

    slave_config = None
    slave_host = flags.FLAGS.slave_host
    slave_port = flags.FLAGS.slave_port

    if slave_host is not None and slave_port is not None:
        slave_config = HubConfiguration(slave_host, slave_port)
    else:
        slave_config = EnvironmentHubConfiguration()

    hub = HubSlaveServer.HubSlaveServer(slave_config, master_config)
    # hub.add_handler('StfcHubMessageTypes.ImagePostedMessage', lambda message: print(message))
    hub.add_handler(typeName=None, handler=lambda message: print(message))

    with hub:
        txt = None
        while txt != 'exit':
            txt = input('Type exit to stop')

    print('done')


if __name__ == '__main__':
    app.run(main)
