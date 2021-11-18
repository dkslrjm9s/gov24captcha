from rest_framework import serializers
from .models import AnaResults

class AnaResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnaResults
        fields = ['created', 'result', 'time', 'img']