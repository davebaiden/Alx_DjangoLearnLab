from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.db.models import Q

from .models import Post, Comment, Tag
from .forms import PostForm, CommentForm

# --- existing auth views & PostListView/PostDetailView kept ---

class PostListView(ListView):
    model = Post
    template_name = 'blog/posts_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 10

    def get_queryset(self):
        # if there's a search query (q), forward to SearchResultsView instead, but allow filtering here too
        qs = super().get_queryset()
        q = self.request.GET.get('q', '')
        if q:
            qs = qs.filter(
                Q(title__icontains=q) |
                Q(content__icontains=q) |
                Q(tags__name__icontains=q)
            ).distinct()
        return qs

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['comments'] = post.comments.all()
        context['comment_form'] = CommentForm()
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        # set author then save, handle tags
        form.instance.author = self.request.user
        response = super().form_valid(form)
        self._handle_tags(form.cleaned_data.get('tags', ''), self.object)
        return response

    def _handle_tags(self, tags_field, post_obj):
        tag_names = [t.strip() for t in tags_field.split(',') if t.strip()]
        tags_objs = []
        for name in tag_names:
            tag_obj, created = Tag.objects.get_or_create(name__iexact=name, defaults={'name': name})
            # get_or_create can't search case-insensitively with name__iexact in get_or_create,
            # so adjust to check first:
            if created:
                tags_objs.append(tag_obj)
            else:
                # If get_or_create with name__iexact did not work in some DBs, ensure we have the object:
                try:
                    tag_obj = Tag.objects.get(name__iexact=name)
                except Tag.DoesNotExist:
                    tag_obj = Tag.objects.create(name=name)
                tags_objs.append(tag_obj)
        post_obj.tags.set(tags_objs)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        self._handle_tags(form.cleaned_data.get('tags', ''), self.object)
        return response

    def _handle_tags(self, tags_field, post_obj):
        tag_names = [t.strip() for t in tags_field.split(',') if t.strip()]
        tags_objs = []
        for name in tag_names:
            try:
                tag_obj = Tag.objects.get(name__iexact=name)
            except Tag.DoesNotExist:
                tag_obj = Tag.objects.create(name=name)
            tags_objs.append(tag_obj)
        post_obj.tags.set(tags_objs)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

# --------- Tag listing / Search ---------

class TagListView(ListView):
    model = Post
    template_name = 'blog/posts_list.html'  # reuse posts_list template
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        tag_name = self.kwargs.get('tag_name')
        return Post.objects.filter(tags__slug=tag_name).order_by('-published_date').distinct()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['tag_name'] = self.kwargs.get('tag_name')
        return ctx

class SearchResultsView(ListView):
    model = Post
    template_name = 'blog/search_results.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get('q', '').strip()
        if not q:
            return Post.objects.none()
        queryset = Post.objects.filter(
            Q(title__icontains=q) |
            Q(content__icontains=q) |
            Q(tags__name__icontains=q)
        ).distinct().order_by('-published_date')
        return queryset
