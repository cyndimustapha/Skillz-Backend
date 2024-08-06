# resources/message_resource.py

from flask import request
from flask_restful import Resource
from app import db
from models import Message

class MessageResource(Resource):
    def get(self, message_id=None):
        if message_id:
            message = Message.query.get_or_404(message_id)
            return message.to_dict(), 200
        else:
            messages = Message.query.all()
            return [message.to_dict() for message in messages], 200

    def post(self):
        data = request.get_json()
        new_message = Message(
            sender_id=data.get('sender_id'),
            receiver_id=data.get('receiver_id'),
            content=data.get('content')
        )
        db.session.add(new_message)
        db.session.commit()
        return new_message.to_dict(), 201

    def delete(self, message_id):
        message = Message.query.get_or_404(message_id)
        db.session.delete(message)
        db.session.commit()
        return '', 204
