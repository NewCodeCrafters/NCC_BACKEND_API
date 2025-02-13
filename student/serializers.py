from rest_framework import serializers
from .models import StudentProfile, StudentPayment, StudentAdmission
from teacher.serializers import CourseSerializer
from accounts.serializers import UserListSerializer


class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserListSerializer(read_only=True)
    courses = CourseSerializer(many=True, read_only=True)
    extra_kwargs = {"slug": {"read_only": True}}

    class Meta:
        model = StudentProfile
        fields = (
            "user",
            "first_name",
            "last_name",
            "fee",
            "fully_paid",
            "courses",
            "slug",
            "balance",
        )
        
class LimitedStudentProfileSerializer(serializers.ModelSerializer):
    extra_kwargs = {"slug": {"read_only": True}}
    class Meta:
        model = StudentProfile
        fields = ("first_name", "last_name", "slug") 


class StudentPaymentSerializer(serializers.ModelSerializer):
    student = LimitedStudentProfileSerializer(read_only=True)

    class Meta:
        model = StudentPayment
        fields = (
            "student",
            "amount",
            "date_paid",
        )
        
class StudentAdmissionSerializers(serializers.ModelSerializer):
    student = LimitedStudentProfileSerializer(read_only=True)
    
    class Meta:
        model = StudentAdmission
        fields = (
            'student', 
            'batch',
            'date_start',
            'date_end',
        )
