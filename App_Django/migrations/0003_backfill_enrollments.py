from django.db import migrations


def backfill(apps, schema_editor):
    """Create an Enrollment row for every existing student that already has a course."""
    Student = apps.get_model('App_Django', 'Student')
    Enrollment = apps.get_model('App_Django', 'Enrollment')
    for s in Student.objects.exclude(course__isnull=True):
        Enrollment.objects.get_or_create(student=s, course_id=s.course_id)


class Migration(migrations.Migration):
    dependencies = [('App_Django', '0002_model_cleanup')]
    operations = [migrations.RunPython(backfill, migrations.RunPython.noop)]
