from django.contrib import admin

from .models import Course, Enrollment, Student, Teacher


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject_specification', 'email']
    search_fields = ['name', 'email', 'subject_specification']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'teacher']
    search_fields = ['name', 'code']
    list_filter = ['teacher']
    list_select_related = ['teacher']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'roll_number', 'email', 'date_of_birth', 'course']
    search_fields = ['name', 'roll_number', 'email']
    list_filter = ['course']
    list_select_related = ['course']


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'enrollment_date']
    list_filter = ['course']
    search_fields = ['student__name', 'course__name']
    list_select_related = ['student', 'course']
