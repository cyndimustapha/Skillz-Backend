from flask import request, jsonify
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import User, Message, db
from datetime import datetime

class SignUpResource(Resource):
    def post(self):
        data = request.get_json()
        first_name = data.get('firstName')
        last_name = data.get('lastName')
        role = data.get('role')
        email = data.get('email')
        password = data.get('password')
        profile_picture = data.get('profilePicture')
        bio = data.get('bio')
        verified = data.get('verified', False)

        if User.query.filter_by(email=email).first():
            return {'message': 'Email is already registered'}, 400

        # Use 'pbkdf2:sha256' for password hashing
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        new_user = User(
            first_name=first_name,
            last_name=last_name,
            role=role,
            email=email,
            password=hashed_password,
            profile_picture=profile_picture,
            bio=bio,
            verified=verified
        )

        db.session.add(new_user)
        db.session.commit()

        return {'message': 'Registration successful'}, 201

class SignInResource(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            # Generate JWT token
            access_token = create_access_token(identity=user.id)

            # Optionally update last sign-in time if needed
            user.last_sign_in = datetime.now()
            db.session.commit()

            return {'token': access_token}, 200
        else:
            return {'message': 'Invalid credentials'}, 401
        
class SignOutResource(Resource):
    @jwt_required()
    def post(self):
        # Invalidate the token on the client side
        return {'message': 'Successfully logged out'}, 200
    
class UsersInConversationResource(Resource):
    @jwt_required()
    def get(self):
        # Get the current user's ID from JWT
        current_user_id = get_jwt_identity()
        if not isinstance(current_user_id, int):
            return jsonify({"error": "Invalid user ID format"}), 400

        # Retrieve all messages involving the current user
        received_messages = Message.query.filter_by(receiver_id=current_user_id).all()
        sent_messages = Message.query.filter_by(sender_id=current_user_id).all()

        # Collect user IDs from the messages
        user_ids = set(
            [msg.sender_id for msg in received_messages] +
            [msg.receiver_id for msg in sent_messages]
        )
        user_ids.discard(current_user_id)  # Remove the current user from the list

        # Fetch user details for the collected user IDs
        users = User.query.filter(User.id.in_(user_ids)).all()
        users_list = [user.to_dict() for user in users]

        return jsonify(users_list) 

class UserResource(Resource):
    @jwt_required()
    def get(self, user_id=None):
        if user_id:
            # Fetch a user by ID
            user = User.query.get(user_id)
            if user:
                return user.to_dict(), 200
            else:
                return {'message': 'User not found'}, 404
        else:
            # Fetch the currently logged-in user's details
            current_user_id = get_jwt_identity()
            user = User.query.get(current_user_id)
            if user:
                return user.to_dict(), 200
            else:
                return {'message': 'User not found'}, 404
