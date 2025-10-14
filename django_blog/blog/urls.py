from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Auth (login/logout use Django built-ins)
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),

    # Posts CRUD
    path('posts/', views.PostListView.as_view(), name='posts-list'),                    # /posts/
    path('posts/new/', views.PostCreateView.as_view(), name='post-create'),             # /posts/new/
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),        # /posts/<pk>/
    path('posts/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post-update'),   # /posts/<pk>/edit/
    path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'), # /posts/<pk>/delete/
]
