import psycopg2
import redis
import json
import os
from bottle import Bottle, request

class Sender(Bottle):
    def __init__(self):
        super().__init__()
        self.route('/', method='POST', callback=self.send)
        self.queue = redis.StrictRedis(host='redis', port=6379, db=0)

        db_host = os.getenv('DB_HOST', 'database')
        db_user = os.getenv('DB_USER', 'postgres')
        db_name = os.getenv('DB_NAME', 'email_sender')
        dsn = f'dbname={db_name} user={db_user} host={db_host}'
        self.connection = psycopg2.connect(dsn)

    def register_message(self, subject, message):
        sql = 'INSERT INTO emails (subject, message) VALUES (%s, %s)'
        cursor = self.connection.cursor()
        cursor.execute(sql, (subject, message))
        self.connection.commit()
        cursor.close()

        msg = {'subject': subject, 'message': message}
        self.queue.rpush('sender', json.dumps(msg))

        print('Message registered!')


    def send(self):
        subject = request.forms.get('subject')
        message = request.forms.get('message')

        self.register_message(subject, message)

        return 'Message receiveid! Subject: {} Message: {}'.format(subject, message)

sender = Sender()
sender.run(host='0.0.0.0', port=8000)