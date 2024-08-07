from flask import request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource
from app import db
from models import CourseContent

class CourseContentResource(Resource):
    def get(self, content_id=None):
        try:
            if content_id:
                content = CourseContent.query.get_or_404(content_id)
                return jsonify(content.serialize()), 200
            else:
                contents = CourseContent.query.all()
                return jsonify([content.serialize() for content in contents]), 200
        except Exception as e:
            return jsonify({'message': 'Error retrieving content(s)', 'error': str(e)}), 500

    def post(self):
        try:
            data = request.get_json()
            new_content = CourseContent(
                course_id=data['course_id'],
                content_type=data['content_type'],
                content_url=data['content_url']
            )
            db.session.add(new_content)
            db.session.commit()
            return jsonify({'message': 'Content created successfully', 'content': new_content.serialize()}), 201
        except Exception as e:
            return jsonify({'message': 'Error creating content', 'error': str(e)}), 500

    def delete(self, content_id):
        try:
            content = CourseContent.query.get_or_404(content_id)
            db.session.delete(content)
            db.session.commit()
            return jsonify({'message': 'Content deleted successfully'}), 204
        except Exception as e:
            return jsonify({'message': 'Error deleting content', 'error': str(e)}), 500