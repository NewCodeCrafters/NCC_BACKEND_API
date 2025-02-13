from rest_framework import generics
from accounts.permissions import IsAdminOrTeacher, IsAdminUser
from student.models import StudentPayment
from student.serializers import StudentPaymentSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated


class CreatePaymentView(generics.CreateAPIView):
    queryset = StudentPayment.objects.all()
    serializer_class = StudentPaymentSerializer
    permission_classes = [IsAdminOrTeacher]


class UpdatePaymentView(generics.UpdateAPIView):
    queryset = StudentPayment.objects.all()
    serializer_class = StudentPaymentSerializer
    permission_classes = [IsAdminOrTeacher]
    lookup_field = "student__user__slug"


class DeletePaymentView(generics.DestroyAPIView):
    queryset = StudentPayment.objects.all()
    serializer_class = StudentPaymentSerializer
    permission_classes = [IsAdminUser]
    lookup_field = "student__user__slug"


class ListDetailPaymentView(generics.ListAPIView):
    serializer_class = StudentPaymentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "student__user__email",
        "student__user__role",
        "amount",
        "date_paid",
    ]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        slug = self.kwargs["slug"]
        return StudentPayment.objects.filter(student__user__slug=slug)


class ListPaymentView(generics.ListAPIView):
    queryset = StudentPayment.objects.all()
    serializer_class = StudentPaymentSerializer
    permission_classes = [IsAdminOrTeacher]
