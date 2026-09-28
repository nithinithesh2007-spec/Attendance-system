from datetime import date
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from .models import Student, Attendance

def home(request):
    today = date.today()
    context = {
        "total_students": Student.objects.count(),
        "present_today": Attendance.objects.filter(date=today, status="Present").count(),
        "absent_today": Attendance.objects.filter(date=today, status="Absent").count(),
    }
    return render(request, "attendance/home.html", context)

def students(request):
    return render(
        request,
        "attendance/students.html",
        {"students": Student.objects.all().order_by("register_number")},
    )

def add_student(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        register_number = request.POST.get("register_number", "").strip()
        email = request.POST.get("email", "").strip()
        department = request.POST.get("department", "").strip()
        year = request.POST.get("year", "").strip()

        if Student.objects.filter(register_number=register_number).exists():
            messages.error(request, "Register number already exists.")
            return redirect("add_student")

        Student.objects.create(
            name=name,
            register_number=register_number,
            email=email,
            department=department,
            year=year,
        )
        messages.success(request, "Student added successfully.")
        return redirect("students")

    return render(request, "attendance/add_student.html")

def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    student.delete()
    messages.success(request, "Student deleted successfully.")
    return redirect("students")

def mark_attendance(request):
    student_list = Student.objects.all().order_by("register_number")
    selected_date = request.POST.get("date", str(date.today()))

    if request.method == "POST":
        attendance_date = request.POST.get("date")
        for student in student_list:
            status = request.POST.get(f"status_{student.id}")
            if status in {"Present", "Absent"}:
                Attendance.objects.update_or_create(
                    student=student,
                    date=attendance_date,
                    defaults={"status": status},
                )
        messages.success(request, "Attendance saved successfully.")
        return redirect("mark_attendance")

    return render(
        request,
        "attendance/mark_attendance.html",
        {"students": student_list, "selected_date": selected_date},
    )

def attendance_report(request):
    report = []
    for student in Student.objects.all().order_by("register_number"):
        records = Attendance.objects.filter(student=student)
        total = records.count()
        present = records.filter(status="Present").count()
        absent = records.filter(status="Absent").count()
        percentage = round((present / total) * 100, 2) if total else 0
        report.append({
            "student": student,
            "total": total,
            "present": present,
            "absent": absent,
            "percentage": percentage,
        })
    return render(request, "attendance/report.html", {"report": report})
