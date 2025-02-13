from rest_framework import generics 
from student.models import StudentAdmission
from student.serializers import StudentAdmissionSerializers
from accounts.permissions import IsAdminOrTeacher, IsAdminUser
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

class CreateAdmissionView(generics.CreateAPIView):
    queryset = StudentAdmission.objects.all()
    serializer_class = StudentAdmissionSerializers
    permission_classes = [IsAdminOrTeacher]
    
class DeleteAdmissionView(generics.DestroyAPIView):
    queryset = StudentAdmission.objects.all()
    serializer_class = StudentAdmissionSerializers
    permission_classes = [IsAdminUser]
    lookup_field = "student__user__slug"
    
class UpdateAdmissionView(generics.UpdateAPIView):
    queryset = StudentAdmission.objects.all()
    serializer_class = StudentAdmissionSerializers
    permission_classes = [IsAdminOrTeacher]
    lookup_field = "student__user__slug"
    
class ListAdmissionView(generics.ListAPIView):
    queryset = StudentAdmission.objects.all()
    serializer_class = StudentAdmissionSerializers
    permission_classes = [IsAdminOrTeacher]
    
class ListDetailedAdmissionView(generics.ListAPIView):
    serializer_class = StudentAdmissionSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["student__user__email", "student__user__role", 'batch', 'date_start', 'date_end']
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        slug = self.kwargs["slug"]
        return StudentAdmission.objects.filter(student__user__slug=slug)