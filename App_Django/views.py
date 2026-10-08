from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CourseForm, StudentForm, TeacherForm
from .models import Course, Enrollment, Student, Teacher

PAGE_SIZE = 8


def paginate(request, queryset):
    return Paginator(queryset, PAGE_SIZE).get_page(request.GET.get('page'))


# ---------- Dashboard ----------
def dashboard(request):
    context = {
        'student_count': Student.objects.count(),
        'teacher_count': Teacher.objects.count(),
        'course_count': Course.objects.count(),
        'enrollment_count': Enrollment.objects.count(),
        'recent_students': Student.objects.select_related('course').order_by('-id')[:5],
        'course_stats': Course.objects.annotate(total=Count('students')).order_by('-total')[:5],
    }
    return render(request, 'App_Django/dashboard.html', context)


# ---------- Students ----------
def student_list(request):
    q = request.GET.get('q', '').strip()
    students = Student.objects.select_related('course')
    if q:
        students = students.filter(
            Q(name__icontains=q) | Q(roll_number__icontains=q) | Q(email__icontains=q)
        )
    return render(request, 'App_Django/student_list.html',
                  {'page': paginate(request, students), 'q': q})


def student_detail(request, pk):
    student = get_object_or_404(Student.objects.select_related('course__teacher'), pk=pk)
    return render(request, 'App_Django/student_detail.html', {'student': student})


def student_create(request):
    form = StudentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        student = form.save()
        messages.success(request, f'Student "{student.name}" added successfully.')
        return redirect('student_list')
    return render(request, 'App_Django/form.html', {'form': form, 'title': 'Add Student'})


def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = StudentForm(request.POST or None, instance=student)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'Student "{student.name}" updated successfully.')
        return redirect('student_detail', pk=pk)
    return render(request, 'App_Django/form.html', {'form': form, 'title': 'Update Student'})


def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        messages.success(request, f'Student "{student.name}" deleted.')
        return redirect('student_list')
    return render(request, 'App_Django/confirm_delete.html',
                  {'object': student, 'kind': 'student', 'cancel_url': 'student_detail'})


# ---------- Teachers ----------
def teacher_list(request):
    q = request.GET.get('q', '').strip()
    teachers = Teacher.objects.annotate(course_total=Count('courses')).order_by('name')
    if q:
        teachers = teachers.filter(Q(name__icontains=q) | Q(subject_specification__icontains=q))
    return render(request, 'App_Django/teacher_list.html',
                  {'page': paginate(request, teachers), 'q': q})


def teacher_create(request):
    form = TeacherForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        teacher = form.save()
        messages.success(request, f'Teacher "{teacher.name}" added successfully.')
        return redirect('teacher_list')
    return render(request, 'App_Django/form.html', {'form': form, 'title': 'Add Teacher'})


def teacher_update(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    form = TeacherForm(request.POST or None, instance=teacher)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'Teacher "{teacher.name}" updated.')
        return redirect('teacher_list')
    return render(request, 'App_Django/form.html', {'form': form, 'title': 'Update Teacher'})


def teacher_delete(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        teacher.delete()
        messages.success(request, f'Teacher "{teacher.name}" deleted.')
        return redirect('teacher_list')
    return render(request, 'App_Django/confirm_delete.html',
                  {'object': teacher, 'kind': 'teacher', 'cancel_url': 'teacher_list'})


# ---------- Courses ----------
def course_list(request):
    q = request.GET.get('q', '').strip()
    courses = Course.objects.select_related('teacher').annotate(student_total=Count('students')).order_by('name')
    if q:
        courses = courses.filter(Q(name__icontains=q) | Q(code__icontains=q))
    return render(request, 'App_Django/course_list.html',
                  {'page': paginate(request, courses), 'q': q})


def course_create(request):
    form = CourseForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        course = form.save()
        messages.success(request, f'Course "{course.name}" added successfully.')
        return redirect('course_list')
    return render(request, 'App_Django/form.html', {'form': form, 'title': 'Add Course'})


def course_update(request, pk):
    course = get_object_or_404(Course, pk=pk)
    form = CourseForm(request.POST or None, instance=course)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'Course "{course.name}" updated.')
        return redirect('course_list')
    return render(request, 'App_Django/form.html', {'form': form, 'title': 'Update Course'})


def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        messages.success(request, f'Course "{course.name}" deleted.')
        return redirect('course_list')
    return render(request, 'App_Django/confirm_delete.html',
                  {'object': course, 'kind': 'course', 'cancel_url': 'course_list'})


def about(request):
    return render(request, 'App_Django/about.html')
