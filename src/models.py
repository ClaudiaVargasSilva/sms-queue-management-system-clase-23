from flask_sqlalchemy import SQLAlchemy
import os
from twilio.rest import Client

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Queue:
    def __init__(self):
        self._queue = []
        # depending on the _mode, the queue has to behave like a FIFO or LIFO
        self._mode = 'FIFO'
        self.account_sid = 'AC16d82e4980d8849c4de8301871390da7'
        self.auth_token = '16dbb204abf831d6596242b4a37ea2ee'
        self.client = Client(self.account_sid, self.auth_token)


    def enqueue(self, user):
        if self.size() == 0:
            message = self.client.messages \
                .create(
                     body='hola ' + user['name'] + ' es tu turno',
                     from_='+19103708697',
                     to='+56964436488'
                 )
        else:
             message = self.client.messages \
                .create(
                     body='hola ' + user['name'] + ' bienvenido/a, ' + str(self.size()) + " persona(s) se encuentran antes de ti",
                     from_='+19103708697',
                     to='+56964436488'
                 )

        self._queue.append(user)

    def dequeue(self):
        if self.size() > 0:
            if self._mode == 'FIFO':
                message = self.client.messages \
                .create(
                    body='hola ' + self._queue[1]['name']+ ' es tu turno',
                    from_='+19103708697',
                    to='+56964436488'
                 )
                next_user = self._queue.pop(0)
                return next_user
            elif self._mode == 'LIFO':
                next_user = self._queue.pop(-1)
                return next_user
        else:
            msg = {
                "msg": "No items in Queue"
            }
            return msg

    def get_queue(self):
        return self._queue

    def size(self):
        return len(self._queue)