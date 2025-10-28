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
from django.contrib.auth.forms import AuthenticationForm
import hashlib


def Streak_Calculator_Month(m):
    n = 1 
    today = localtime(now()).date()
    month_day = today.day 
    if not m:
        return 0
    elif month_day not in m and (month_day-1) not in m:
        return 0 
    for s in reversed(m):
        if s-1 in m:
            n = n +1
        else:
            return n

def Streak_Calculator_Year(m):
    n = 1
    today = localtime(now()).date()
    year_day = today.timetuple().tm_yday  # <-- day of the year (1–365 or 366)
    if not m:
        return 0
    elif year_day not in m and (year_day - 1) not in m:
        return 0
    for s in reversed(m):
        if s - 1 in m:
            n = n + 1
        else:
            return n



today = localtime(now()).date()  # timezone-aware "current day"
month_day = today.day
year_day = today.timetuple().tm_yday



@ensure_csrf_cookie
def home(request, student_name):
    # Get today's date
    today = datetime.today().date()


    #define which days in the month are completed
    Student_profile = StudentProfile.objects.get(user__username = student_name)
    Student_Progress, created = StudentProgress.objects.get_or_create(Student=Student_profile)
    if not Student_profile.exam_date:
        Student_profile.exam_date = date.today()


   

    #erase the year progress every new year
    if (today.day == 1 and today.month == 1):
        Student_Progress.Year_Progress = []
        Student_Progress.save()

    #this is to erase teh month data every month
    if (Student_Progress.last_reset is None or
        Student_Progress.last_reset.month != today.month or
        Student_Progress.last_reset.year != today.year):
            Student_Progress.Month_Progress = []
            Student_Progress.Video_Progress = {}
            Student_Progress.last_reset = today
            Student_Progress.save()
    
 

    if request.method == "POST":
        exam_date = request.POST.get("exam_date")
        if exam_date:
            Student_profile.exam_date = exam_date
            Student_profile.save()
 #this is to send the template the exam date so that the java script can catch it
    exam_date_ = Student_profile.exam_date

    return render(request, 'runway.html',{
        "completions": json.dumps(Student_Progress.Month_Progress, cls=DjangoJSONEncoder),
        "student_name": student_name,
        "exam_date": exam_date_
    })


def upload_video(request, student_name):
    if request.method == "POST" and request.FILES.get("video"):
        today = localtime(now()).date()
        month_day = today.day
        year_day = today.timetuple().tm_yday

        # Get student data
        Student_profile = StudentProfile.objects.get(user__username=student_name)
        Student_Progress, created = StudentProgress.objects.get_or_create(Student=Student_profile)
        video = request.FILES["video"]

        # --- Compute SHA256 hash ---
        hasher = hashlib.sha256()
        for chunk in video.chunks():
            hasher.update(chunk)
        video_hash = hasher.hexdigest()

        # --- Check for duplicates ---
        hash_list = Student_Progress.Video_Hashes
        if video_hash in hash_list:
            return redirect('runway2:homepage', student_name=student_name)

        # --- Save video ---
        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        filename = fs.save(video.name, video)
        file_url = fs.url(filename)

        # --- Update progress data ---
        Student_Progress.Month_Progress.append(month_day)
        Student_Progress.Year_Progress.append(year_day)
        Student_Progress.Video_Progress[str(month_day)] = file_url

        # --- Store video hash ---
        hash_list.append(video_hash)
        Student_Progress.Video_Hashes = hash_list

        Student_Progress.save()

        # --- Return JSON response ---
        return JsonResponse({
            "video_url": file_url,
            "Month_Progress": Student_Progress.Month_Progress,
            "Year_Progress": Student_Progress.Year_Progress,
            "Video_Progress": Student_Progress.Video_Progress
        })

def get_month_progress(request, student_name):
    # Get the logged-in student profile
    Student_ = StudentProfile.objects.get( user__username = student_name)
    Progress, created = StudentProgress.objects.get_or_create(Student = Student_)
    Monthly_Progress = Progress.Month_Progress
    Yearly_Progress = Progress.Year_Progress
    Video_Progress = Progress.Video_Progress
    Month_Streak = Streak_Calculator_Month(Monthly_Progress)
    Year_Streak = Streak_Calculator_Year(Yearly_Progress)

    # Return JSON with Month_Progress
    return JsonResponse({
        "completions": Monthly_Progress,  # e.g., [1, 5, 7]
        "Video_Progress" : Video_Progress,
        "Month_Streak":Month_Streak,
        "Year_Streak":Year_Streak
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


# views.py


def Login(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            # Log the user in
            from django.contrib.auth import login
            user = form.get_user()
            login(request, user)
            student_name = user.username
            return redirect('runway2:homepage' , student_name = student_name)  # or any page you want
    return render(request, "login.html", {"form": form})


    


def teacher_(request , teacher_name):
    teacher = TeacherProfile.objects.get(user__username = teacher_name)
    students = teacher.students.all()
    default_student = students[0]
    default_student_profile = StudentProfile.objects.get(user__username = default_student)
    exam_date_ = default_student_profile.exam_date
    exam_dates = {}
    for s in students:
        profile = StudentProfile.objects.get(user__username = s)
        name = s.user.username
        exam_dates[name] = profile.exam_date.strftime("%Y-%m-%d") if profile.exam_date else None
    exam_dates_json = json.dumps(exam_dates)
    return render(request, "teacher.html", {
        "teacher": teacher.user,
        "student_name": default_student,
        "students": students,
        "exam_date": exam_date_,
        "exam_dates": exam_dates_json,
    })



def teacher( request, teacher_name, student_name):
    teacher = TeacherProfile.objects.get(user__username = teacher_name)
    student = StudentProfile.objects.get(user__username = student_name)
    students = teacher.students.all()
    return render(request,"teacher.html", {
        "teacher":teacher.user,
        "student_name":student.user,
        "students" : students
    })


def welcome(request):
    return render(request, "welcome.html")


# Create your views here.
