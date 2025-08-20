from django.urls import path
from . import views

app_name = 'runway2'

urlpatterns = [
    path('', views.home, name='home'),
    path('homepage/', views.home, name='homepage'),
    path('api/submit/', views.upload_submission, name='upload_submission'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
]
