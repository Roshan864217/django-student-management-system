from django.contrib import admin
from django.urls import path

from App_Django import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'),

    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.student_create, name='student_add'),
    path('students/<int:pk>/', views.student_detail, name='student_detail'),
    path('students/<int:pk>/edit/', views.student_update, name='student_edit'),
    path('students/<int:pk>/delete/', views.student_delete, name='student_delete'),

    path('teachers/', views.teacher_list, name='teacher_list'),
    path('teachers/add/', views.teacher_create, name='teacher_add'),
    path('teachers/<int:pk>/edit/', views.teacher_update, name='teacher_edit'),
    path('teachers/<int:pk>/delete/', views.teacher_delete, name='teacher_delete'),

    path('courses/', views.course_list, name='course_list'),
    path('courses/add/', views.course_create, name='course_add'),
    path('courses/<int:pk>/edit/', views.course_update, name='course_edit'),
    path('courses/<int:pk>/delete/', views.course_delete, name='course_delete'),

    path('about/', views.about, name='about'),
]
