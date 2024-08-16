# from app import app, db
# from models import User, Course, CourseContent, Payment, Enrollment, Review, Message, Accolade
# from datetime import datetime
# import pytz
# from faker import Faker
# from werkzeug.security import generate_password_hash

# # Define East African Time timezone
# EAT = pytz.timezone('Africa/Nairobi')

# # Define function to get current time in EAT
# def get_eat_now():
#     return datetime.now(EAT)

# # Initialize Faker
# fake = Faker()

# def seed_database():
#     with app.app_context():
#         # Clear existing data
#         db.drop_all()
#         db.create_all()

#         # Create sample users
#         users = []
#         for _ in range(10):  # Create 10 users
#             role = fake.random_element(elements=('learner', 'instructor'))
#             user = User(
#                 role=role,
#                 first_name=fake.first_name(),
#                 last_name=fake.last_name(),
#                 email=fake.email(),
#                 password=generate_password_hash('password123'),
#                 profile_picture=fake.image_url(),
#                 bio=fake.paragraph(nb_sentences=2),
#                 verified=fake.boolean(),
#                 created_at=get_eat_now(),
#                 updated_at=get_eat_now()
#             )
#             users.append(user)
        
#         db.session.add_all(users)
#         db.session.commit()

#         # Create sample courses
#         categories = ['Cooking', 'Tech', 'Human Relations', 'AI', 'Business', 'Art', 'Science']
#         courses = []
#         for i in range(15):  # Create 15 courses
#            instructor = fake.random_element(elements=[user for user in users if user.role == 'instructor'])
#            category = fake.random_element(categories)  # Randomly select a category                                    
#            image_url = f'https://images.pexels.com/photos/459403/pexels-photo-459403.jpeg?auto=compress&cs=tinysrgb&w={1260 + i}&h={750 + i}&dpr=1' 

#            course = Course(
#                instructor_id=instructor.id,
#                title=fake.sentence(nb_words=4),
#                description=fake.paragraph(nb_sentences=3),
#                price=fake.random_number(digits=3),
#                image_url=image_url,  # Unique placeholder course image
#                category=category,
#                created_at=get_eat_now(),
#                updated_at=get_eat_now()
#            )
#            courses.append(course)

#         db.session.add_all(courses)
#         db.session.commit()

#         # Create sample course content
#         course_contents = []
#         for _ in range(15):  # Create 15 course contents
#             course = fake.random_element(elements=courses)
#             course_content = CourseContent(
#                 course_id=course.id,
#                 content_type=fake.random_element(elements=['Video', 'Text']),
#                 content_url=fake.uri(),
#                 created_at=get_eat_now(),
#                 updated_at=get_eat_now()
#             )
#             course_contents.append(course_content)
        
#         db.session.add_all(course_contents)
#         db.session.commit()

        # Create sample enrollments
#         enrollments = []
#         for _ in range(5):  # Create 5 enrollments
#             course = fake.random_element(elements=courses)
#             learner = fake.random_element(elements=[user for user in users if user.role == 'learner'])
#             enrollment = Enrollment(
#                 course_id=course.id,
#                 learner_id=learner.id,
#                 status=fake.random_element(elements=['enrolled', 'completed']),
#                 enrolled_at=get_eat_now()
#             )
#             enrollments.append(enrollment)
        
#         db.session.add_all(enrollments)
#         db.session.commit()
        
#         # Create sample payments
#         payments = []
#         for _ in range(5):  # Create 5 payments
#             enrollment = fake.random_element(elements=enrollments)
#             payment = Payment(
#                 course_id=enrollment.course_id,
#                 learner_id=enrollment.learner_id,
#                 amount=fake.random_number(digits=2),
#                 payment_status=fake.random_element(elements=['completed', 'pending']),
#                 payment_date=get_eat_now()
#             )
#             payments.append(payment)
        
#         db.session.add_all(payments)
#         db.session.commit()

#         # Create sample reviews
#         reviews = []
#         for _ in range(5):  # Create 5 reviews
#             course = fake.random_element(elements=courses)
#             learner = fake.random_element(elements=[user for user in users if user.role == 'learner'])
#             review = Review(
#                 course_id=course.id,
#                 learner_id=learner.id,
#                 rating=fake.random_int(min=1, max=5),
#                 comment=fake.text(max_nb_chars=200),
#                 created_at=get_eat_now(),
#                 updated_at=get_eat_now()
#             )
#             reviews.append(review)
        
#         db.session.add_all(reviews)
#         db.session.commit()

