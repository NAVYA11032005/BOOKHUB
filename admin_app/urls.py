from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_login, name='admin_login'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add-teacher/', views.add_teacher, name='add_teacher'),
    path('update-teacher/<int:pk>/', views.update_teacher, name='update_teacher'),
    path('delete-teacher/<int:pk>/', views.delete_teacher, name='delete_teacher'),
    path('approve-student/<int:pk>/', views.approve_student, name='approve_student'),

    path('reset-teacher-password/<int:pk>/', views.reset_teacher_password, name='reset_teacher_password'),
    path('logout/', views.admin_logout, name='admin_logout'),
]
