from flask import Flask, jsonify, make_response, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_cors import CORS
from datetime import datetime, timedelta
import pytz

app = Flask(__name__)

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

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt_manager = JWTManager(app)
mail = Mail(app)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
api = Api(app)

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
