from .HubClient import HubClient
from . import Message
from pymongo import MongoClient
import os
import datetime


class LoggingHubClient(HubClient):

    def __init__(self, configuration=None):
        self.client = MongoClient("mongodb://localhost")
        self.db = self.client['Hub']
        self.collection = self.db['Messages']
        self.pid = os.getpid()

        HubClient.__init__(self, configuration)
        self.add_handler(typeName=None, handler=self.log)

    def log(self, message: Message):
        log_obj = {
            'Time': datetime.datetime.now(),
            'Direction': 'In',
            'Type': message.typeName,
            'Args': message.args,
            'PID': self.pid
        }

        self.collection.insert_one(log_obj)
