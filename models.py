from datetime import datetime
import pytz
from app import db, get_eat_now
from sqlalchemy_serializer import SerializerMixin

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role = db.Column(db.String(50))
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    profile_picture = db.Column(db.String(255))
    bio = db.Column(db.Text)
    verified = db.Column(db.Boolean)
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
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text)
    sent_at = db.Column(db.TIMESTAMP, default=get_eat_now)

class Accolade(db.Model, SerializerMixin):
    __tablename__ = 'accolades'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    enrollment_id = db.Column(db.Integer, db.ForeignKey('enrollments.id'), nullable=False)
    accolade_type = db.Column(db.String(100))
    awarded_at = db.Column(db.TIMESTAMP, default=get_eat_now)

