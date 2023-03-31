from rest_framework import serializers
from project.app.models import File, CheckLog

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'

class CheckLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckLog
        fields = '__all__'