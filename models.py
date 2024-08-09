from app import db
from sqlalchemy_serializer import SerializerMixin
import pytz
from datetime import datetime

# Define East African Time timezone
EAT = pytz.timezone('Africa/Nairobi')

def get_eat_now():
    return datetime.now(EAT)

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    profile_picture = db.Column(db.String(255), nullable=True)  # Optional
    bio = db.Column(db.Text, nullable=True)  # Optional
    verified = db.Column(db.Boolean, default=False)  # Optional, default to False
    created_at = db.Column(db.TIMESTAMP, default=get_eat_now)
    updated_at = db.Column(db.TIMESTAMP, default=get_eat_now, onupdate=get_eat_now)

    courses = db.relationship('Course', backref='user', lazy=True)
    enrollments = db.relationship('Enrollment', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)
    sent_messages = db.relationship('Message', foreign_keys='Message.sender_id', backref='sender', lazy=True)
    received_messages = db.relationship('Message', foreign_keys='Message.receiver_id', backref='receiver', lazy=True)
    payments = db.relationship('Payment', backref='learner', lazy=True)

class Course(db.Model, SerializerMixin):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    instructor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(255))
    description = db.Column(db.Text)
    price = db.Column(db.DECIMAL(10, 2))
    created_at = db.Column(db.TIMESTAMP, default=get_eat_now)
    updated_at = db.Column(db.TIMESTAMP, default=get_eat_now, onupdate=get_eat_now)

    contents = db.relationship('CourseContent', backref='course', lazy=True)
    enrollments = db.relationship('Enrollment', backref='course', lazy=True)
    reviews = db.relationship('Review', backref='course', lazy=True)
    payments = db.relationship('Payment', backref='course', lazy=True)

class CourseContent(db.Model, SerializerMixin):
    __tablename__ = 'coursecontent'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    content_type = db.Column(db.String(50))
    content_url = db.Column(db.String(255))
    created_at = db.Column(db.TIMESTAMP, default=get_eat_now)
    updated_at = db.Column(db.TIMESTAMP, default=get_eat_now, onupdate=get_eat_now)

class Payment(db.Model, SerializerMixin):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    learner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.DECIMAL(10, 2))
    payment_status = db.Column(db.String(50))
    payment_date = db.Column(db.TIMESTAMP, default=get_eat_now)

class Enrollment(db.Model, SerializerMixin):
    __tablename__ = 'enrollments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    learner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(50))
    enrolled_at = db.Column(db.TIMESTAMP, default=get_eat_now)
    completed_at = db.Column(db.TIMESTAMP)

    accolades = db.relationship('Accolade', backref='enrollment', lazy=True)

class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    learner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Integer)
    comment = db.Column(db.Text)
    created_at = db.Column(db.TIMESTAMP, default=get_eat_now)
    updated_at = db.Column(db.TIMESTAMP, default=get_eat_now, onupdate=get_eat_now)

class Message(db.Model, SerializerMixin):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) 
    content = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, default=db.func.now())

    def __repr__(self):
        return f"<Message {self.id}: from {self.sender_id} to {self.receiver_id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "sender_id": self.sender_id,
            "receiver_id": self.receiver_id,
            "content": self.content,
            "sent_at": self.sent_at.isoformat()
        }

class Accolade(db.Model, SerializerMixin):
    __tablename__ = 'accolades'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    enrollment_id = db.Column(db.Integer, db.ForeignKey('enrollments.id'), nullable=False)
    accolade_type = db.Column(db.String(100))
    awarded_at = db.Column(db.TIMESTAMP, default=get_eat_now)
