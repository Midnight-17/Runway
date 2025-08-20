from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Submission(models.Model):
    file = models.FileField(upload_to='videos/')
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Submission {self.date} - {self.file.name}"


# --- Auth models for Teachers and Students ---
class CustomUser(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)


class TeacherProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"TeacherProfile({self.user.username})"


class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"StudentProfile({self.user.username}) -> {self.teacher}"
