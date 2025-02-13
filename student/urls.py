from django.urls import path
from .controllers.profile_views import (
    StudentUpdateView,
    StudentCreateView,
    StudentDetailListView,
    StudentListView,
    StudentDeleteView,
)

from .controllers import profile_views, payment_views, admission_views

urlpatterns = [
    # Profile Views
    
    path("create_student/", profile_views.StudentCreateView.as_view(), name="create_student"),
    path("list_students/", profile_views.StudentListView.as_view(), name="all_students"),
    path("delete_profile/<slug:user__slug>/", profile_views.StudentDeleteView.as_view(), name="delete_student"),
    path("update_profile/<slug:user__slug>/", profile_views.StudentUpdateView.as_view(), name="update_student"),
    path("filter_student/<slug:user__slug>/", profile_views.StudentDetailListView.as_view(), name="filter_student"),
    
    # Payment Views
    path('create_payment/', payment_views.CreatePaymentView.as_view(), name='create_payment'),
    path('list_payments/', payment_views.ListPaymentView.as_view(), name='list_payments'),
    path('delete_payment/<slug:student__user__slug>/', payment_views.DeletePaymentView.as_view(), name='delete_payment'),
    path('update_payment/<slug:student__user__slug>/', payment_views.UpdatePaymentView.as_view(), name='update_payment'),
    path('filter_payment/<slug:student__user__slug>/', payment_views.ListDetailPaymentView.as_view(), name='filter_payment'),
    
    # Admission Views
    path('register_admission/', admission_views.CreateAdmissionView.as_view(), name='create_admission'),
    path('list_admissions/', admission_views.ListAdmissionView.as_view(), name="list_admissions"),
    path('delete_admission/<slug:student__user__slug>/', admission_views.DeleteAdmissionView.as_view(), name='delete_admission'),
    path('update_admission/<slug:student__user__slug>/', admission_views.UpdateAdmissionView.as_view(), name='update_admission'),
    path('filter_admission/<slug:student__user__slug>/', admission_views.ListDetailedAdmissionView.as_view(), name='filter_admission'),
]
