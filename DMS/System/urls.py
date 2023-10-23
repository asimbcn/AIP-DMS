from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("shared/", views.for_me, name="shared"),
    path("upload/", views.upload_files, name="upload"),
    path("edit", views.edit_profile, name="edit"),
    path("statistics/", views.stats, name="stats"),
    path("search/", views.search, name="search"),
    path("logs/", views.sec_log, name="logs"),
    path("file/<str:pk>/<str:type>", views.view_file, name="view"),
] 


