from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from models import db, Message, User

class MessageResource(Resource):
    @jwt_required()
    def post(self):
        data = request.json
        sender_id = get_jwt_identity()
        receiver_id = data.get('receiver_id')
        content = data.get('content')

        if not receiver_id or not content:
            return jsonify({"error": "Receiver ID and content are required"}), 400

        message = Message(sender_id=sender_id, receiver_id=receiver_id, content=content)
        db.session.add(message)
        db.session.commit()

        return jsonify({"message": "Message sent successfully", "data": message.to_dict()}), 201

    @jwt_required()
    def get(self, user_id=None):
        current_user_id = get_jwt_identity()

        if user_id:
            # Fetch messages between the current user and the specified user
            messages = Message.query.filter(
                ((Message.sender_id == current_user_id) & (Message.receiver_id == user_id)) |
                ((Message.sender_id == user_id) & (Message.receiver_id == current_user_id))
            ).order_by(Message.timestamp.asc()).all()

            message_list = [message.to_dict() for message in messages]
            return jsonify(message_list), 200

        else:
            # Get distinct users with whom the current user has conversations
            conversations = db.session.query(User).filter(
                (User.id == Message.receiver_id) | (User.id == Message.sender_id)
            ).distinct().all()

            conversation_list = [user.to_dict() for user in conversations]
            return jsonify(conversation_list), 200
