from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField

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
        return self.user.username


class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.SET_NULL, null=True, related_name="students")
    exam_date = models.DateField(null=True, blank=True )

    def __str__(self):
        return f"{self.user.username}"
    

# Ok here we are making the lists for studnets, year completed progress and motnh completed progress 
class StudentProgress(models.Model):
    Student = models.OneToOneField(StudentProfile, on_delete=models.CASCADE)
    Year_Progress = models.JSONField( default=list, blank=True)
    Month_Progress = models.JSONField( default=list, blank=True)
    Video_Progress = models.JSONField(default=dict, blank=True) 
    last_reset = models.DateField(null=True, blank=True)   # <-- new field

    def __str__(self):
        return f"{self.Student}'s Progress" 



