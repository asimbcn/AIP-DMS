from django.urls import path
from . import views

urlpatterns = [
    path("", views.user_login, name="login"),
    path("register/", views.user_register, name="register"),
    path("redirect/", views.redir, name="redir"),
    path("logout", views.user_logout, name="logout"),
]