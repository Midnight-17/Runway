from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class StudentSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    teacher_code = forms.CharField(required=True, label="Teacher Code")

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'teacher_code']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove default help texts for username and passwords
        if 'username' in self.fields:
            self.fields['username'].help_text = ''
        if 'password1' in self.fields:
            self.fields['password1'].help_text = ''
        if 'password2' in self.fields:
            self.fields['password2'].help_text = ''

class TeacherSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove default help texts for username and passwords
        if 'username' in self.fields:
            self.fields['username'].help_text = ''
        if 'password1' in self.fields:
            self.fields['password1'].help_text = ''
        if 'password2' in self.fields:
            self.fields['password2'].help_text = ''
