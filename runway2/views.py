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

@require_POST
def upload_submission(request):
    file = request.FILES.get('file')
    if not file:
        return JsonResponse({"error": "No file provided"}, status=400)

    date_str = request.POST.get('date')
    try:
        if date_str:
            date_val = datetime.fromisoformat(date_str).date()
        else:
            date_val = tz_now().date()
    except ValueError:
        return JsonResponse({"error": "Invalid date format; expected YYYY-MM-DD"}, status=400)

    sub = Submission.objects.create(file=file, date=date_val)
    return JsonResponse({
        "ok": True,
        "date": date_val.isoformat(),
        "file_url": sub.file.url,
        "id": sub.id,
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


class LoginView(DjangoLoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('runway2:homepage')

# Create your views here.
