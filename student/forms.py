from django import forms
from django.contrib.auth.models import User
from .models import StudentProfile, Appointment
from admin_app.models import Teacher

class StudentRegisterForm(forms.Form):  # ✅ CHANGED: Use Form, not ModelForm
    username = forms.CharField(max_length=150, required=True)
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=False)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password", required=True)
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password", required=True)
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists!")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if StudentProfile.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered!")
        return email
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

class StudentAppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['teacher', 'date', 'time_slot', 'purpose']
        widgets = {
            'teacher': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time_slot': forms.Select(choices=[
                ('10:00 AM', '10:00 AM'), ('11:00 AM', '11:00 AM'),
                ('2:00 PM', '2:00 PM'), ('3:00 PM', '3:00 PM'), ('4:00 PM', '4:00 PM'),
            ], attrs={'class': 'form-control'}),
            'purpose': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

class StudentApprovalForm(forms.ModelForm):  # ✅ For Admin use
    class Meta:
        model = StudentProfile
        fields = ['approved']
        widgets = {
            'approved': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
