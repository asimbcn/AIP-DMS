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
    path("add_logs/", views.add_logs, name="add_logs"),
    path("user_info/", views.user_info, name="user_info"),
    path("change_status/<str:pk>/<str:reason>", views.change_status, name="change_status"),
    path("restrict/<str:pk>", views.restrict, name="restrict"),
    path("active_change/<str:pk>", views.active_change, name="active_change"),
    path("file/<str:pk>/<str:type>", views.view_file, name="view"),
    path("change_group/<str:pk>/<str:type>", views.change_group, name="change_group"),
    path("download/<str:pk>/<str:type>", views.download, name="download"),
    path("edit_file/<str:pk>/<str:type>", views.edit_file, name="edit_file"),
] 


