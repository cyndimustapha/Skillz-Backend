# resources/__init__.py

from .instructor_resource import InstructorResource
from .learner_resource import LearnerResource
from .course_resource import CourseResource
from .course_content_resource import CourseContentResource
from .payment_resource import PaymentResource
from .enrollments_resource import EnrollmentResource
from .review_resource import ReviewResource
from .message_resource import MessageResource
from .accolade_resource import AccoladeResource

__all__ = [
    'InstructorResource',
    'LearnerResource',
    'CourseResource',
    'CourseContentResource',
    'PaymentResource',
    'EnrollmentResource',
    'ReviewResource',
    'MessageResource',
    'AccoladeResource'
]
