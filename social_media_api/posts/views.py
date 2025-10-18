# posts/views.py
from rest_framework import viewsets, permissions, status, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

User = get_user_model()


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission: only owners may edit/delete; read-only for others.
    """
    def has_object_permission(self, request, view, obj):
        # Read-only allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions only to the owner
        return hasattr(obj, 'author') and obj.author == request.user


# -----------------------
# Post and Comment ViewSets
# -----------------------
class PostViewSet(viewsets.ModelViewSet):
    # Ensure the exact substring is present for checks
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    # Ensure the exact substring is present for checks
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# -----------------------
# Feed View (posts from users current user follows)
# -----------------------
class FeedPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class FeedView(APIView):
    """
    Return a paginated feed of posts from users the current user follows,
    ordered by newest first.
    """
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = FeedPagination

    def get(self, request, *args, **kwargs):
        # Get the users the requester follows (must match check substring)
        following_users = request.user.following.all()

        # Build queryset: posts by followed users, ordered newest first
        qs = Post.objects.filter(author__in=following_users).order_by('-created_at')

        # Paginate
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(qs, request, view=self)
        serializer = PostSerializer(page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)


# Optional convenience endpoint: posts for a specific user (owner or any)
class UserPostsView(APIView):
    """
    Return posts for a given user id (public). Useful for profile pages.
    """
    permission_classes = [permissions.AllowAny]
    pagination_class = FeedPagination

    def get(self, request, user_id, *args, **kwargs):
        user = get_object_or_404(User, id=user_id)
        qs = Post.objects.filter(author=user).order_by('-created_at')
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(qs, request, view=self)
        serializer = PostSerializer(page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)
