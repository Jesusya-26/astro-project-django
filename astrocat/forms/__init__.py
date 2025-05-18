"""
Django forms for user registration, authentication, and space data input.

Includes:
- User registration and login forms
- News posting form
- Forms for creating and editing space systems and objects
"""

from .feedback import FeedbackForm
from .news import NewsForm
from .space_objects import SpaceObjectForm
from .space_systems import SpaceSystemForm
from .users import EditUserForm, LoginForm, RegisterForm

__all__ = [
    "FeedbackForm",
    "NewsForm",
    "SpaceObjectForm",
    "SpaceSystemForm",
    "EditUserForm",
    "LoginForm",
    "RegisterForm",
]
