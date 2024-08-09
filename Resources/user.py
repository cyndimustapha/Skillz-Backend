from flask import request, jsonify
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from app import db
from models import User
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