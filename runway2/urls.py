from django.urls import path
from . import views

app_name = 'runway2'

urlpatterns = [
    path('', views.home, name='home'),
    path('homepage/', views.home, name='homepage'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path("upload-video/", views.upload_video, name="upload_video"),
    path("monthly-progress/", views.get_month_progress, name="monthly_progress")
]
