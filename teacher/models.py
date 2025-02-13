from django.db import models
from django.utils.text import slugify

# Create your models here.


class Course(models.Model):
    course_choices = {
        "ML": "Machine Learning",
        "Frontend": "Frontend Development",
        "Backend": "Backend Development",
        "CyberSec": "Cyber Security",
    }
    course = models.CharField(max_length=50, choices=course_choices)


class TeacherProfile(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    courses = models.ManyToManyField(Course)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Teacher {self.first_name} {self.last_name} Created"


class TeacherPayment(models.Model):
    teacher = models.ForeignKey(
        TeacherProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="teacher_payments",
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_paid = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment of {self.amount} to {self.teacher.first_name} {self.teacher.last_name}"
