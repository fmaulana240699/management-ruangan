from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.forms.models import model_to_dict
from .models import Gedung, ReservasiGedung
from .serializers import GedungSerializer, ReservasiGedungSerializer

class GedungListCreateView(generics.ListCreateAPIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated, IsAdmin]    
    queryset = Gedung.objects.all()
    serializer_class = GedungSerializer  


class GedungDeleteView(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated, IsAdmin | IsItSupport]

    def delete(self, request):
        gedung_id = request.data.get('id')

        try:
            gedung = Gedung.objects.get(id=gedung_id)
            gedung.delete()
            return Response({'message': 'Gedung berhasil dihapus'}, status=204)
        except Gedung.DoesNotExist:
            return Response({'message': 'Gedung tidak ditemukan'}, status=404)


class GedungUpdateView(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated, IsAdmin | IsItSupport]

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
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated, IsAdmin]    
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
    

class login():
    pass

class logout():
    pass