#         # Create sample messages
#         messages = []
#         for _ in range(5):  # Create 5 messages
#             sender = fake.random_element(elements=[user for user in users if user.role == 'learner'])
#             receiver = fake.random_element(elements=[user for user in users if user.role == 'instructor'])
#             message = Message(
#                 sender_id=sender.id,
#                 receiver_id=receiver.id,
#                 content=fake.text(max_nb_chars=100),
#                 sent_at=get_eat_now()
#             )
#             messages.append(message)
        
#         db.session.add_all(messages)
#         db.session.commit()

#         # Create sample accolades
#         accolades = []
#         for _ in range(5):  # Create 5 accolades
#             enrollment = fake.random_element(elements=enrollments)
#             accolade = Accolade(
#                 enrollment_id=enrollment.id,
#                 accolade_type=fake.random_element(elements=['Completion Certificate', 'Achievement Badge']),
#                 awarded_at=get_eat_now()
#             )
#             accolades.append(accolade)
        
#         db.session.add_all(accolades)
#         db.session.commit()

#         print('Database seeded!')

# if __name__ == '__main__':
#     seed_database()

from app import app, db
from models import User, Course, CourseContent, Payment, Enrollment, Review, Message, Accolade
from datetime import datetime
import pytz
from werkzeug.security import generate_password_hash

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

        # Create real sample users
        users = [
            User(
                role='learner',
                first_name='Alice',
                last_name='Johnson',
                email='alice.johnson@example.com',
                password=generate_password_hash('password123'),
                profile_picture='https://example.com/images/alice.jpg',
                bio='Aspiring data scientist passionate about AI and machine learning.',
                verified=True,
                created_at=get_eat_now(),
                updated_at=get_eat_now()
            ),
            User(
                role='instructor',
                first_name='Bob',
                last_name='Smith',
                email='bob.smith@example.com',
                password=generate_password_hash('password123'),
                profile_picture='https://example.com/images/bob.jpg',
                bio='Seasoned software engineer with 10+ years of experience.',
                verified=True,
                created_at=get_eat_now(),
                updated_at=get_eat_now()
            ),
            User(
                role='instructor',
                first_name='Carol',
                last_name='Williams',
                email='carol.williams@example.com',
                password=generate_password_hash('password123'),
                profile_picture='https://example.com/images/carol.jpg',
                bio='Expert chef and culinary instructor.',
                verified=True,
                created_at=get_eat_now(),
                updated_at=get_eat_now()
            ),
            User(
                role='instructor',
                first_name='David',
                last_name='Brown',
                email='david.brown@example.com',
                password=generate_password_hash('password123'),
                profile_picture='https://example.com/images/david.jpg',
                bio='Professional artist specializing in digital art.',
                verified=True,
                created_at=get_eat_now(),
                updated_at=get_eat_now()
            ),
            User(
                role='learner',
                first_name='Eve',
                last_name='Davis',
                email='eve.davis@example.com',
                password=generate_password_hash('password123'),
                profile_picture='https://example.com/images/eve.jpg',
                bio='Business analyst with a passion for entrepreneurship.',
                verified=True,
                created_at=get_eat_now(),
                updated_at=get_eat_now()
            )
            # Add more real users if needed
        ]

        db.session.add_all(users)
        db.session.commit()

        # Create real sample courses
        courses = [
            Course(
                instructor_id=users[1].id,  # Bob
                title='Introduction to Python Programming',
                description='Learn the basics of Python, one of the most popular programming languages.',
                price=50,
                image_url='https://example.com/images/python-course.jpg',
                category='Tech',
                created_at=get_eat_now(),
                updated_at=get_eat_now()
            ),
            Course(
                instructor_id=users[1].id,  # Bob
                title='AI for Beginners',
                description='A foundational course in Artificial Intelligence, covering key concepts and applications.',
                price=100,
                image_url='https://example.com/images/ai-course.jpg',
                category='AI',
                created_at=get_eat_now(),
                updated_at=get_eat_now()
            ),
            Course(
                instructor_id=users[2].id,  # Carol
                title='Mastering Italian Cuisine',
                description='A comprehensive guide to cooking authentic Italian dishes.',
                price=75,
                image_url='https://example.com/images/italian-cuisine.jpg',
                category='Cooking',
                created_at=get_eat_now(),
                updated_at=get_eat_now()
            ),
            Course(
                instructor_id=users[2].id,  # Carol
                title='Baking for Beginners',
                description='Learn the basics of baking delicious bread and pastries.',
                price=60,
                image_url='https://example.com/images/baking-course.jpg',
                category='Cooking',
                created_at=get_eat_now(),
                updated_at=get_eat_now()
            ),
            Course(
                instructor_id=users[3].id,  # David
                title='Introduction to Digital Art',
                description='Learn to create stunning digital artworks using industry-standard tools.',
                price=120,
                image_url='https://example.com/images/digital-art-course.jpg',
                category='Art',
                created_at=get_eat_now(),
                updated_at=get_eat_now()
            ),
            Course(
                instructor_id=users[3].id,  # David
                title='Advanced Photoshop Techniques',
                description='Master the art of photo editing with advanced techniques in Photoshop.',
                price=130,
                image_url='https://example.com/images/photoshop-course.jpg',
                category='Art',
                created_at=get_eat_now(),
                updated_at=get_eat_now()
            ),
            Course(
                instructor_id=users[1].id,  # Bob
                title='Web Development Bootcamp',
                description='Become a full-stack web developer with this intensive bootcamp.',
                price=200,
                image_url='https://example.com/images/web-development-course.jpg',
                category='Tech',
                created_at=get_eat_now(),
                updated_at=get_eat_now()
            ),
            Course(
                instructor_id=users[1].id,  # Bob
                title='Data Structures and Algorithms',
                description='An in-depth course on data structures and algorithms for software engineering.',
                price=150,
                image_url='https://bizanosa.com/wp-content/uploads/2017/11/29-Introduction-to-Programming-for-beginners.jpg',
                category='Tech',
                created_at=get_eat_now(),
                updated_at=get_eat_now()
            ),
            Course(
                instructor_id=users[2].id,  # Carol
                title='Healthy Cooking: Low-Carb Recipes',
                description='Learn how to cook delicious low-carb meals for a healthier lifestyle.',
                price=80,
                image_url='https://example.com/images/healthy-cooking-course.jpg',
                category='Cooking',
                created_at=get_eat_now(),
                updated_at=get_eat_now()
            ),
            Course(
                instructor_id=users[3].id,  # David
                title='Graphic Design Essentials',
                description='A beginner-friendly course on the fundamentals of graphic design.',
                price=90,
                image_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT7r7-DzV5UbLtY8Ls1URAmGFRcBkRJ6mfv0Q&s',
                category='Art',
                created_at=get_eat_now(),
                updated_at=get_eat_now()
            ),
        ]

        db.session.add_all(courses)
        db.session.commit()

        # Create real sample course content
        course_contents = [
            CourseContent(
                course_id=9,
                content_type='Video',
                content_url='coursecontent/4 Meals Anyone Can Make.mp4',
                created_at=get_eat_now(),
                updated_at=get_eat_now()
            ),
            CourseContent(
                course_id=courses[1].id,
                content_type='Text',
                content_url='https://example.com/texts/ai-introduction.pdf',
                created_at=get_eat_now(),
                updated_at=get_eat_now()
            ),
            CourseContent(
                course_id=courses[2].id,
                content_type='Video',
                content_url='https://example.com/videos/italian-cuisine.mp4',
                created_at=get_eat_now(),
                updated_at=get_eat_now()
            ),
            CourseContent(
                course_id=courses[3].id,
                content_type='Text',
                content_url='https://example.com/texts/baking-basics.pdf',
                created_at=get_eat_now(),
                updated_at=get_eat_now()
            ),
            CourseContent(
                course_id=courses[4].id,
                content_type='Video',
                content_url='https://example.com/videos/digital-art.mp4',
                created_at=get_eat_now(),
                updated_at=get_eat_now()
            ),
            CourseContent(
                course_id=courses[5].id,
                content_type='Text',
                content_url='https://example.com/texts/photoshop-advanced.pdf',
                created_at=get_eat_now(),
                updated_at=get_eat_now()
            ),
            CourseContent(
                course_id=courses[6].id,
                content_type='Video',
                content_url='https://example.com/videos/web-development.mp4',
                created_at=get_eat_now(),
                updated_at=get_eat_now()
            ),
            CourseContent(
                course_id=courses[7].id,
                content_type='Text',
                content_url='https://example.com/texts/data-structures.pdf',
                created_at=get_eat_now(),
                updated_at=get_eat_now()
            ),
            CourseContent(
                course_id=courses[8].id,
                content_type='Video',
                content_url='https://example.com/videos/healthy-cooking.mp4',
                created_at=get_eat_now(),
                updated_at=get_eat_now()
            ),
            CourseContent(
                course_id=courses[9].id,
                content_type='Video',
                content_url='https://youtu.be/SnxFkHqN1RA?feature=shared',
                created_at=get_eat_now(),
                updated_at=get_eat_now()
            ),
        ]

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

        print('Database seeded!')

if __name__ == '__main__':
    seed_database()
