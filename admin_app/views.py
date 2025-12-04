from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Teacher
from .forms import TeacherForm
from student.models import StudentProfile
from teacher.models import TeacherProfile

def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('admin_dashboard')
        messages.error(request, 'Invalid credentials or not an admin!')
    return render(request, 'admin_app/login.html')

@login_required
def admin_dashboard(request):
    teachers = Teacher.objects.all()
    pending_students = StudentProfile.objects.filter(approved=False)
    
    # ✅ PERFECT: Single list of dicts - NO template filters needed!
    teacher_data = []
    active_teachers_count = 0
    
    for teacher in teachers:
        try:
            profile = TeacherProfile.objects.get(teacher=teacher)
            teacher_data.append({
                'teacher': teacher,
                'has_profile': True,
                'username': profile.user.username,
                'can_login': True
            })
            active_teachers_count += 1
        except TeacherProfile.DoesNotExist:
            teacher_data.append({
                'teacher': teacher,
                'has_profile': False,
                'username': None,
                'can_login': False
            })
    
    return render(request, 'admin_app/dashboard.html', {
        'teacher_data': teacher_data,
        'active_teachers': active_teachers_count,
        'pending_students': pending_students,
        'pending_count': pending_students.count()
    })

@login_required
def add_teacher(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            teacher = form.save()
            messages.success(request, f'Teacher "{teacher.name}" added successfully!')
            return redirect('admin_dashboard')
    else:
        form = TeacherForm()
    return render(request, 'admin_app/add_teacher.html', {'form': form})

@login_required
def update_teacher(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            messages.success(request, f'Teacher "{teacher.name}" updated!')
            return redirect('admin_dashboard')
    else:
        form = TeacherForm(instance=teacher)
    return render(request, 'admin_app/update_teacher.html', {'form': form, 'teacher': teacher})

@login_required
def delete_teacher(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        teacher_name = teacher.name
        teacher.delete()
        try:
            profile = TeacherProfile.objects.get(teacher=teacher)
            profile.delete()
        except:
            pass
        messages.success(request, f'Teacher "{teacher_name}" deleted!')
        return redirect('admin_dashboard')
    return render(request, 'admin_app/delete_teacher.html', {'teacher': teacher})

@login_required
def approve_student(request, pk):
    student = get_object_or_404(StudentProfile, pk=pk)
    if request.method == 'POST':
        student.approved = True
        student.save()
        messages.success(request, f'Student "{student.name}" approved!')
        return redirect('admin_dashboard')
    return render(request, 'admin_app/approve_student.html', {'student': student})


@login_required
def reset_teacher_password(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    try:
        profile = TeacherProfile.objects.get(teacher=teacher)
        user = profile.user
        new_password = 'Welcome123!'
        user.set_password(new_password)
        user.save()
        messages.success(request, f'Password reset for "{teacher.name}": {new_password}')
    except TeacherProfile.DoesNotExist:
        messages.error(request, f'No login account found for "{teacher.name}"')
    return redirect('admin_dashboard')

def admin_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('/')
