from django.urls import path
from .views import GedungListCreateView, GedungDeleteView, GedungUpdateView, ReservasiGedungListCreateView, ApprovalReservasiAPIView

urlpatterns = [
    path('gedung', GedungListCreateView.as_view(), name='gedung-list-create'),
    path('gedung/delete', GedungDeleteView.as_view(), name='gedung-delete'),
    path('gedung/<int:pk>', GedungUpdateView.as_view(), name='gedung-update'),
    path('reservasi', ReservasiGedungListCreateView.as_view(), name='reservasi-list-create'),
    path('approval', ApprovalReservasiAPIView.as_view(), name='approval-reservasi'),
]
