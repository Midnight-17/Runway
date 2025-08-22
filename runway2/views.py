from django.shortcuts import render, redirect
from django.http import JsonResponse
from datetime import datetime
from .models import Submission, TeacherProfile, StudentProfile, CustomUser
from .forms import StudentSignUpForm, TeacherSignUpForm
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.timezone import now as tz_now
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.urls import reverse_lazy
from django.conf import settings
from django.core.files.storage import FileSystemStorage


@ensure_csrf_cookie
def home(request):
    # Get today's date
    today = datetime.today().date()

    # Define the target date (November 2 of the current year)
    target_date = datetime(today.year, 11, 2).date()

    # Calculate the difference in days
    delta = (target_date - today).days

    # If target date has already passed this year, calculate days until Nov 2 next year
    if delta < 0:
        delta = 0

    return render(request, 'runway.html',{
        "Days_left": delta
    })

def upload_video(request):
    if request.method == "POST" and request.FILES.get("video"):
        video = request.FILES["video"]
        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        filename = fs.save(video.name, video)
        file_url = fs.url(filename)
        return JsonResponse({"video_url": file_url})
    return JsonResponse({"error": "No video uploaded"}, status=400)

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


class LoginView(DjangoLoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('runway2:homepage')

# Create your views here.
