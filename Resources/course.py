from flask import request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource
from app import db
from models import Course

class CourseResource(Resource):
    def get(self, course_id=None):
        try:
            if course_id:
                course = Course.query.get_or_404(course_id)
                return jsonify(course.serialize()), 200
            else:
                courses = Course.query.all()
                return jsonify([course.serialize() for course in courses]), 200
        except Exception as e:
            return jsonify({'message': 'Error retrieving course(s)', 'error': str(e)}), 500

    def post(self):
        try:
            data = request.get_json()
            new_course = Course(
                instructor_id=data['instructor_id'],
                title=data['title'],
                description=data['description'],
                price=data['price']
            )
            db.session.add(new_course)
            db.session.commit()
            return jsonify({'message': 'Course created successfully', 'course': new_course.serialize()}), 201
        except Exception as e:
            return jsonify({'message': 'Error creating course', 'error': str(e)}), 500

    def delete(self, course_id):
        try:
            course = Course.query.get_or_404(course_id)
            db.session.delete(course)
            db.session.commit()
            return jsonify({'message': 'Course deleted successfully'}), 204
        except Exception as e:
            return jsonify({'message': 'Error deleting course', 'error': str(e)}), 500
