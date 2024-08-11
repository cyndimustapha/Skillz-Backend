from flask import request, jsonify
from flask_restful import Resource
from models import CourseContent, db

class CourseContentResource(Resource):
    def get(self, content_id=None):
        if content_id:
            # Get a single content by ID
            content = CourseContent.query.get_or_404(content_id)
            return content.to_dict(), 200
        else:
            # Get all contents
            contents = CourseContent.query.all()
            return [content.to_dict() for content in contents], 200

    def post(self):
        data = request.get_json()
        new_content = CourseContent(
            course_id=data['course_id'],
            content_type=data['content_type'],
            content_url=data['content_url']
        )
        db.session.add(new_content)
        db.session.commit()
        return new_content.to_dict(), 201

    def delete(self, content_id):
        content = CourseContent.query.get_or_404(content_id)
        db.session.delete(content)
        db.session.commit()
        return {'message': 'Content deleted'}, 200