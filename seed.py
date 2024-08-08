from faker import Faker
from models import db, User, Course, CourseContent, Payment, Enrollment, Review, Message, Accolade
from app import app
from datetime import datetime
import random


fake = Faker()

with app.app_context():

    print('Start seeding...')

    print("Deleting data...")
    User.query.delete()
    Course.query.delete()
    CourseContent.query.delete()
    Payment.query.delete()
    Enrollment.query.delete()
    Review.query.delete()
    Message.query.delete()
    Accolade.query.delete()

    print("Creating users...")


    images=["images/Anna.jpeg"]


    users = []

    for n in range(10):
        users.append(User(name=fake.name(), email=fake.email(), password='12345', profile_picture = fake.image_url(), bio=fake.paragraph(nb_sentences=5, variable_nb_sentences=False),role=random.choice(['instructor', 'learner']), verified=False))

    db.session.add_all(users)
    db.session.commit()

    print(users)
    
    # Anna = User(id="1", role="instructor", name="Anna Lisa", email="anna@gmail.com", password="8463456", bio="")