from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

from .models import Post, News, Author
from .forms import NewsForm, ArticleForm, PostForm
from .filters import NewsFilter


def news_list(request):
    news_list = News.objects.all()
    paginator = Paginator(news_list, 10)  # 10 новостей на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'news/news_list.html', {'page_obj': page_obj})


def news_detail(request, news_id):
    news_item = get_object_or_404(News, pk=news_id)
    return render(request, 'news/news_detail.html', {'news_item': news_item})


def news_search(request):
    news = News.objects.all()
    news_filter = NewsFilter(request.GET, queryset=news)
    return render(request, 'news/news_search.html', {'filter': news_filter})


class ArticleListView(ListView):
    model = Post
    template_name = 'news/article_list.html'
    context_object_name = 'articles'

    def get_queryset(self):
        return Post.objects.filter(type=Post.ARTICLE)


class NewsCreateView(PermissionRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'news/news_form.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        author, created = Author.objects.get_or_create(user=self.request.user)
        post = form.save(commit=False)
        post.author = author
        post.type = Post.NEWS
        post.save()
        return super().form_valid(form)


class NewsUpdateView(PermissionRequiredMixin, UpdateView):
    model = Post
    form_class = NewsForm
    template_name = 'news/news_form.html'

    def get_queryset(self):
        return Post.objects.filter(type=Post.NEWS)


class NewsDeleteView(DeleteView):
    model = Post
    template_name = 'news/news_confirm_delete.html'
    success_url = reverse_lazy('news_list')

    def get_queryset(self):
        return Post.objects.filter(type=Post.NEWS)


class ArticleCreateView(PermissionRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'news/news_form.html'
    success_url = reverse_lazy('article_list')

    def form_valid(self, form):
        author, created = Author.objects.get_or_create(user=self.request.user)
        post = form.save(commit=False)
        post.author = author
        post.type = Post.ARTICLE
        post.save()
        return super().form_valid(form)


class ArticleUpdateView(PermissionRequiredMixin, UpdateView):
    model = Post
    form_class = ArticleForm
    template_name = 'news/article_form.html'

    def get_queryset(self):
        return Post.objects.filter(type=Post.ARTICLE)


class ArticleDeleteView(DeleteView):
    model = Post
    template_name = 'news/article_confirm_delete.html'
    success_url = reverse_lazy('article_list')

    def get_queryset(self):
        return Post.objects.filter(type=Post.ARTICLE)


class ArticleDetailView(DetailView):
    model = Post
    template_name = 'news/article_detail.html'  # Укажите путь к шаблону
    context_object_name = 'article'