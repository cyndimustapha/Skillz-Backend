# resources/__init__.py

from .user import UserResource
from .course import CourseResource
from .course_content import CourseContentResource
#from .payment_resource import PaymentResource
#from .enrollments_resource import EnrollmentResource
#from .review_resource import ReviewResource
from .message_resource import MessageResource
#from .accolade_resource import AccoladeResource

__all__ = [
    'UserResource',
    'CourseResource',
    'CourseContentResource',
    # 'PaymentResource',
    # 'EnrollmentResource',
    #'ReviewResource',
    'MessageResource',
    #'AccoladeResource'
]
