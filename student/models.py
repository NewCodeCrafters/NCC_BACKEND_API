from django.db import models
from django.db.models import Sum
from django.utils.text import slugify

from django.contrib.auth import get_user_model

User = get_user_model()

class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

class AdmissionBatch(models.Model):
    name = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.name} ({self.year})"

class Student(models.Model):
    class Gender(models.TextChoices):
        MALE = 'M', 'Male'
        FEMALE = 'F', 'Female'

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='student_profile'  # Unique related_name
    )
    student_id = models.CharField(max_length=20, unique=True)
    admission_batch = models.ForeignKey(AdmissionBatch, on_delete=models.SET_NULL, null=True)
    gender = models.CharField(max_length=1, choices=Gender.choices)
    dob = models.DateField()


class StudentCourse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    batch = models.CharField(max_length=50)
    enrollment_date = models.DateField(auto_now_add=True)

    @property
    def balance(self):
        total_paid = self.payment_set.aggregate(total=Sum('amount'))['total'] or 0
        return self.course.fee - total_paid

class Payment(models.Model):
    enrollment = models.ForeignKey(StudentCourse, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('PENDING', 'Pending'), ('COMPLETED', 'Completed')])
