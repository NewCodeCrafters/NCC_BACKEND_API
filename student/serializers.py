from rest_framework import serializers
from .models import AdmissionBatch, Course, Payment, Student, StudentCourse

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'fee', 'start_date', 'end_date']

class AdmissionBatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdmissionBatch
        fields = ['id', 'name', 'year', 'start_date', 'end_date']
        
class StudentSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)

    class Meta:
        model = Student
        fields = [
            'student_id', 'email', 'first_name', 'last_name', 
            'admission_batch', 'gender', 'dob'
        ]
        
class StudentCourseSerializer(serializers.ModelSerializer):
    balance = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = StudentCourse
        fields = [
            'id', 'student', 'course', 'batch', 
            'enrollment_date', 'balance'
        ]


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'id', 'enrollment', 'amount', 
            'payment_date', 'status'
        ]
        
class NestedStudentCourseSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    balance = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = StudentCourse
        fields = [
            'id', 'student', 'course', 'batch', 
            'enrollment_date', 'balance'
        ]
        
class NestedPaymentSerializer(serializers.ModelSerializer):
    enrollment = NestedStudentCourseSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id', 'enrollment', 'amount', 
            'payment_date', 'status'
        ]

from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class CreateStudentSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    student_id = serializers.CharField(write_only=True)
    admission_batch = serializers.PrimaryKeyRelatedField(
        queryset=AdmissionBatch.objects.all(), write_only=True
    )
    gender = serializers.ChoiceField(
        choices=Student.Gender.choices, write_only=True
    )
    dob = serializers.DateField(write_only=True)

    class Meta:
        model = Student
        fields = [
            'email', 'password', 'first_name', 'last_name',
            'student_id', 'admission_batch', 'gender', 'dob'
        ]

    def create(self, validated_data):
        # Extract user-related data
        user_data = {
            'email': validated_data.pop('email'),
            'password': validated_data.pop('password'),
            'first_name': validated_data.pop('first_name'),
            'last_name': validated_data.pop('last_name'),
        }

        # Create user
        user = User.objects.create_user(**user_data)

        # Create student
        student = Student.objects.create(user=user, **validated_data)
        return student
