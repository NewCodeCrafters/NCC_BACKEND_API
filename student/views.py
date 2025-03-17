from datetime import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import AdmissionBatch, Course, Payment, Student, StudentCourse
from django.db.models import Sum
from .serializers import (
    CourseSerializer,
    AdmissionBatchSerializer,
    StudentSerializer,
    StudentCourseSerializer,
    PaymentSerializer,
    NestedStudentCourseSerializer,
    NestedPaymentSerializer,
    CreateStudentSerializer,
)
from .permissions import IsStaffOrAdmin, IsSelfOrStaffAdmin

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsStaffOrAdmin]  # Only staff/admin can manage courses

class AdmissionBatchViewSet(viewsets.ModelViewSet):
    queryset = AdmissionBatch.objects.all()
    serializer_class = AdmissionBatchSerializer
    permission_classes = [IsStaffOrAdmin]  # Only staff/admin can manage batches

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.select_related('user', 'admission_batch').all()
    serializer_class = StudentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['gender', 'admission_batch']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsStaffOrAdmin()]  # Only staff/admin can create/update/delete students
        return [permissions.IsAuthenticated()]  # Authenticated users can view

    @action(detail=False, methods=['post'], permission_classes=[IsStaffOrAdmin])
    def create_student(self, request):
        """Custom action to create a student with a user account."""
        serializer = CreateStudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def courses(self, request, pk=None):
        """Get all courses enrolled by a student."""
        student = self.get_object()
        enrollments = StudentCourse.objects.filter(student=student)
        serializer = NestedStudentCourseSerializer(enrollments, many=True)
        return Response(serializer.data)

class StudentCourseViewSet(viewsets.ModelViewSet):
    queryset = StudentCourse.objects.select_related('student', 'course').all()
    serializer_class = StudentCourseSerializer
    permission_classes = [IsStaffOrAdmin]  # Only staff/admin can manage enrollments

    @action(detail=True, methods=['get'])
    def payments(self, request, pk=None):
        """Get all payments for a specific enrollment."""
        enrollment = self.get_object()
        payments = Payment.objects.filter(enrollment=enrollment)
        serializer = NestedPaymentSerializer(payments, many=True)
        return Response(serializer.data)

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.select_related('enrollment').all()
    serializer_class = PaymentSerializer
    permission_classes = [IsStaffOrAdmin]  # Only staff/admin can manage payments

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent payments (last 30 days)."""
        recent_payments = Payment.objects.filter(
            payment_date__gte=timezone.now() - timezone.timedelta(days=30)
        )
        serializer = NestedPaymentSerializer(recent_payments, many=True)
        return Response(serializer.data)


class DashboardViewSet(viewsets.ViewSet):
    permission_classes = [IsStaffOrAdmin]  # Only staff/admin can access the dashboard

    @action(detail=False, methods=['get'])
    def active_students(self, request):
        """
        Get all active students in the current admission batch.
        """
        current_batch = AdmissionBatch.objects.filter(
            start_date__lte=timezone.now(),
            end_date__gte=timezone.now()
        ).first()

        if not current_batch:
            return Response(
                {"detail": "No active admission batch found."},
                status=status.HTTP_404_NOT_FOUND
            )

        active_students = Student.objects.filter(admission_batch=current_batch)
        serializer = StudentSerializer(active_students, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def fully_paid_students(self, request):
        """
        Get students who have fully paid their fees in the current admission batch.
        """
        current_batch = AdmissionBatch.objects.filter(
            start_date__lte=timezone.now(),
            end_date__gte=timezone.now()
        ).first()

        if not current_batch:
            return Response(
                {"detail": "No active admission batch found."},
                status=status.HTTP_404_NOT_FOUND
            )

        fully_paid_students = []
        for student in Student.objects.filter(admission_batch=current_batch):
            enrollments = StudentCourse.objects.filter(student=student)
            fully_paid = all(enrollment.balance == 0 for enrollment in enrollments)
            if fully_paid:
                fully_paid_students.append(student)

        serializer = StudentSerializer(fully_paid_students, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def total_revenue(self, request):
        """
        Get total revenue for the current admission batch.
        """
        current_batch = AdmissionBatch.objects.filter(
            start_date__lte=timezone.now(),
            end_date__gte=timezone.now()
        ).first()

        if not current_batch:
            return Response(
                {"detail": "No active admission batch found."},
                status=status.HTTP_404_NOT_FOUND
            )

        total_revenue = Payment.objects.filter(
            enrollment__student__admission_batch=current_batch,
            status='COMPLETED'
        ).aggregate(total=Sum('amount'))['total'] or 0

        return Response({"total_revenue": total_revenue})