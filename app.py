import random
import string
from flask import Flask, jsonify, make_response, request
from flask_migrate import Migrate
from flask_restful import Api, Resource
from datetime import datetime, timedelta
import pytz
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_mail import Mail, Message
from flask_cors import CORS
from models import db, User, Message
import cloudinary
import cloudinary.uploader
import cloudinary.api
import uuid
import os

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

# Define East African Time timezone
EAT = pytz.timezone('Africa/Nairobi')

def get_eat_now():
    return datetime.now(EAT)

# Generate and send 2FA code
def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

def send_email(to_email, subject, content):
    msg = Message(subject=subject, recipients=[to_email], body=content)
    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

@app.route('/send-2fa', methods=['POST'])
def send_2fa():
    email = request.json.get('email')
    if email:
        otp = generate_otp()
        otp_store[email] = {
            'otp': otp,
            'expiry': datetime.now() + timedelta(minutes=5)  # OTP expires in 5 minutes
        }
        subject = "Your 2FA Code"
        content = f"Your 2FA code is {otp}. It will expire in 5 minutes."
        if send_email(email, subject, content):
            return jsonify({'message': '2FA code sent to email'}), 200
        return jsonify({'message': 'Failed to send email'}), 500
    return jsonify({'message': 'Email is required'}), 400

@app.route('/verify-2fa', methods=['POST'])
def verify_2fa():
    email = request.json.get('email')
    otp = request.json.get('otp')
    if email in otp_store:
        stored_otp = otp_store[email]['otp']
        expiry = otp_store[email]['expiry']
        if datetime.now() > expiry:
            return jsonify({'message': 'OTP expired'}), 400
        if otp == stored_otp:
            del otp_store[email]  # Remove OTP after successful verification
            return jsonify({'message': 'OTP verified'}), 200
        return jsonify({'message': 'Invalid OTP'}), 400
    return jsonify({'message': 'No OTP found for email'}), 400

# In-memory storage for simplicity
otp_store = {}

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
    CourseResource,
    CourseContentResource,
    ReviewResource,
    EnrollmentResource,
    AccoladeResource, 
    AccoladeListResource,
    PaymentResource,
    VerifyEmailResource,
    Verify2FAResource,
    UserProfileResource

)

# Register API resources
api = Api(app)
api.add_resource(MessageResource, '/messages', '/messages/<int:user_id>')
api.add_resource(SignUpResource, '/sign-up')
api.add_resource(SignInResource, '/sign-in')
api.add_resource(SignOutResource, '/sign-out')
api.add_resource(UsersInConversationResource, '/users/conversations')
api.add_resource(CourseResource, '/courses', '/courses/<int:course_id>')
api.add_resource(CourseContentResource, '/coursecontents', '/coursecontents/<int:content_id>')
api.add_resource(PaymentResource, '/sendSTKPush')
api.add_resource(EnrollmentResource, '/enrollments')
api.add_resource(AccoladeListResource, '/accolades')
api.add_resource(AccoladeResource, '/accolades/<int:id>')
api.add_resource(ReviewResource, '/reviews', '/reviews/<int:review_id>')
api.add_resource(VerifyEmailResource, '/verify/<string:token>')
api.add_resource(Verify2FAResource, '/verify-2fa')
api.add_resource(UserProfileResource, '/user/profile')



# Create tables and run the application
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
