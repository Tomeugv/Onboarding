from django import forms
from .models import Post, Category

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'text', 'category']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()
        self.fields['category'].required = False
        self.fields['category'].label = "Category (optional)"