from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("students/", views.students, name="students"),
    path("students/add/", views.add_student, name="add_student"),
    path("students/delete/<int:student_id>/", views.delete_student, name="delete_student"),
    path("attendance/", views.mark_attendance, name="mark_attendance"),
    path("report/", views.attendance_report, name="attendance_report"),
]
