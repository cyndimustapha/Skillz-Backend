from faker import Faker
from models import db, User, Course, CourseContent, Payment, Enrollment, Review, Message, Accolade
from app import app
from datetime import datetime
import random

random.seed(1)
fake = Faker()

with app.app_context():

    print('Start seeding...')

    # Clear existing data
    print("Deleting data...")
    User.query.delete()
    Course.query.delete()
    CourseContent.query.delete()
    Payment.query.delete()
    Enrollment.query.delete()
    Review.query.delete()
    Message.query.delete()
    Accolade.query.delete()

    # Create users
    print("Creating users...")
    users = []
    for n in range(10):
        role = random.choice(['instructor', 'learner'])
        user = User(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            password='12345',
            profile_picture=fake.image_url(),
            bio=fake.paragraph(nb_sentences=5, variable_nb_sentences=False),
            role=role,
            verified=False
        )
        users.append(user)

    db.session.add_all(users)
    db.session.commit()

    # Print created users
    print("Users created:")
    for user in users:
        print(user)

    # Identify instructors
    instructors = [user for user in users if user.role == "instructor"]
    print("Instructors identified:")
    for instructor in instructors:
        print(instructor.name)

    # Create courses
    print("Creating courses...")
    courses = []
    for n in range(7):
        # Randomly assign an instructor to each course
        instructor = random.choice(instructors) if instructors else None
        course = Course(
            title=fake.sentence(nb_words=4),
            description=fake.paragraph(nb_sentences=3, variable_nb_sentences=False),
            instructor_id=instructor.id if instructor else None,
            price=random.randint(3000,5000)
            
        )
        courses.append(course)

    db.session.add_all(courses)
    db.session.commit()

    # Print created courses
    print("Courses created:")
    for course in courses:
        print(course)



    #Creating course content
    print("Creating course content...")
    course_contents = []
    for n in range(20):
        course_ids = [course.id for course in courses]
        chosen_course_id=random.choices(course_ids, weights=None, k=1)
        course_content = CourseContent(
            course_id=chosen_course_id[0],
            content_type=random.choice(['video','text']),
            content_url=fake.uri(),
            
        )
        course_contents.append(course_content)

    db.session.add_all(course_content)
    db.session.commit()



    # #Creating enrollments
    # print("Creating enrollments")
    # enrollments=[]
    # for n in range(6):
    #     course_ids = [course.id for course in courses]
    #     chosen_course_id=random.choices(course_ids, weights=None, k=1)
    #     learners_ids= [user.id for user in users if user.role == 'learner']