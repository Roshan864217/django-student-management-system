from django.db import models


class Teacher(models.Model):
    name = models.CharField(max_length=100)
    subject_specification = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    teacher = models.ForeignKey(
        Teacher, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='courses',
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.code})'


class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    course = models.ForeignKey(
        Course, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='students',
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name} - {self.roll_number}'


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-enrollment_date', '-id']
        constraints = [
            models.UniqueConstraint(fields=['student', 'course'], name='unique_student_course'),
        ]

    def __str__(self):
        return f'{self.student.name} -> {self.course.name}'
