from datetime import date

from django import forms

from .models import Course, Enrollment, Student, Teacher


class StyledModelForm(forms.ModelForm):
    """Adds the shared CSS class to every widget."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')


class TeacherForm(StyledModelForm):
    class Meta:
        model = Teacher
        fields = ['name', 'subject_specification', 'email']


class CourseForm(StyledModelForm):
    class Meta:
        model = Course
        fields = ['name', 'code', 'teacher']


class StudentForm(StyledModelForm):
    class Meta:
        model = Student
        fields = ['name', 'roll_number', 'email', 'date_of_birth', 'course']
        widgets = {'date_of_birth': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')}

    def clean_date_of_birth(self):
        dob = self.cleaned_data['date_of_birth']
        if dob >= date.today():
            raise forms.ValidationError('Date of birth must be in the past.')
        return dob

    def save(self, commit=True):
        student = super().save(commit=commit)
        if commit and student.course_id:
            Enrollment.objects.get_or_create(student=student, course=student.course)
        return student
