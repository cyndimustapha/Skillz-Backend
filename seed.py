from app import app, db
from models import User, Course, CourseContent, Payment, Enrollment, Review, Message, Accolade
from datetime import datetime
import pytz
from faker import Faker
from werkzeug.security import generate_password_hash

# Define East African Time timezone
EAT = pytz.timezone('Africa/Nairobi')

# Define function to get current time in EAT
def get_eat_now():
    return datetime.now(EAT)

# Initialize Faker
fake = Faker()

# Define function to generate a Lorem Picsum image URL
def picsum_image_url(width, height, category=''):
    
    return f"https://picsum.photos/150/150"

def seed_database():
    with app.app_context():
        try:
            # Clear existing data
            db.drop_all()
            db.create_all()

            # Create sample users
            users = []
            for _ in range(10):  # Create 10 users
                role = fake.random_element(elements=('learner', 'instructor'))
                user = User(
                    role=role,
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    email=fake.unique.email(),  # Ensure unique emails
                    password=generate_password_hash('password123'),
                    profile_picture=picsum_image_url(150, 150, 'profile'),  # Placeholder profile picture
                    bio=fake.paragraph(nb_sentences=2),
                    verified=fake.boolean(),
                    created_at=get_eat_now(),
                    updated_at=get_eat_now()
                )
                users.append(user)
            
            db.session.add_all(users)
            db.session.commit()

            # Create sample courses
            courses = []
            for _ in range(5):  # Create 5 courses
                instructor = fake.random_element(elements=[user for user in users if user.role == 'instructor'])
                course = Course(
                    instructor_id=instructor.id,
                    title=fake.sentence(nb_words=4),
                    description=fake.paragraph(nb_sentences=3),
                    price=fake.random_number(digits=2),
                    created_at=get_eat_now(),
                    updated_at=get_eat_now(),
                    image=picsum_image_url(150, 150, 'course')  # Placeholder course image
                )
                courses.append(course)
            
            db.session.add_all(courses)
            db.session.commit()

            # Create sample course content
            course_contents = []
            for _ in range(15):  # Create 15 course contents
                course = fake.random_element(elements=courses)
                course_content = CourseContent(
                    course_id=course.id,
                    content_type=fake.random_element(elements=['Video', 'Text']),
                    content_url=fake.uri(),
                    created_at=get_eat_now(),
                    updated_at=get_eat_now()
                )
                course_contents.append(course_content)
            
            db.session.add_all(course_contents)
            db.session.commit()

            # Create sample enrollments
            enrollments = []
            for _ in range(5):  # Create 5 enrollments
                course = fake.random_element(elements=courses)
                learner = fake.random_element(elements=[user for user in users if user.role == 'learner'])
                enrollment = Enrollment(
                    course_id=course.id,
                    learner_id=learner.id,
                    status=fake.random_element(elements=['enrolled', 'completed']),
                    enrolled_at=get_eat_now()
                )
                enrollments.append(enrollment)
            
            db.session.add_all(enrollments)
            db.session.commit()

            # Create sample payments
            payments = []
            for _ in range(5):  # Create 5 payments
                enrollment = fake.random_element(elements=enrollments)
                payment = Payment(
                    course_id=enrollment.course_id,
                    learner_id=enrollment.learner_id,
                    amount=fake.random_number(digits=2),
                    payment_status=fake.random_element(elements=['completed', 'pending']),
                    payment_date=get_eat_now()
                )
                payments.append(payment)
            
            db.session.add_all(payments)
            db.session.commit()

            # Create sample reviews
            reviews = []
            for _ in range(5):  # Create 5 reviews
                course = fake.random_element(elements=courses)
                learner = fake.random_element(elements=[user for user in users if user.role == 'learner'])
                review = Review(
                    course_id=course.id,
                    learner_id=learner.id,
                    rating=fake.random_int(min=1, max=5),
                    comment=fake.text(max_nb_chars=200),
                    created_at=get_eat_now(),
                    updated_at=get_eat_now()
                )
                reviews.append(review)
            
            db.session.add_all(reviews)
            db.session.commit()

            # Create sample messages
            messages = []
            for _ in range(5):  # Create 5 messages
                sender = fake.random_element(elements=[user for user in users if user.role == 'learner'])
                receiver = fake.random_element(elements=[user for user in users if user.role == 'instructor'])
                message = Message(
                    sender_id=sender.id,
                    receiver_id=receiver.id,
                    content=fake.text(max_nb_chars=100),
                    sent_at=get_eat_now()
                )
                messages.append(message)
            
            db.session.add_all(messages)
            db.session.commit()

            # Create sample accolades
            accolades = []
            for _ in range(5):  # Create 5 accolades
                enrollment = fake.random_element(elements=enrollments)
                accolade = Accolade(
                    enrollment_id=enrollment.id,
                    accolade_type=fake.random_element(elements=['Completion Certificate', 'Achievement Badge']),
                    awarded_at=get_eat_now()
                )
                accolades.append(accolade)
            
            db.session.add_all(accolades)
            db.session.commit()

            print('Database seeded successfully!')
        except Exception as e:
            db.session.rollback()
            print(f"An error occurred: {e}")

if __name__ == '__main__':
    seed_database()
