from django.db import models
from django.db.models import Sum
from django.utils.text import slugify

# Create your models here.


class StudentProfile(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    fully_paid = models.BooleanField(default=False)
    courses = models.ManyToManyField("teacher.Course")
    slug = models.SlugField(unique=True, blank=True, null=True)

    @property
    def balance(self):
        total_paid = self.student_payments.aggregate(Sum("amount"))["amount__sum"] or 0
        return self.fee - total_paid

    def save(self, *args, **kwargs):
        
        self.fully_paid = self.balance == 0 
        
        if not self.slug:
            self.slug = slugify(self.user.username)
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Student {self.first_name} {self.last_name} Created"


class StudentPayment(models.Model):
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="student_payments",
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_paid = models.DateTimeField(auto_now_add=True)
    
    date_paid = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  
        if self.student:
            self.student.save()

    def __str__(self):
        return f"Payment of {self.amount} to {self.student.first_name} {self.student.last_name}"


class StudentAdmission(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.SET_NULL, null=True)
    batch = models.CharField(max_length=200)
    date_start = models.DateField(auto_now_add=True)
    date_end = models.DateField(null=True, blank=True)
