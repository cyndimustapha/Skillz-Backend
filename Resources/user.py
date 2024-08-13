from flask import request, jsonify
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import User, Message, db
from datetime import datetime, timedelta
import cloudinary.uploader
import uuid
from flask_mail import Message as MailMessage
from app import mail

# In-memory storage for OTP (use a persistent storage in production)
otp_store = {}

class SignUpResource(Resource):
    def post(self):
        data = request.form
        first_name = data.get('firstName')
        last_name = data.get('lastName')
        role = data.get('role')
        email = data.get('email')
        password = data.get('password')
        bio = data.get('bio')

        if User.query.filter_by(email=email).first():
            return {'message': 'Email is already registered'}, 400

        profile_picture = request.files.get('profilePicture')
        profile_picture_url = None
        if profile_picture:
            upload_result = cloudinary.uploader.upload(profile_picture)
            profile_picture_url = upload_result.get('secure_url')

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        verification_token = str(uuid.uuid4())

        new_user = User(
            first_name=first_name,
            last_name=last_name,
            role=role,
            email=email,
            password=hashed_password,
            profile_picture=profile_picture_url,
            bio=bio,
            verification_token=verification_token
        )

        db.session.add(new_user)
        db.session.commit()

        # Send verification email
        verification_link = f"http://127.0.0.1:5000/verify/{verification_token}"
        msg = MailMessage("Verify Your Email", sender="your-email@example.com", recipients=[email])
        msg.body = f"Please click the following link to verify your email: {verification_link}"
        mail.send(msg)

        return {'message': 'Registration successful. Please check your email to verify your account.'}, 201

class VerifyEmailResource(Resource):
    def get(self, token):
        user = User.query.filter_by(verification_token=token).first()
        if user:
            user.verified = True
            user.verification_token = None  # Clear the token after verification
            db.session.commit()
            return {'message': 'Email verified successfully'}, 200
        else:
            return {'message': 'Invalid or expired token'}, 400

class SignInResource(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            if not user.verified:
                return {'message': 'Please verify your email before logging in'}, 403

            # Generate JWT token and 2FA code
            access_token = create_access_token(identity=user.id)
            otp = generate_otp()
            otp_store[email] = {
                'otp': otp,
                'expiry': datetime.now() + timedelta(minutes=5)  # OTP expires in 5 minutes
            }

            # Send OTP to the user's email
            subject = "Your 2FA Code"
            content = f"Your 2FA code is {otp}. It will expire in 5 minutes."
            if send_email(email, subject, content):
                return {'message': 'Please verify your 2FA code sent to your email'}, 200

            return {'message': 'Failed to send 2FA code'}, 500
        
        return {'message': 'Invalid credentials'}, 401

class Verify2FAResource(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        otp = data.get('otp')

        if email in otp_store:
            stored_otp = otp_store[email]['otp']
            expiry = otp_store[email]['expiry']
            if datetime.now() > expiry:
                return {'message': 'OTP expired'}, 400
            if otp == stored_otp:
                del otp_store[email]  # Remove OTP after successful verification
                # Generate JWT token
                user = User.query.filter_by(email=email).first()
                access_token = create_access_token(identity=user.id)
                return {'token': access_token}, 200
            return {'message': 'Invalid OTP'}, 400

        return {'message': 'No OTP found for email'}, 400

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

def generate_otp():
    import random
    import string
    return ''.join(random.choices(string.digits, k=6))

def send_email(to_email, subject, content):
    msg = MailMessage(subject=subject, recipients=[to_email], body=content)
    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
