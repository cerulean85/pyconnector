import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import yaml
from connector.MySQLPoolConnector import MySQLPoolConnector, execute
class EarthlingDBPool(MySQLPoolConnector):
    def __init__(self):
        self.getDBOption()
        if not EarthlingDBPool._instance:
            self.pool = self.getPool()
            self.pool.init()

    @classmethod
    def getInstance(cls):
        if not cls._instance:
            cls._instance = EarthlingDBPool()
        return cls._instance


def exec(query):
    return execute(query, EarthlingDBPool)