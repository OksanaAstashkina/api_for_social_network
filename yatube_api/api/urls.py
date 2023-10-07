from django.urls import include, path
from rest_framework import routers

from api.views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet

app_name = 'api'

router_version_1 = routers.DefaultRouter()
router_version_1.register('v1/posts', PostViewSet, basename='posts')
router_version_1.register('v1/groups', GroupViewSet, basename='groups')
router_version_1.register('v1/follow', FollowViewSet, basename='follow')
router_version_1.register(
    r'v1/posts/(?P<post_id>\d+)/comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('', include(router_version_1.urls)),
    path('v1/', include('djoser.urls.jwt')),
]
