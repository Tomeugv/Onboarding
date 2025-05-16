from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.shortcuts import redirect
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
        return super().form_valid(form)

'''
class CreateView(generic.CreateView):
    model = Post
    template_name = "blog/post_edit.html"
    fields = ['title', 'text']
    
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})
'''
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})
