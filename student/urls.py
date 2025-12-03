from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_login, name='student_login'),
    path('register/', views.student_register, name='student_register'),
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('book/', views.book_appointment, name='book_appointment'),
    path('logout/', views.student_logout, name='student_logout'),
]
