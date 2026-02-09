from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Dataset, EquipmentRecord


class EquipmentRecordSerializer(serializers.ModelSerializer):
    """Serializer for individual equipment records."""
    
    class Meta:
        model = EquipmentRecord
        fields = ['id', 'equipment_name', 'equipment_type', 'flowrate', 'pressure', 'temperature']


class DatasetSerializer(serializers.ModelSerializer):
    """Serializer for dataset with summary statistics."""
    records_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Dataset
        fields = [
            'id', 'filename', 'uploaded_at', 'total_count',
            'avg_flowrate', 'avg_pressure', 'avg_temperature',
            'type_distribution', 'records_count'
        ]
    
    def get_records_count(self, obj):
        return obj.records.count()


class DatasetDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer including all equipment records."""
    records = EquipmentRecordSerializer(many=True, read_only=True)
    
    class Meta:
        model = Dataset
        fields = [
            'id', 'filename', 'uploaded_at', 'total_count',
            'avg_flowrate', 'avg_pressure', 'avg_temperature',
            'type_distribution', 'records'
        ]


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    password = serializers.CharField(write_only=True, min_length=6)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user
