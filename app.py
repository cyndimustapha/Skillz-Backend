from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from flask_migrate import Migrate
from datetime import datetime
import pytz
from Resources import (
    InstructorResource, LearnerResource, CourseResource, 
    CourseContentResource, PaymentResource, EnrollmentResource, 
    ReviewResource, MessageResource, AccoladeResource
)


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourdatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define East African Time timezone
EAT = pytz.timezone('Africa/Nairobi')

def get_eat_now():
    return datetime.now(EAT)

from models import User, Course, CourseContent, Payment, Enrollment, Review, Message, Accolade

# Registering Resources
api.add_resource(MessageResource, '/messages', '/messages/<int:message_id>')

if __name__ == '__main__':
    app.run(debug=True)
