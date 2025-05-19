
from django.urls import reverse_lazy
from django.utils import timezone
from .models import Post, PostEditHistory
from .forms import PostForm
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin



class PostListView(generic.ListView):
    paginate_by = 5
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    
    def get_queryset(self):
        """Return published posts, ordered by date."""
        return Post.objects.filter(
            published_date__lte=timezone.now()
        ).order_by('published_date')



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
    