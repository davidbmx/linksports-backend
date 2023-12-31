from rest_framework.routers import DefaultRouter

from .views import PostViewSet, MyPostViewSet, PostCommentView, PostUserViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'posts/(?P<post_id>[0-9a-f-]+)/comments', PostCommentView, basename='comments')
router.register(r'posts/by_user/(?P<uid>\w+)', PostUserViewSet, basename='by_user')
router.register(r'myposts', MyPostViewSet, basename='myposts')
urlpatterns = router.urls
