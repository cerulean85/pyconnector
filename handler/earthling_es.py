import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from connector.ElasticSearchConnector import insert


def insert_list_to_es(data_list, index, doc_type, request_timeout = 30):
    insert(data_list, index, doc_type, request_timeout)