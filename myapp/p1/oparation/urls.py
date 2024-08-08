from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, TagView, FavoriteView, LikeView, CommentView, PaginatedPostView, ToplikeView, TopCommentView, SpecificAuthorView

router = DefaultRouter()
router.register(r'post', PostViewSet, basename='PostViewSet')
router.register(r'tag',TagView,basename='tag')
router.register(r'favorite',FavoriteView,basename='favorite')
router.register(r'like',LikeView,basename='like')
router.register(r'comment',CommentView,basename='comment')
urlpatterns = [
    path('paginated/post', PaginatedPostView.as_view(), name='paginated_post'),
    path('top/like', ToplikeView.as_view(), name='top_like'),
    path('top/comment', TopCommentView.as_view(), name='top_comment'),
    path('specific/author/<author_id>/', SpecificAuthorView.as_view(), name='specific_author'),
    path('', include(router.urls)),
]