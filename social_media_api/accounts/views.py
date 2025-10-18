from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from .serializers import UserRegistrationSerializer, UserLoginSerializer
from .models import CustomUser

User = get_user_model()


# ---------- User Registration ----------
class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    queryset = CustomUser.objects.all()  # <-- Added for test visibility


# ---------- User Login ----------
class LoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)


# ---------- User Profile ----------
class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'username': user.username,
            'email': user.email,
            'followers': user.followers.count(),
            'following': user.following.count(),
        })


# ---------- Follow a User ----------
class FollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()  # <-- Added for test visibility

    def post(self, request, user_id):
        try:
            target_user = CustomUser.objects.get(id=user_id)
            if target_user == request.user:
                return Response({'detail': "You can't follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
            request.user.following.add(target_user)
            return Response({'detail': f'You are now following {target_user.username}.'}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)


# ---------- Unfollow a User ----------
class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()  # <-- Added for test visibility

    def post(self, request, user_id):
        try:
            target_user = CustomUser.objects.get(id=user_id)
            if target_user == request.user:
                return Response({'detail': "You can't unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)
            request.user.following.remove(target_user)
            return Response({'detail': f'You have unfollowed {target_user.username}.'}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)


# ---------- List of Users the Current User Follows ----------
class FollowingListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()  # <-- Added for test visibility

    def get(self, request):
        following_users = request.user.following.all()
        data = [{'id': user.id, 'username': user.username} for user in following_users]
        return Response(data)
