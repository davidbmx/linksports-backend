from rest_framework.routers import DefaultRouter

from .views import PostViewSet, MyPostViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'myposts', MyPostViewSet, basename='myposts')
urlpatterns = router.urls