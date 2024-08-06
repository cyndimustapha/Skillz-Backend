from flask import request
from flask_restful import Resource
from app import db
from models import User

class UserResource(Resource):
    def get(self, user_id=None):
        if user_id:
            user = User.query.get(user_id)
            if user:
                return user.to_dict(), 200
            else:
                return {'message': 'User not found'}, 404
        else:
            users = User.query.all()
            return [user.to_dict() for user in users], 200

    def post(self):
        data = request.get_json()
        # Ensure all required fields are provided
        if not all(field in data for field in ['role', 'name', 'email', 'password']):
            return {'message': 'Missing required fields'}, 400

        # Create new User instance
        new_user = User(
            role=data.get('role'),
            name=data.get('name'),
            email=data.get('email'),
            password=data.get('password'), 
            profile_picture=data.get('profile_picture'),
            bio=data.get('bio'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )
        
        db.session.add(new_user)
        db.session.commit()
        return new_user.to_dict(), 201

    def delete(self, user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return '', 204
        else:
            return {'message': 'User not found'}, 404
