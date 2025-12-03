from django.urls import path
from . import views

urlpatterns = [
    path('', views.teacher_login, name='teacher_login'),
    path('dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('appointment/<int:pk>/', views.manage_appointment, name='manage_appointment'),
    path('logout/', views.teacher_logout, name='teacher_logout'),
     path('register/', views.teacher_register, name='teacher_register'),  # ADD
]
