from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from models import db, Message, User
import logging

logging.basicConfig(level=logging.DEBUG)

class MessageResource(Resource):
    @jwt_required()
    def post(self):
        try:
            data = request.json
            logging.debug(f"Received data: {data}")

            sender_id = get_jwt_identity()
            receiver_id = data.get('receiver_id')
            content = data.get('content')

            if not receiver_id or not content:
                return {"error": "Receiver ID and content are required"}, 400

            message = Message(sender_id=sender_id, receiver_id=receiver_id, content=content)
            db.session.add(message)
            db.session.commit()

            response_data = {"message": "Message sent successfully", "data": message.to_dict()}
            logging.debug(f"Sending response: {response_data}")

            return response_data, 201

        except Exception as e:
            logging.error(f"Error: {e}", exc_info=True)
            return {"error": "Internal Server Error"}, 500
        
    @jwt_required()
    def get(self):
        try:
            current_user_id = get_jwt_identity()
            user_id = request.args.get('user_id')

            if user_id:
                messages = Message.query.filter(
                    ((Message.sender_id == current_user_id) & (Message.receiver_id == user_id)) |
                    ((Message.sender_id == user_id) & (Message.receiver_id == current_user_id))
                ).order_by(Message.sent_at.asc()).all()

                message_list = [message.to_dict() for message in messages]
                logging.debug(f"Messages retrieved: {message_list}")
                return message_list, 200

            else:
                conversations = db.session.query(User).filter(
                    (User.id == Message.receiver_id) | (User.id == Message.sender_id)
                ).distinct().all()

                conversation_list = [user.to_dict() for user in conversations]
                logging.debug(f"Conversations retrieved: {conversation_list}")
                return conversation_list, 200

        except Exception as e:
            logging.error(f"Error: {e}", exc_info=True)
            return {"error": "Internal Server Error"}, 500
