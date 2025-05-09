import os, sys, yaml
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from elasticsearch import Elasticsearch
from elasticsearch import helpers

class ElasticSearchConnector:
    _instance = None
    es_address = 'localhost'
    es_port = 0
    conn = None

    def __init__(self):
        root_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = root_dir.split('/')
        if root_dir[len(root_dir) - 1] == 'handler':
            tmp = ''
            for i in range(0, len(root_dir) - 1):
                dir_str = root_dir[i]
                tmp = tmp + dir_str + '/'

        with open(f'earth-compose.yml') as f:
            es_option = yaml.load(f, Loader=yaml.FullLoader)
            es_option = es_option['es']
            self.es_address = es_option['address']
            self.es_port    = es_option['port']

        self.conn = Elasticsearch([{'host': self.es_address, 'port': self.es_port}])    


    def getConn(self):
        return self.conn


    @classmethod
    def getInstance(cls):
        if not cls._instance:
            cls._instance = ElasticSearchConnector()
        return cls._instance
    

def insert(data_list, index, doc_type, request_timeout = 30):
    conn = ElasticSearchConnector().getInstance().getConn()
    helpers.bulk(conn, data_list, index=index, doc_type=doc_type, request_timeout = 30)
