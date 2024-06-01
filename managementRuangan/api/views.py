from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.forms.models import model_to_dict
from .custom_permissions import IsAdmin, IsPeminjam
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Gedung, ReservasiGedung, Users
from .serializers import GedungSerializer, ReservasiGedungSerializer, UserSerializer

class GedungListCreateView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin]    
    queryset = Gedung.objects.all()
    serializer_class = GedungSerializer  


class GedungDeleteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin]

    def delete(self, request):
        gedung_id = request.data.get('id')

        try:
            gedung = Gedung.objects.get(id=gedung_id)
            gedung.delete()
            return Response({'message': 'Gedung berhasil dihapus'}, status=204)
        except Gedung.DoesNotExist:
            return Response({'message': 'Gedung tidak ditemukan'}, status=404)


class GedungUpdateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request, pk):
        # try:
        #     gedung = Gedung.objects.get(pk=pk)
        #     gedung = model_to_dict(gedung)
        #     return Response(gedung, status=200)
        # except Gedung.DoesNotExist:
        #     return Response({'message': 'Gedung tidak ditemukan'}, status=404) 
        try:
            gedung = Gedung.objects.get(pk=pk)
        except Gedung.DoesNotExist:
            return Response({"error": "Gedung tidak ditemukan"}, status=404)

        reservasi = ReservasiGedung.objects.filter(id_gedung=gedung)
        gedungSerializer = GedungSerializer(gedung)
        reservasiSerializer = ReservasiGedungSerializer(reservasi, many=True)

        data = {
            "building": gedungSerializer.data,
            "reservations": reservasiSerializer.data
        }

        return Response(data)
        
    def patch(self, request, pk):
        try:
            gedung = Gedung.objects.get(pk=pk)
            serializer = GedungSerializer(gedung, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=200)
            return Response(serializer.errors, status=400)
        except Gedung.DoesNotExist:
            return Response({'message': 'Gedung tidak ditemukan'}, status=404)           

class ReservasiGedungListCreateView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin]    
    queryset = ReservasiGedung.objects.all()
    serializer_class = ReservasiGedungSerializer

    def post(self, request):
        data = request.data
        serializer = ReservasiGedungSerializer(data=data)
        if serializer.is_valid():
            gedung = serializer.validated_data['id_gedung']
            start_time = serializer.validated_data['start_peminjaman']
            end_time = serializer.validated_data['end_peminjaman']

            conflicts = ReservasiGedung.objects.filter(
                id_gedung=gedung,
                start_peminjaman=start_time,
                end_peminjaman=end_time
            ).exists()            

            if conflicts:
                return Response({"error": "Reservasi konflik"}, status=400)
            
            serializer.save()
            return Response(serializer.data, status=201)
        
        return Response(serializer.errors, status=400)

class ApprovalReservasiAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin]       
    def patch(self, request):
        try:
            reservation = ReservasiGedung.objects.get(id=request.data["id_reservasi"])
        except ReservasiGedung.DoesNotExist:
            return Response({"error": "Reservasi tidak ditemukan"}, status=404)

        serializer = ReservasiGedungSerializer(reservation, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=400)
    

class LoginView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = Users.objects.filter(username=username).first()

        if user is None:
            return Response({'error': 'Invalid credentials'}, status=400)

        if not user.check_password(password):
            return Response({'error': 'Invalid credentials'}, status=400)

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                "username": user.username,
                "role": user.role
                # "fullname": user.fullname
            }
        })

class LogoutView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated & (IsAdmin | IsPeminjam)]  

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=205)
        except Exception as e:
            return Response(status=400)    
        
class UserDeleteView(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated & IsAdmin]

    def delete(self, request):
        user_id = request.data.get('id')
        try:
            user = Users.objects.get(id=user_id)
            user.delete()
            return Response({'message': 'User berhasil dihapus'}, status=204)
        except Users.DoesNotExist:
            return Response({'message': 'User tidak ditemukan'}, status=404)

class UserUpdateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated & IsAdmin]

    def get(self, request, pk):
        try:
            user = Users.objects.get(id=pk)
            user = model_to_dict(user)
            return Response(user, status=200)
        except Users.DoesNotExist:
            return Response({'message': 'User tidak ditemukan'}, status=404)     

    def patch(self, request, pk):
        try:
            user = Users.objects.get(id=pk)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                validated_data = serializer.validated_data
                if validated_data.get("password"):
                    validated_data["password"] = make_password(request.data["password"])
                serializer.save()
                return Response(serializer.data, status=200)
            return Response(serializer.errors, status=400)
        except Users.DoesNotExist:
            return Response({'message': 'User tidak ditemukan'}, status=404) 
        
class UserListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated & IsAdmin]      
    queryset = Users.objects.all()
    serializer_class = UserSerializer      


class RegisterView(generics.CreateAPIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated & IsAdmin]
    queryset = Users.objects.all()
    serializer_class = UserSerializer