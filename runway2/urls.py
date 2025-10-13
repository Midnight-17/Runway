from django.urls import path
from . import views

app_name = 'runway2'

urlpatterns = [
    path('', views.home, name='home'),
    path('homepage/<str:student_name>', views.home, name='homepage'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.Login, name='login'),
    path("upload-video/<str:student_name>", views.upload_video, name="upload_video"),
    path("monthly-progress/<str:student_name>", views.get_month_progress, name="monthly_progress"),
    path("teacher/<str:teacher_name>/<str:student_name>", views.teacher , name="teacher"),
    path("teacher/<str:teacher_name>", views.teacher_, name="teacher_"),
    path("welcome/", views.welcome, name="welcome")
]
