"""
Django views for a space-themed web application.

This module includes views for:
- User authentication and profile management
- News creation, editing, and display
- User-submitted feedback and about page
- Space systems and celestial object management
- Main page and data visualization
"""

from .feedback import about_view, feedback_view
from .news import add_news_view, delete_news_view, edit_news_view, main_page_view
from .space_objects import (
    add_space_object_view,
    delete_space_object_view,
    edit_space_object_view,
    space_object_detail_view,
)
from .space_systems import (
    add_system_view,
    data_page_view,
    delete_system_view,
    download_solar_system_view,
    edit_system_view,
)
from .users import (
    edit_user_view,
    login_view,
    logout_view,
    register_view,
    user_profile_view,
)

__all__ = [
    "about_view",
    "feedback_view",
    "add_news_view",
    "delete_news_view",
    "edit_news_view",
    "main_page_view",
    "add_space_object_view",
    "edit_space_object_view",
    "delete_space_object_view",
    "space_object_detail_view",
    "add_system_view",
    "data_page_view",
    "delete_system_view",
    "download_solar_system_view",
    "edit_system_view",
    "edit_user_view",
    "login_view",
    "logout_view",
    "register_view",
    "user_profile_view",
]
