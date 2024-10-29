from rest_framework import serializers
from .models import OperatingHours, BreakTime

class OperatingHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperatingHours
        fields = ['day', 'start_time', 'end_time']

class BreakTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BreakTime
        fields = ['day', 'start_time', 'end_time']
