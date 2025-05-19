from django.conf import settings
from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    modified_date = models.DateTimeField(blank=True, null=True)
    modified_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name='modified_posts',
        through='PostEditHistory'  # Add this line
    )


    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
    
class PostEditHistory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    edit_date = models.DateTimeField(auto_now_add=True)
    changed_fields = models.TextField(blank=True)  # Stores which fields changed

    class Meta:
        ordering = ['-edit_date']
        verbose_name_plural = 'Post edit history'