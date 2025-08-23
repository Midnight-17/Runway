
from django.contrib import admin
from .models import CustomUser, StudentProfile, TeacherProfile, StudentProgress

# Register models so they show up in Django Admin
admin.site.register(CustomUser)
admin.site.register(StudentProfile)
admin.site.register(TeacherProfile)
admin.site.register(StudentProgress)


# Register your models here.
