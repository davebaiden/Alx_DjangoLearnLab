# accounts/views.py (append)
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, generics
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

User = get_user_model()

class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        """
        Follow the user with id=user_id
        """
        target = get_object_or_404(User, id=user_id)
        if target == request.user:
            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        # Add current user to target.followers OR add target to request.user.following
        target.followers.add(request.user)  # this makes request.user appear in target.followers
        return Response({"detail": f"You are now following {target.username}."}, status=status.HTTP_200_OK)


class UnfollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        """
        Unfollow the user with id=user_id
        """
        target = get_object_or_404(User, id=user_id)
        if target == request.user:
            return Response({"detail": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        target.followers.remove(request.user)
        return Response({"detail": f"You have unfollowed {target.username}."}, status=status.HTTP_200_OK)


class FollowingListView(generics.ListAPIView):
    """
    List users that the current user is following.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = None  # optional: replace with a UserSerializer if you have one

    def get(self, request, *args, **kwargs):
        following_qs = request.user.following.all()
        data = [{"id": u.id, "username": u.username} for u in following_qs]
        return Response(data)
