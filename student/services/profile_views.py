from rest_framework import generics
from student.models import StudentProfile
from accounts.permissions import IsAdminOrTeacher, IsAdminUser
from student.serializers import StudentProfileSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class StudentCreateView(generics.CreateAPIView):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    permission_classes = [IsAdminOrTeacher]


class StudentListView(generics.ListAPIView):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    permission_classes = [IsAdminOrTeacher]


class StudentDetailListView(generics.ListAPIView):
    serializer_class = StudentProfileSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "user__email",
        "user__role",
        "first_name",
        "last_name",
        "fee",
        "courses",
        "balance",
    ]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        slug = self.kwargs["slug"]
        return StudentProfile.objects.filter(user__slug=slug)


class StudentUpdateView(generics.UpdateAPIView):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    permission_classes = [IsAdminOrTeacher]
    lookup_field = "user__slug"


class StudentDeleteView(generics.DestroyAPIView):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    permission_classes = [IsAdminUser]
    lookup_field = "user__slug"
