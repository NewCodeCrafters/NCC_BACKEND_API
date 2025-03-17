from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CourseViewSet,
    AdmissionBatchViewSet,
    StudentViewSet,
    StudentCourseViewSet,
    PaymentViewSet,
    DashboardViewSet,
)

router = DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'admission-batches', AdmissionBatchViewSet)
router.register(r'students', StudentViewSet)
router.register(r'enrollments', StudentCourseViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'dashboard', DashboardViewSet, basename='dashboard')

urlpatterns = [
    path('', include(router.urls)),
]