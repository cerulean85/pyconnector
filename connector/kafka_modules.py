import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import yaml
from kafka import KafkaProducer, KafkaConsumer

def get_consumer(topic_name, action):
    with open(f'earth-compose.yml') as f:
        compose = yaml.load(f, Loader=yaml.FullLoader)
        compose = compose['kafka']
        address, port = compose['address'], compose['port']

    consumer = KafkaConsumer(topic_name, bootstrap_servers=[f"{address}:{port}"],
                         auto_offset_reset='earliest', # 가장 처음부터 소비
                         enable_auto_commit=True,
                        #  group_id=str_group_name,
                         value_deserializer=action,                       
                        #  consumer_timeout_ms=60000 # 타임아웃지정(단위:밀리초)
                        )
    return consumer

def get_producer(action):
    with open(f'earth-compose.yml') as f:
        compose = yaml.load(f, Loader=yaml.FullLoader)
        compose = compose['kafka']
        address, port = compose['address'], compose['port']

    producer = KafkaProducer(
        acks=0,
        compression_type='gzip',
        bootstrap_servers=[f"{address}:{port}"],
        value_serializer=action)
    
    return producer