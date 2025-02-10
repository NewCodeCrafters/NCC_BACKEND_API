from rest_framework import generics
from rest_framework.response import Response
from .models import User
from .serializers import AdminCreateUserSerializer, UserListSerializer
from .permissions import IsAdminUser, IsAdminOrTeacher
from rest_framework import status



# Create your views here.

class UserCreateView(generics.CreateAPIView):
    """Only Admin can create users."""
    queryset = User.objects.all()
    serializer_class = AdminCreateUserSerializer
    permission_classes = [IsAdminUser]
    
class UserListView(generics.ListAPIView):
    """Only Admin can list all users."""
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAdminOrTeacher]

class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]
    lookup_field = "slug"

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        if user.role == "admin":
            return Response({"error": "You cannot delete an admin user!"}, status=status.HTTP_403_FORBIDDEN)
        return super().delete(request, *args, **kwargs)

class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAdminUser]
    lookup_field = "slug"