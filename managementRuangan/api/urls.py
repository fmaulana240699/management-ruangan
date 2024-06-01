from django.urls import path
from .views import GedungListCreateView, GedungDeleteView, GedungUpdateView, ReservasiGedungListCreateView, ApprovalReservasiAPIView, LoginView, LogoutView, UserDeleteView, UserUpdateView, UserListView, RegisterView

urlpatterns = [
    path('gedung', GedungListCreateView.as_view(), name='gedung-list-create'),
    path('gedung/delete', GedungDeleteView.as_view(), name='gedung-delete'),
    path('gedung/<int:pk>', GedungUpdateView.as_view(), name='gedung-update'),
    path('reservasi', ReservasiGedungListCreateView.as_view(), name='reservasi-list-create'),
    path('approval', ApprovalReservasiAPIView.as_view(), name='approval-reservasi'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),  
    path('register/', RegisterView.as_view(), name='register'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<str:pk>/', UserUpdateView.as_view(), name='user-details-update'),
    path('users/delete/', UserDeleteView.as_view(), name='user-delete'),      
]
