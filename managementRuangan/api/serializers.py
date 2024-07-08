from rest_framework import serializers
from .models import Gedung, ReservasiGedung, Users


class GedungSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gedung
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Users
        fields = '__all__'

    def create(self, validated_data):
        password = validated_data.pop('password')
        instance = self.Meta.model(**validated_data)
        instance.set_password(password) 
        instance.save()
        return instance

class NamaGedungSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gedung
        fields = ['nama']

class FullnameUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['fullname', 'email']

class ReservasiGedungSerializer(serializers.ModelSerializer):
    id_gedung = NamaGedungSerializer()
    id_peminjam = FullnameUserSerializer()
    
    class Meta:
        model = ReservasiGedung
        fields = '__all__' 

class ReservasiGedungCreateSerializer(serializers.ModelSerializer):    
    class Meta:
        model = ReservasiGedung
        fields = '__all__'   