from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("shared/", views.for_me, name="shared"),
    path("upload/", views.upload_files, name="upload"),
] 


