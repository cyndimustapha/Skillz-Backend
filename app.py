import os
import random
import string
from datetime import datetime, timedelta

from flask import Flask, jsonify, make_response, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_mail import Mail, Message as MailMessage
from flask_migrate import Migrate
from flask_restful import Api

import cloudinary
import cloudinary.uploader
import cloudinary.api
import pytz

from models import db, User, Message

# Initialize the Flask app
app = Flask(__name__)

# Configurations
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'Skillz_key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///yourdatabase.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', 'skillzgroup41@gmail.com')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', 'bpyk njqd znuo qhkv')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', 'skillzgroup41@gmail.com')

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
jwt_manager = JWTManager(app)
mail = Mail(app)
CORS(app)

cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME', 'dx0dgxzpk'),
    api_key=os.getenv('CLOUDINARY_API_KEY', '528686173472686'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET', 'vl_n-rurd_6IJQ-TM_oC8ruukyk')
)

# In-memory storage for OTP (use a persistent storage in production)
otp_store = {}

# Define East African Time timezone
EAT = pytz.timezone('Africa/Nairobi')

def get_eat_now():
    return datetime.now(EAT)

# Utility functions
def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

def send_email(mail, to_email, subject, content):
    msg = MailMessage(subject=subject, recipients=[to_email], body=content)
    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
    
# Handle CORS preflight requests
@app.before_request
def handle_preflight():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        return response

# Import resources
from Resources import (
    MessageResource,
    SignInResource,
    SignUpResource,
    SignOutResource,
    UsersInConversationResource,
    AllUsersResource,
    EditUserResource,
    UserResource,
    CourseResource,
    CourseContentResource,
    ReviewResource,
    EnrollmentResource,
    AccoladeResource, 
    AccoladeListResource,
    Verify2FAResource,
    VerifyEmailResource,
    PaymentResource
)


api = Api(app)
api.add_resource(MessageResource, '/messages', '/messages/<int:user_id>')
api.add_resource(SignUpResource, '/sign-up')
api.add_resource(SignInResource, '/sign-in')
api.add_resource(SignOutResource, '/sign-out')
api.add_resource(UsersInConversationResource, '/users/conversations')
api.add_resource(UserResource, '/users', '/users/<int:user_id>')
api.add_resource(AllUsersResource, '/users/all')
api.add_resource(EditUserResource, '/users/edit')
api.add_resource(PaymentResource, '/sendSTKPush')
api.add_resource(CourseResource, '/courses', '/courses/<int:course_id>')
api.add_resource(CourseContentResource, '/coursecontents', '/coursecontents/<int:content_id>')
api.add_resource(EnrollmentResource, '/enrollments/<int:learner_id>')
api.add_resource(AccoladeListResource, '/accolades')
api.add_resource(AccoladeResource, '/accolades/<int:id>')
api.add_resource(ReviewResource, '/reviews', '/reviews/<int:review_id>')
api.add_resource(VerifyEmailResource, '/verify/<string:token>')
api.add_resource(Verify2FAResource, '/verify-2fa')


# Create tables and run the application
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
