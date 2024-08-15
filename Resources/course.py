from flask import request, jsonify
from flask_restful import Resource
from models import Course, db
import cloudinary
import cloudinary.uploader

class CourseResource(Resource):
    def get(self, course_id=None):
        if course_id:
            # Get a single course by ID
            course = Course.query.get_or_404(course_id)
            return course.to_dict(), 200
        else:
            # Get all courses or filter by instructor_id
            instructor_id = request.args.get('instructor_id')
            if instructor_id:
                courses = Course.query.filter_by(instructor_id=instructor_id).all()
            else:
                courses = Course.query.all()
            return [course.to_dict() for course in courses], 200

    def post(self):
        data = request.get_json()
        image_file = request.files.get('file')  # Ensure this key matches the key used in FormData

        image_url = None
        if image_file:
            try:
                upload_result = cloudinary.uploader.upload(image_file)
                image_url = upload_result.get('secure_url')
            except Exception as e:
                return {'message': f'Error uploading image: {str(e)}'}, 500

        new_course = Course(
            instructor_id=data['instructor_id'],
            title=data['title'],
            description=data['description'],
            price=data['price'],
            image_url=image_url,  
            category=data.get('category') 
        )
        db.session.add(new_course)
        db.session.commit()
        return new_course.to_dict(), 201

    def delete(self, course_id):
        course = Course.query.get_or_404(course_id)
        db.session.delete(course)
        db.session.commit()
        return {'message': 'Course deleted'}, 200
