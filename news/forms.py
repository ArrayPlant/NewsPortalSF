from django import forms
from .models import Post

class NewsForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'categories']

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'categories']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'categories']