from rest_framework import serializers
from .models import Gedung, ReservasiGedung, Users


class GedungSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gedung
        fields = '__all__'

class ReservasiGedungSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservasiGedung
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