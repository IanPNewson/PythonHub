from Modules.Hub.LoggingHubClient import LoggingHubClient


hub = LoggingHubClient()

with hub:
    while input('Running, type exit to quit') != 'exit':
        pass

print('Done')
