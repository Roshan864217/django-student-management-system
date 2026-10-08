from datetime import date, timedelta

from django.test import TestCase
from django.urls import reverse

from .models import Course, Enrollment, Student, Teacher


class BaseData(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.teacher = Teacher.objects.create(name='Neeraj', subject_specification='Django', email='n@x.com')
        cls.course = Course.objects.create(name='Django', code='DJ1', teacher=cls.teacher)
        cls.student = Student.objects.create(
            name='Roshan', roll_number='101', email='r@x.com',
            date_of_birth=date(2004, 5, 17), course=cls.course)


class PageTests(BaseData):
    def test_all_list_pages_load(self):
        for name in ['dashboard', 'student_list', 'teacher_list', 'course_list', 'about', 'student_add',
                     'teacher_add', 'course_add']:
            self.assertEqual(self.client.get(reverse(name)).status_code, 200, name)

    def test_detail_404(self):
        self.assertEqual(self.client.get(reverse('student_detail', args=[999])).status_code, 404)

    def test_search(self):
        r = self.client.get(reverse('student_list'), {'q': 'Rosh'})
        self.assertContains(r, 'Roshan')
        r = self.client.get(reverse('student_list'), {'q': 'nobody'})
        self.assertContains(r, 'No students found')


class StudentCrudTests(BaseData):
    def test_create_also_enrolls(self):
        r = self.client.post(reverse('student_add'), {
            'name': 'Asha', 'roll_number': '102', 'email': 'a@x.com',
            'date_of_birth': '2005-01-01', 'course': self.course.pk})
        self.assertRedirects(r, reverse('student_list'))
        self.assertTrue(Enrollment.objects.filter(student__roll_number='102', course=self.course).exists())

    def test_duplicate_roll_number_rejected(self):
        r = self.client.post(reverse('student_add'), {
            'name': 'Dup', 'roll_number': '101', 'email': 'd@x.com',
            'date_of_birth': '2005-01-01', 'course': self.course.pk})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(Student.objects.count(), 1)

    def test_future_dob_rejected(self):
        future = (date.today() + timedelta(days=5)).isoformat()
        r = self.client.post(reverse('student_add'), {
            'name': 'F', 'roll_number': '103', 'email': 'f@x.com', 'date_of_birth': future})
        self.assertContains(r, 'must be in the past')

    def test_update(self):
        self.client.post(reverse('student_edit', args=[self.student.pk]), {
            'name': 'Roshan J', 'roll_number': '101', 'email': 'r@x.com',
            'date_of_birth': '2004-05-17', 'course': self.course.pk})
        self.student.refresh_from_db()
        self.assertEqual(self.student.name, 'Roshan J')

    def test_delete_requires_post(self):
        self.client.get(reverse('student_delete', args=[self.student.pk]))
        self.assertTrue(Student.objects.filter(pk=self.student.pk).exists())
        self.client.post(reverse('student_delete', args=[self.student.pk]))
        self.assertFalse(Student.objects.filter(pk=self.student.pk).exists())

    def test_deleting_teacher_keeps_course(self):
        self.teacher.delete()
        self.course.refresh_from_db()
        self.assertIsNone(self.course.teacher)


class CourseTeacherTests(BaseData):
    def test_course_without_teacher_allowed(self):
        r = self.client.post(reverse('course_add'), {'name': 'Java', 'code': 'J1', 'teacher': ''})
        self.assertRedirects(r, reverse('course_list'))
