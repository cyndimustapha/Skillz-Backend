

from flask import Flask, jsonify, make_response,request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from datetime import datetime
import pytz
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask_mail import Mail
from flask_cors import CORS


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'Skillz_key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)
jwt_manager = JWTManager(app)


# Configurations
app.config['JWT_SECRET_KEY'] = 'Skillz_key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourdatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.example.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'your-email@example.com'
app.config['MAIL_PASSWORD'] = 'your-email-password'
app.config['MAIL_DEFAULT_SENDER'] = 'your-email@example.com'

db = SQLAlchemy(app)
migrate = Migrate(app, db)


db.init_app(app)
mail = Mail(app)

CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

migrate = Migrate(app, db, render_as_batch=True)

api = Api(app)

api.add_resource(User, '/users')
api.add_resource(Course, '/courses')
api.add_resource(CourseContent, '/coursecontent')
api.add_resource (Payment, '/payments')
api.add_resource(Enrollment, '/enrollments')
api.add_resource(Review, '/reviews')
api.add_resource(Message, '/messages')
api.add_resource(Accolade, '/accolades')

@app.before_request
def handle_preflight():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        return response



with app.app_context():
    db.create_all()


# Define East African Time timezone
EAT = pytz.timezone('Africa/Nairobi')

def get_eat_now():
    return datetime.now(EAT)

# Import models and resources
from models import User, Course, CourseContent, Payment, Enrollment, Review, Message, Accolade
from Resources import (
    
    MessageResource
)

# Register API resources
#api.add_resource(UserResource, '/users')
#api.add_resource(CourseResource, '/courses')
#api.add_resource(CourseContentResource, '/coursecontent')
#api.add_resource(PaymentResource, '/payments')
#api.add_resource(EnrollmentResource, '/enrollments')
#api.add_resource(ReviewResource, '/reviews')
api.add_resource(MessageResource, '/messages')
#api.add_resource(AccoladeResource, '/accolades')

# Handle CORS preflight requests
@app.before_request
def handle_preflight():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        return response

# Create tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

