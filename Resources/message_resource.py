from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models import Message, User
from datetime import datetime, timezone
from flasgger import swag_from

class MessageResource(Resource):
    @swag_from({
        'responses': {
            201: {
                'description': 'Message created successfully',
                'schema': {'type': 'object'}
            },
            400: {
                'description': 'User ID and message text are required'
            },
            404: {
                'description': 'Recipient not found or Sender not found'
            }
        }
    })
    @jwt_required()
    def post(self):
        data = request.get_json()

        receiver_id = data.get('user_id')
        message_text = data.get('message')

        if not receiver_id or not message_text:
            return jsonify({"error": "User ID and message text are required"}), 400

        recipient = User.query.get(receiver_id)
        if not recipient:
            return jsonify({"error": "Recipient not found"}), 404

        sender_info = get_jwt_identity()
        sender_id = sender_info['id']
        
        sender = User.query.get(sender_id)
        if not sender:
            return jsonify({"error": "Sender not found"}), 404

        new_message = Message(
            sender_id=sender.id,
            recipient_id=recipient.id,
            content=message_text,
            sent_at=datetime.now(timezone.utc)
        )

        db.session.add(new_message)
        db.session.commit()

        return jsonify(new_message.to_dict()), 201

    @swag_from({
        'responses': {
            200: {
                'description': 'List of messages',
                'schema': {
                    'type': 'array',
                    'items': {'type': 'object'}
                }
            },
            404: {
                'description': 'User not found'
            }
        }
    })
    @jwt_required()
    def get(self):
        sender_info = get_jwt_identity()
        user_id = sender_info['id']

        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        sent_messages = Message.query.filter_by(sender_id=user.id).order_by(Message.sent_at.desc()).all()
        received_messages = Message.query.filter_by(receiver_id=user.id).order_by(Message.sent_at.desc()).all()

        all_messages = sorted(sent_messages + received_messages, key=lambda x: x.sent_at, reverse=True)

        return jsonify([message.to_dict() for message in all_messages]), 200
