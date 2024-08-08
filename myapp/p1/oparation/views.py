from rest_framework import generics, permissions
from cpre.models.comment import Comment
from cpre.models.favorite import Favorite
from cpre.models.like import Like
from cpre.models.tag import Tag
from cpre.models.post import Post
from .serializers import PostSerializer, TagsSerializer, FavoriteSerializer, CommentSerializer, LikeSerializer
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .permissions import IsUserAuthor
from django.db.models import Count
from rest_framework.response import Response
from rest_framework import status

class TagView(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    permission_classes = [permissions.IsAuthenticated, IsUserAuthor]

    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)

class CommentView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsUserAuthor]
    #we just test this to see if we can pass an id to the header only for learing but i did not use this in the testing
    def create(self, request, *args, **kwargs):
        response =  super().create(request, *args, **kwargs)
        response.headers['X-CONTENT-ID'] = response.data['id']
        return response

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class LikeView(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated, IsUserAuthor]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class FavoriteView(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated, IsUserAuthor]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostPagination(PageNumberPagination):
    page_size = 10

class PaginatedPostView(generics.ListAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    pagination_class = PostPagination   

    

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().prefetch_related('tags')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['title', 'html_body', 'tags__name']
    filterset_fields = ['title', 'html_body', 'tags']
    ordering_fields = ['created_at','id']
    ordering = ['created_at']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class ToplikeView(generics.ListAPIView):
    serializer_class = PostSerializer
    
    def get_queryset(self):
        return Post.objects.annotate(
            like_count=Count('likes')
        ).order_by('-like_count')[:10]

class TopCommentView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.annotate(
            comment_count=Count('comments')
            ).order_by('-comment_count')[:10]

class SpecificAuthorView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        author_id = self.kwargs.get('author_id')
        if author_id is not None:
            return Post.objects.filter(author_id=author_id)
        return Post.objects.none()