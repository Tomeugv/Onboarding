from django.urls import path
from . import views
from debug_toolbar.toolbar import debug_toolbar_urls


urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', views.DetailView.as_view(), name='post_detail'),
    path('post/new/', views.PostCreateView.as_view(), name='post_new'),
    path('post/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    path('author/<str:username>/', views.AuthorPostsView.as_view(), name='author_posts'),
    path('category/<slug:slug>/', views.CategoryPostsView.as_view(), name='category_posts'),
] + debug_toolbar_urls()