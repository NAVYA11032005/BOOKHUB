from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import TeacherProfile, TeacherMessage
from .forms import AppointmentActionForm
from student.models import Appointment
from admin_app.models import Teacher as AdminTeacher

def teacher_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            try:
                teacher_profile = TeacherProfile.objects.get(user=user)
                auth_login(request, user)
                return redirect('teacher_dashboard')
            except TeacherProfile.DoesNotExist:
                messages.error(request, 'Teacher account not found!')
        else:
            messages.error(request, 'Invalid credentials!')
    return render(request, 'teacher/login.html')

@login_required(login_url='teacher_login')
def teacher_dashboard(request):
    try:
        teacher_profile = TeacherProfile.objects.get(user=request.user)
    except TeacherProfile.DoesNotExist:
        return redirect('teacher_login')
    
    appointments = Appointment.objects.filter(teacher=teacher_profile.teacher)
    messages = TeacherMessage.objects.filter(teacher=teacher_profile).order_by('-created_at')
    
    return render(request, 'teacher/dashboard.html', {
        'teacher': teacher_profile,
        'appointments': appointments,
        'messages': messages,
        'pending_count': appointments.filter(status='pending').count(),
        'approved_count': appointments.filter(status='approved').count()
    })

@login_required(login_url='teacher_login')
def manage_appointment(request, pk):
    teacher_profile = TeacherProfile.objects.get(user=request.user)
    appointment = get_object_or_404(Appointment, pk=pk, teacher=teacher_profile.teacher)
    
    if request.method == 'POST':
        form = AppointmentActionForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, f'Appointment {appointment.status} successfully!')
            return redirect('teacher_dashboard')
    else:
        form = AppointmentActionForm(instance=appointment)
    
    return render(request, 'teacher/manage_appointment.html', {
        'form': form,
        'appointment': appointment,
        'teacher': teacher_profile
    })

def teacher_logout(request):
    logout(request)
    return redirect('/')
