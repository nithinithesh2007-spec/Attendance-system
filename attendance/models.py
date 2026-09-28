from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    register_number = models.CharField(max_length=30, unique=True)
    email = models.EmailField(blank=True)
    department = models.CharField(max_length=100)
    year = models.IntegerField()

    def __str__(self):
        return f"{self.name} - {self.register_number}"

class Attendance(models.Model):
    STATUS_CHOICES = [
        ("Present", "Present"),
        ("Absent", "Absent"),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student", "date"],
                name="unique_student_attendance_date",
            )
        ]

    def __str__(self):
        return f"{self.student.name} - {self.date} - {self.status}"
