
from django.urls import reverse_lazy
from django.utils import timezone
from .models import Post, PostEditHistory, Category
from .forms import PostForm
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .filters import PostFilter

User = get_user_model()


class PostListView(generic.ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context



class DetailView(generic.DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = PostForm 
    template_name = 'blog/post_edit.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.published_date = timezone.now()
        response = super().form_valid(form)  # Saves the form first
        form.instance.modified_by.add(self.request.user)  # Adds current user to M2M
        return response


class PostUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Post
    form_class = PostForm 
    template_name = 'blog/post_edit.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        # Get the original post before changes
        original_post = self.get_object()
        
        # Detect changed fields
        changed_fields = []
        if form.instance.title != original_post.title:
            changed_fields.append('title')
        if form.instance.text != original_post.text:
            changed_fields.append('text')
        
        # Save modifications
        form.instance.modified_date = timezone.now()
        response = super().form_valid(form)
        
        # Record edit history if any changes were made
        if changed_fields:
            post_edit = PostEditHistory.objects.create(
                post=form.instance,
                user=self.request.user,
                changed_fields=", ".join(changed_fields)
            )
            post_edit.save()
            form.instance.modified_by.add(self.request.user)
        
        return response
    

class AuthorPostsView(generic.ListView):
    template_name = 'blog/author_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        self.author = get_object_or_404(User, username=self.kwargs['username'])
        return Post.objects.filter(
            author=self.author,
            published_date__isnull=False
        ).order_by('-published_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = self.author
        return context
    
class CategoryPostsView(generic.ListView):
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Post.objects.filter(
            category=self.category,
            published_date__isnull=False
        ).order_by('-published_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['title'] = f"Posts in category: {self.category.name}"
        return context