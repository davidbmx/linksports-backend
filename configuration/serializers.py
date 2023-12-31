from rest_framework import serializers

from configuration.models import Sport

class SportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sport
        fields = '__all__'
        