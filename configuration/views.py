from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from configuration.models import Sport
from configuration.serializers import SportSerializer

# Create your views here.
class SportListView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Sport.objects.all()
    serializer_class = SportSerializer
    permission_classes = [IsAuthenticated]