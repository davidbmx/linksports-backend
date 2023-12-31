from rest_framework.routers import DefaultRouter

from configuration.views import SportListView

router = DefaultRouter()

router.register(r'configuration/sports', SportListView, basename='sports')

urlpatterns = router.urls
