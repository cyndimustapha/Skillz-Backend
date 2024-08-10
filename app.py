from flask import Flask, jsonify, make_response, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from datetime import datetime, timedelta
import pytz
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_cors import CORS

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt_manager = JWTManager()
mail = Mail()

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
db.init_app(app)
migrate.init_app(app, db)
jwt_manager.init_app(app)
mail.init_app(app)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Define East African Time timezone
EAT = pytz.timezone('Africa/Nairobi')

def get_eat_now():
    return datetime.now(EAT)

# Import models and resources
from models import User, Course, CourseContent, Payment, Enrollment, Review, Message, Accolade
from Resources import (
    MessageResource,
    SignInResource,
    SignUpResource,
    SignOutResource,
    UsersInConversationResource,
    CourseResource,
    CourseContentResource,
    ReviewResource,
    # PaymentResource,
    EnrollmentResource,
    AccoladeResource, 
    AccoladeListResource,
)


# Register API resources
api = Api(app)
api.add_resource(MessageResource, '/messages')
api.add_resource(SignUpResource, '/sign-up')
api.add_resource(SignInResource, '/sign-in')
api.add_resource(SignOutResource, '/sign-out')
api.add_resource(UsersInConversationResource, '/users/conversations')
api.add_resource(CourseResource, '/courses')
api.add_resource(CourseContentResource, '/coursecontent')
# api.add_resource(PaymentResource, '/payments')
api.add_resource(EnrollmentResource, '/enrollments')
api.add_resource(ReviewResource, '/reviews')
api.add_resource(AccoladeListResource, '/accolades')
api.add_resource(AccoladeResource, '/accolades/<int:id>')



@app.before_request
def handle_preflight():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        return response

# Create tables and run the application
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
