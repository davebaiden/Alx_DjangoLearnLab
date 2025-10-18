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


# --------- Authentication Views ---------
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("post-list")
    else:
        form = UserCreationForm()
    return render(request, "blog/register.html", {"form": form})


@login_required
def profile(request):
    return render(request, "blog/profile.html")


# --------- Post Views (CRUD) ---------
class PostListView(ListView):
    model = Post
    template_name = "blog/posts_list.html"
    context_object_name = "posts"
    ordering = ["-published_date"]
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get("q", "")
        if q:
            qs = qs.filter(
                Q(title__icontains=q)
                | Q(content__icontains=q)
                | Q(tags__name__icontains=q)
            ).distinct()
        return qs


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context["comments"] = post.comments.all()
        context["comment_form"] = CommentForm()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        self._handle_tags(form.cleaned_data.get("tags", ""), self.object)
        return response

    def _handle_tags(self, tags_field, post_obj):
        tag_names = [t.strip() for t in tags_field.split(",") if t.strip()]
        tags_objs = []
        for name in tag_names:
            try:
                tag_obj = Tag.objects.get(name__iexact=name)
            except Tag.DoesNotExist:
                tag_obj = Tag.objects.create(name=name)
            tags_objs.append(tag_obj)
        post_obj.tags.set(tags_objs)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        self._handle_tags(form.cleaned_data.get("tags", ""), self.object)
        return response

    def _handle_tags(self, tags_field, post_obj):
        tag_names = [t.strip() for t in tags_field.split(",") if t.strip()]
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
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("post-list")

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


# --------- Tag & Search Views ---------
class TagListView(ListView):
    model = Post
    template_name = "blog/posts_list.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        tag_name = self.kwargs.get("tag_name")
        return Post.objects.filter(tags__slug=tag_name).order_by("-published_date").distinct()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["tag_name"] = self.kwargs.get("tag_name")
        return ctx


class SearchResultsView(ListView):
    model = Post
    template_name = "blog/search_results.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get("q", "").strip()
        if not q:
            return Post.objects.none()
        queryset = Post.objects.filter(
            Q(title__icontains=q)
            | Q(content__icontains=q)
            | Q(tags__name__icontains=q)
        ).distinct().order_by("-published_date")
        return queryset


# --------- Comment CRUD ---------
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs["pk"])
        form.instance.author = self.request.user
        form.instance.post = post
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.post.get_absolute_url()


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return self.object.post.get_absolute_url()


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "blog/comment_confirm_delete.html"

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return self.object.post.get_absolute_url()
