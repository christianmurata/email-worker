import redis
import json
import os
from time import sleep
from random import randint

redis_host = os.getenv('REDIS_HOST', 'redis')
redis_port = os.getenv('REDIS_PORT', 6379)
redis_db = os.getenv('REDIS_DB', 0)

queue = redis.Redis(host=redis_host, port=redis_port, db=redis_db)

print('Wainting messages...')

while True:
    message = json.loads(queue.blpop('sender')[1])

    print('Sending message...:', message['subject'])
    sleep(randint(15,45))
    print('Message sent...:', message['message'])