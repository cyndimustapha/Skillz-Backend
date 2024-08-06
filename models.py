from datetime import datetime
import pytz
from app import db, get_eat_now
from sqlalchemy_serializer import SerializerMixin

class Instructor(db.Model, SerializerMixin):
    __tablename__ = 'instructors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    profile_picture = db.Column(db.String(255))
    bio = db.Column(db.Text)
    verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    courses = db.relationship('Course', backref='instructor', lazy=True)
    sent_messages = db.relationship('Message', foreign_keys='Message.sender_id', backref='sender_instructor', lazy=True)
    received_messages = db.relationship('Message', foreign_keys='Message.recipient_id', backref='recipient_instructor', lazy=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "profile_picture": self.profile_picture,
            "bio": self.bio,
            "verified": self.verified,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "user_type": "instructor" 
        }


class Learner(db.Model, SerializerMixin):
    __tablename__ = 'learners'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    profile_picture = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    enrollments = db.relationship('Enrollment', backref='learner', lazy=True)
    reviews = db.relationship('Review', backref='learner', lazy=True)
    sent_messages = db.relationship('Message', foreign_keys='Message.sender_id', backref='sender_learner', lazy=True)
    received_messages = db.relationship('Message', foreign_keys='Message.recipient_id', backref='recipient_learner', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "profile_picture": self.profile_picture,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "user_type": "learner"
        }


class Course(db.Model, SerializerMixin):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    contents = db.relationship('CourseContent', backref='course', lazy=True)
    enrollments = db.relationship('Enrollment', backref='course', lazy=True)
    reviews = db.relationship('Review', backref='course', lazy=True)


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
    learner_id = db.Column(db.Integer, db.ForeignKey('learners.id'), nullable=False)
    amount = db.Column(db.DECIMAL(10, 2))
    payment_status = db.Column(db.String(50))
    payment_date = db.Column(db.TIMESTAMP, default=get_eat_now)


class Enrollment(db.Model, SerializerMixin):
    __tablename__ = 'enrollments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    learner_id = db.Column(db.Integer, db.ForeignKey('learners.id'), nullable=False)
    status = db.Column(db.String(50))
    enrolled_at = db.Column(db.TIMESTAMP, default=get_eat_now)
    completed_at = db.Column(db.TIMESTAMP)

    accolades = db.relationship('Accolade', backref='enrollment', lazy=True)


class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    learner_id = db.Column(db.Integer, db.ForeignKey('learners.id'), nullable=False)
    rating = db.Column(db.Integer)
    comment = db.Column(db.Text)
    created_at = db.Column(db.TIMESTAMP, default=get_eat_now)
    updated_at = db.Column(db.TIMESTAMP, default=get_eat_now, onupdate=get_eat_now)

class Message(db.Model, SerializerMixin):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, nullable=False)  # Can be either Learner or Instructor ID
    recipient_id = db.Column(db.Integer, nullable=False)  # Can be either Learner or Instructor ID
    content = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, default=db.func.now())

    def __repr__(self):
        return f"<Message {self.id}: from {self.sender_id} to {self.recipient_id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "sender_id": self.sender_id,
            "recipient_id": self.recipient_id,
            "content": self.content,
            "sent_at": self.sent_at.isoformat()
        }


class Accolade(db.Model, SerializerMixin):
    __tablename__ = 'accolades'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    enrollment_id = db.Column(db.Integer, db.ForeignKey('enrollments.id'), nullable=False)
    accolade_type = db.Column(db.String(100))
    awarded_at = db.Column(db.TIMESTAMP, default=get_eat_now)
