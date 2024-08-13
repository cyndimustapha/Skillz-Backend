from flask import request, jsonify
from flask_restful import Resource
from models import Course, db

class CourseResource(Resource):
    def get(self, course_id=None):
        if course_id:
            # Get a single course by ID
            course = Course.query.get_or_404(course_id)
            return course.to_dict(), 200
        else:
            # Get all courses
            courses = Course.query.all()
            return [course.to_dict() for course in courses], 200

    def post(self):
        data = request.get_json()
        new_course = Course(
            instructor_id=data['instructor_id'],
            title=data['title'],
            description=data['description'],
            price=data['price'],
            image_url=data['image_url'],
            category=data('category')
        )
        db.session.add(new_course)
        db.session.commit()
        return new_course.to_dict(), 201

    def delete(self, course_id):
        course = Course.query.get_or_404(course_id)
        db.session.delete(course)
        db.session.commit()
        return {'message': 'Course deleted'}, 200