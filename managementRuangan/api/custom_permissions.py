from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
   def has_permission(self, request, view):
      if request.user.role == "Admin":
         return True
      return False

class IsPeminjam(BasePermission):
   def has_permission(self, request, view):
      if request.user.role == "Peminjam":
         return True
      return False