from app import app, db
from models import User, Course, CourseContent, Payment, Enrollment, Review, Message, Accolade
from datetime import datetime
import pytz

# Define East African Time timezone
EAT = pytz.timezone('Africa/Nairobi')

# Define function to get current time in EAT
def get_eat_now():
    return datetime.now(EAT)

def seed_database():
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()

        # Create sample users
        user1 = User(
            role='learner',
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            password='hashedpassword',
            profile_picture='profile1.jpg',
            bio='A passionate learner.',
            verified=True,
            created_at=get_eat_now(),
            updated_at=get_eat_now()
        )
        
        user2 = User(
            role='instructor',
            first_name='Jane',
            last_name='Smith',
            email='jane.smith@example.com',
            password='hashedpassword',
            profile_picture='profile2.jpg',
            bio='An experienced instructor.',
            verified=True,
            created_at=get_eat_now(),
            updated_at=get_eat_now()
        )
        
        db.session.add_all([user1, user2])
        db.session.commit()

        # Create sample course
        course1 = Course(
            instructor_id=user2.id,
            title='Introduction to Programming',
            description='A comprehensive course on programming basics.',
            price=99.99,
            created_at=get_eat_now(),
            updated_at=get_eat_now()
        )

        db.session.add(course1)
        db.session.commit()

        # Create sample course content
        course_content1 = CourseContent(
            course_id=course1.id,
            content_type='Video',
            content_url='http://example.com/video1.mp4',
            created_at=get_eat_now(),
            updated_at=get_eat_now()
        )

        db.session.add(course_content1)
        db.session.commit()

        # Create sample enrollment
        enrollment1 = Enrollment(
            course_id=course1.id,
            learner_id=user1.id,
            status='enrolled',
            enrolled_at=get_eat_now()
        )

        db.session.add(enrollment1)
        db.session.commit()

        # Create sample payment
        payment1 = Payment(
            course_id=course1.id,
            learner_id=user1.id,
            amount=99.99,
            payment_status='completed',
            payment_date=get_eat_now()
        )

        db.session.add(payment1)
        db.session.commit()

        # Create sample review
        review1 = Review(
            course_id=course1.id,
            learner_id=user1.id,
            rating=5,
            comment='Great course!',
            created_at=get_eat_now(),
            updated_at=get_eat_now()
        )

        db.session.add(review1)
        db.session.commit()

        # Create sample message
        message1 = Message(
            sender_id=user1.id,
            receiver_id=user2.id,
            content='Hello, I have a question about the course.',
            sent_at=get_eat_now()
        )

        db.session.add(message1)
        db.session.commit()

        # Create sample accolade
        accolade1 = Accolade(
            enrollment_id=enrollment1.id,
            accolade_type='Completion Certificate',
            awarded_at=get_eat_now()
        )

        db.session.add(accolade1)
        db.session.commit()

        print('Database seeded!')

if __name__ == '__main__':
    seed_database()
