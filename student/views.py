from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, login as auth_login
from django.contrib.auth.models import User  # ✅ ADDED User import
from django.contrib.auth.decorators import login_required
from .models import StudentProfile, Appointment
from .forms import StudentRegisterForm, StudentAppointmentForm
from admin_app.models import Teacher  # ✅ Only Teacher needed

def student_register(request):
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            # Create User first
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = User.objects.create_user(
                username=username, 
                email=form.cleaned_data['email'],
                password=password
            )
            
            # Create StudentProfile (pending approval)
            StudentProfile.objects.create(
                user=user,
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data.get('phone', '')
            )
            messages.success(request, 'Registration successful! Waiting for admin approval.')
            return redirect('student_login')
    else:
        form = StudentRegisterForm()
    return render(request, 'student/register.html', {'form': form})

def student_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            try:
                student = StudentProfile.objects.get(user=user)
                if student.approved:
                    auth_login(request, user)
                    return redirect('student_dashboard')
                else:
                    messages.error(request, 'Your account is pending admin approval!')
            except StudentProfile.DoesNotExist:
                messages.error(request, 'Please register first or contact admin!')
        else:
            messages.error(request, 'Invalid credentials!')
    return render(request, 'student/login.html')

@login_required(login_url='student_login')
def student_dashboard(request):
    try:
        student = StudentProfile.objects.get(user=request.user)
    except StudentProfile.DoesNotExist:
        messages.error(request, 'Student profile not found. Please register first.')
        return redirect('student_register')

    appointments = Appointment.objects.filter(student=student)
    teachers = Teacher.objects.all()
    return render(request, 'student/dashboard.html', {
        'student': student,
        'appointments': appointments,
        'teachers': teachers
    })

@login_required(login_url='student_login')
def book_appointment(request):
    try:
        student = StudentProfile.objects.get(user=request.user)
    except StudentProfile.DoesNotExist:
        messages.error(request, 'Student profile not found. Please register first.')
        return redirect('student_register')
    if request.method == 'POST':
        form = StudentAppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.student = student
            appointment.save()
            messages.success(request, 'Appointment booked! Waiting for teacher approval.')
            return redirect('student_dashboard')
    else:
        form = StudentAppointmentForm()
    return render(request, 'student/book_appointment.html', {'form': form})

def student_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('/')
