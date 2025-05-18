"""Django url patterns for space-themed web application are defined here."""

from django.urls import path

from astrocat import views

urlpatterns = [
    path("", views.main_page_view, name="home"),
    path("news/", views.main_page_view, name="news"),
    path("database/", views.data_page_view, name="database"),
    path("about/", views.about_view, name="about"),
    path("feedback/", views.feedback_view, name="feedback"),
    path(
        "space_object/<int:object_id>/",
        views.space_object_detail_view,
        name="space_object_info",
    ),
    path("user/<int:user_id>/", views.user_profile_view, name="user_profile"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("news/add/", views.add_news_view, name="add_news"),
    path("news/edit/<int:news_id>/", views.edit_news_view, name="edit_news"),
    path("news/delete/<int:news_id>/", views.delete_news_view, name="delete_news"),
    path("system/add/", views.add_system_view, name="add_system"),
    path("system/edit/<int:system_id>/", views.edit_system_view, name="edit_system"),
    path("system/delete/<int:system_id>/", views.delete_system_view, name="delete_system"),
    path(
        "system/<int:system_id>/object/add/",
        views.add_space_object_view,
        name="add_space_object",
    ),
    path(
        "space_object/edit/<int:object_id>/",
        views.edit_space_object_view,
        name="edit_space_object",
    ),
    path(
        "space_object/delete/<int:object_id>/",
        views.delete_space_object_view,
        name="delete_space_object",
    ),
    path("user/edit/<int:user_id>/", views.edit_user_view, name="edit_user"),
    path("download/", views.download_solar_system_view, name="download_file"),
]
