from django.shortcuts import render, redirect
from django.http import JsonResponse
from datetime import datetime, date
from .models import Submission, TeacherProfile, StudentProfile, CustomUser, StudentProgress
from .forms import StudentSignUpForm, TeacherSignUpForm
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.timezone import now as tz_now
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.urls import reverse_lazy
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.timezone import localtime, now

today = localtime(now()).date()  # timezone-aware "current day"
month_day = today.day
year_day = today.timetuple().tm_yday



@ensure_csrf_cookie
def home(request, student_name):
    # Get today's date
    today = datetime.today().date()

    # Define the target date (November 2 of the current year)
    target_date = datetime(today.year, 11, 2).date()

    # Calculate the difference in days
    delta = (target_date - today).days

    #define which days in the month are completed
    Student_profile = StudentProfile.objects.get(user__username = student_name)
    Student_Progress, created = StudentProgress.objects.get_or_create(Student=Student_profile)
    
    # If target date has already passed this year, calculate days until Nov 2 next year
    if delta < 0:
        delta = 0

    return render(request, 'runway.html',{
        "Days_left": delta,
        "completions": json.dumps(Student_Progress.Month_Progress, cls=DjangoJSONEncoder),
        "student_name": student_name
    })

def upload_video(request, student_name):
    if request.method == "POST" and request.FILES.get("video"):
        # ok these are the steps that we are going to use to actually use to append to the lists
        today = localtime(now()).date()
        month_day = today.day
        year_day = today.timetuple().tm_yday


        Student_profile = StudentProfile.objects.get( user__username = student_name )
        Student_Progress, created  = StudentProgress.objects.get_or_create(Student = Student_profile)
        Student_Progress.Month_Progress.append(month_day)
        Student_Progress.Year_Progress.append(year_day)
        video = request.FILES["video"]
        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        filename = fs.save(video.name, video)
        file_url = fs.url(filename)
        Student_Progress.Video_Progress[str(month_day)] = file_url

       
        Student_Progress.save()



        
        return JsonResponse({
                "video_url": file_url,
                "Month_Progress" : Student_Progress.Month_Progress,
                "Year_Progress":Student_Progress.Year_Progress,
                "Video_Progress": Student_Progress.Video_Progress
                             })

    return JsonResponse({"error": "No video uploaded"}, status=400)

def get_month_progress(request, student_name):
    # Get the logged-in student profile
    Student_ = StudentProfile.objects.get( user__username = student_name)
    Progress, created = StudentProgress.objects.get_or_create(Student = Student_)
    Monthly_Progress = Progress.Month_Progress
    Video_Progress = Progress.Video_Progress

    # Return JSON with Month_Progress
    return JsonResponse({
        "completions": Monthly_Progress,  # e.g., [1, 5, 7]
        "Video_Progress" : Video_Progress
    })



# --- Signup view (teachers and students) ---
def signup_view(request):
    if request.method == 'POST':
        if 'student_submit' in request.POST:
            student_form = StudentSignUpForm(request.POST)
            teacher_form = TeacherSignUpForm()
            if student_form.is_valid():
                teacher_code = student_form.cleaned_data.get('teacher_code')
                try:
                    teacher_user = CustomUser.objects.get(username=teacher_code, is_teacher=True)
                    teacher_profile = TeacherProfile.objects.get(user=teacher_user)
                except ObjectDoesNotExist:
                    student_form.add_error('teacher_code', 'Invalid teacher code')
                    return render(request, 'login_signup.html', {'student_form': student_form, 'teacher_form': teacher_form})

                user = student_form.save(commit=False)
                user.is_student = True
                user.save()
                StudentProfile.objects.create(user=user, teacher=teacher_profile)
                # After successful signup, redirect to login page
                return redirect('runway2:login')

        elif 'teacher_submit' in request.POST:
            teacher_form = TeacherSignUpForm(request.POST)
            student_form = StudentSignUpForm()
            if teacher_form.is_valid():
                user = teacher_form.save(commit=False)
                user.is_teacher = True
                user.save()
                TeacherProfile.objects.create(user=user)
                # After successful signup, redirect to login page
                return redirect('runway2:login')
    else:
        student_form = StudentSignUpForm()
        teacher_form = TeacherSignUpForm()

    return render(request, 'login_signup.html', {'student_form': student_form, 'teacher_form': teacher_form})


def Login(request):
    return render(request, "login.html")

    


def teacher_(request , teacher_name):
    teacher = TeacherProfile.objects.get(user__username = teacher_name)
    students = teacher.students.all()
    default_student = students[0]
    return redirect("runway2:teacher", teacher_name = teacher, student_name = default_student)


def teacher( request, teacher_name, student_name):
    teacher = TeacherProfile.objects.get(user__username = teacher_name)
    student = StudentProfile.objects.get(user__username = student_name)
    students = teacher.students.all
    return render(request,"teacher.html", {
        "teacher":teacher.user,
        "student_name":student.user,
        "students" : students
    })


# Create your views here.
