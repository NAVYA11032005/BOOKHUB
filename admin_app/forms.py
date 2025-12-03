from django import forms
from .models import Teacher, PendingStudent

from django import forms
from django.contrib.auth.models import User
from .models import Teacher

class TeacherForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True, help_text="Teacher's login username")
    password = forms.CharField(widget=forms.PasswordInput, required=True, help_text="Teacher's login password")
    
    class Meta:
        model = Teacher
        fields = ['name', 'department', 'subject', 'email', 'phone', 'username', 'password']
    
    def save(self, commit=True):
        # Create User first
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        
        # Create Teacher record
        teacher = super().save(commit=False)
        teacher.save()
        
        # Link TeacherProfile
        from teacher.models import TeacherProfile
        TeacherProfile.objects.get_or_create(user=user, teacher=teacher)
        
        return teacher

class StudentApprovalForm(forms.ModelForm):
    class Meta:
        model = PendingStudent
        fields = ['approved']
