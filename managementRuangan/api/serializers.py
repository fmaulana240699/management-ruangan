from rest_framework import serializers
from .models import Gedung, ReservasiGedung


class GedungSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gedung
        fields = '__all__'

class ReservasiGedungSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservasiGedung
        fields = '__all__' 