from flask import request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource
from app import db
from models import Review

class ReviewResource(Resource):
    def get(self, Review_id=None):
        if Review_id:
            Review = Review.query.get_or_404(Review_id)
            return Review.to_dict(), 200
        else:
            Review = Review.query.all()
            return Review. to_dict(), 200
        
    def post(self):
            data = request.get_json()
            new_Review = Review(
                course_id=data['course_id'],
                learner_id=data['learner_id'],
                rating=data['rating'],
                comment=data['comment']
            )
            db.session.add(new_Review)
            db.session.commit()
            return jsonify(new_Review.serialize())
    
    def delete(self, Review_id):
        review = Review.query.get_or_404(Review_id)
        db.session.delete(review)
        db.session.commit()
        return '', 204
              
