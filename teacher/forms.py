from django import forms
from student.models import Appointment

class AppointmentActionForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['status']
        widgets = {
            'status': forms.Select(choices=[
                ('pending', 'Pending'),
                ('approved', 'Approved'),
                ('cancelled', 'Cancelled'),
            ], attrs={'class': 'form-control'})
        }
