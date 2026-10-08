# 🎓 Student Management System

A Django web application to manage **students, teachers and courses** from one dashboard, with full CRUD, search, pagination, validation and an admin panel.

Built by **Roshan J** during the Python Full Stack Development course at Qspiders.

## Features
- Dashboard with live counts (students, teachers, courses, enrollments), recent students and a students-per-course bar chart
- Students: add, view, update, delete (with confirmation page), search by name / roll no / email
- Teachers and courses: add, edit, delete, search; each course is assigned to a teacher
- Automatic enrollment record created when a student is registered into a course
- Form validation (unique roll number / email, valid email, DOB must be in the past)
- Flash messages for every action, pagination (8 per page), responsive layout
- Django admin with search, filters and optimized queries

## Tech stack
Python 3 · Django 6 · SQLite · HTML5 · CSS3 (no external libraries)

## Data model
```
Teacher 1 ──< Course 1 ──< Student
                  │            │
                  └──< Enrollment >──┘   (unique student + course)
```

## Run locally
```bash
python -m venv venv
venv\Scripts\activate          # Windows   (Linux/Mac: source venv/bin/activate)
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser   # optional, for /admin
python manage.py runserver
```
Open http://127.0.0.1:8000/

Run tests: `python manage.py test`

## URL map
| URL | Purpose |
|---|---|
| `/` | Dashboard |
| `/students/`, `/students/add/`, `/students/<id>/`, `/students/<id>/edit/`, `/students/<id>/delete/` | Student CRUD |
| `/teachers/` + `add/`, `<id>/edit/`, `<id>/delete/` | Teacher CRUD |
| `/courses/` + `add/`, `<id>/edit/`, `<id>/delete/` | Course CRUD |
| `/about/`, `/admin/` | About page, admin panel |

## Project structure
```
Project_Django/
├── manage.py
├── Project_Django/        settings.py, urls.py
└── App_Django/
    ├── models.py  forms.py  views.py  admin.py  tests.py
    ├── migrations/
    ├── static/App_Django/ css/style.css, img/wallpaper.png
    └── templates/App_Django/  base, dashboard, lists, form, confirm_delete, about
```

## Production notes
Set environment variables `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=0`, `DJANGO_ALLOWED_HOSTS=yourdomain.com`.
