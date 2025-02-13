from django.urls import path
from .services.views import UserCreateView, UserListView, UserDeleteView, UserUpdateView

urlpatterns = [
    path("create/", UserCreateView.as_view(), name="user-create"),
    path("", UserListView.as_view(), name="user-list"),
    path("<slug:slug>/delete/", UserDeleteView.as_view(), name="user-delete"),
    path("<slug:slug>/update/", UserUpdateView.as_view(), name="user-update"),
]
