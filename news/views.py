from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

from django.contrib.auth.decorators import login_required

from .models import Post, News, Author, Category, Subscriber
from .forms import NewsForm, ArticleForm, PostForm
from .filters import NewsFilter
from django.urls import reverse

from django.utils.timezone import now
from django.core.mail import send_mail
from datetime import timedelta

from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator


@cache_page(60 * 5)
def news_list(request):
    news_list = News.objects.all()
    paginator = Paginator(news_list, 10)  # 10 новостей на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'news/news_list.html', {'page_obj': page_obj})


@cache_page(60)
def news_detail(request, news_id):
    news_item = get_object_or_404(News, pk=news_id)
    print(News.objects.filter(pk=25).exists())
    return render(request, 'news/news_detail.html', {'news_item': news_item})


def news_search(request):
    news = News.objects.all()
    news_filter = NewsFilter(request.GET, queryset=news)
    return render(request, 'news/news_search.html', {'filter': news_filter})


@method_decorator(cache_page(60 * 60, key_prefix=lambda request, view: f"article_{view.get_object().pk}_{view.get_object().updated_at.timestamp()}"), name='dispatch')
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
    permission_required = 'news.add_post'

    def form_valid(self, form):
        author, created = Author.objects.get_or_create(user=self.request.user)
        post = form.save(commit=False)
        post.author = author
        post.type = Post.NEWS
        post.save()
        print(Post.objects.last())
        print(f"Created post ID: {post.pk}")
        return redirect(reverse('news_detail', args=[post.pk]))

    def form_invalid(self, form):
        print(form.errors)  # Для отладки
        return super().form_invalid(form)


class NewsUpdateView(PermissionRequiredMixin, UpdateView):
    model = Post
    form_class = NewsForm
    template_name = 'news/news_form.html'
    success_url = reverse_lazy('news_list')

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


@login_required
def subscriptions_view(request):
    user = request.user
    categories = Category.objects.all()

    if request.method == 'POST':
        selected_categories = request.POST.getlist('categories')
        Subscriber.objects.filter(user=user).delete()  # Удаляем все текущие подписки
        for category_id in selected_categories:
            category = Category.objects.get(id=category_id)
            Subscriber.objects.create(user=user, category=category)

        return redirect('subscriptions')

    subscribed_categories = user.subscriptions.all().values_list('category__id', flat=True)
    return render(request, 'subscriptions.html', {'categories': categories, 'subscribed_categories': subscribed_categories})


def send_weekly_news():
    last_week = now() - timedelta(days=7)
    subscribers = Subscriber.objects.all()

    for subscriber in subscribers:
        articles = Post.objects.filter(
            categories__in=subscriber.categories.all(),
            published_date__gte=last_week
        ).distinct()

        if articles:
            article_links = "\n".join([f"http://127.0.0.1:8000/articles/{article.id}/" for article in articles])
            send_mail(
                subject='Weekly news digest',
                message=f'Here are the latest articles:\n{article_links}',
                from_email='admin@newsportal.com',
                recipient_list=[subscriber.user.email],
            )