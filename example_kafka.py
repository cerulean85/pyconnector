import time, pickle, json
from multiprocessing import Process, Value, Queue
from handler.earthling_mq import *
def consume_action(message):
    try:
        return json.loads(message.decode('utf-8'))
    except:
        return message.decode('utf-8')


def consume():
    consumer = get_consumer("result", consume_action)
    for message in consumer:
        try:
            # result = message.decode('utf-8')
            # option = json.loads(result)
            message = message.value
            # log.debug(type(message))

            task_no = message["task_no"]
            user_id = message["user_id"]
            log.debug(f"({user_id})의 task-[{task_no}]를 처리 중입니다.")
            # log.debug(user_id)

            filePath = f"/data/model/connect/{user_id}.pickle"
            with open(filePath, 'wb') as fw:
                pickle.dump(message, fw)

            update_state_to_finish(task_no)
            log.debug(f"({user_id})의 task-[{task_no}]를 완료하였습니다.")

        except Exception as err:
            log.debug(err)
            log.debug("Passed")
def produce_action(message):
    try:
        return json.dumps(message, ensure_ascii=False)
    except:
        return message.decode('utf-8')
def produce(message):
    producer = get_producer(produce_action)
    producer.send("result", value=message)
    producer.flush()