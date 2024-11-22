"""
URL configuration for NewsPaper project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from .views import (
    news_list, news_detail, news_search,
    ArticleListView, NewsCreateView, NewsUpdateView, NewsDeleteView,
    ArticleCreateView, ArticleUpdateView, ArticleDeleteView, ArticleDetailView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.news_list, name='news_list'),
    path('accounts/', include('allauth.urls')),

    path('news/', news_list, name='news_list'),
    path('news/<int:news_id>/', news_detail, name='news_detail'),
    path('news/search/', news_search, name='news_search'),
    path('news/<int:news_id>/', news_detail, name='news_detail'),

    # CRUD для новостей
    path('news/create/', NewsCreateView.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', NewsUpdateView.as_view(), name='news_update'),
    path('news/<int:pk>/delete/', NewsDeleteView.as_view(), name='news_delete'),

    # CRUD для статей
    path('articles/', ArticleListView.as_view(), name='article_list'),
    path('articles/create/', ArticleCreateView.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', ArticleUpdateView.as_view(), name='article_update'),
    path('articles/<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
    path('articles/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),

    path('subscriptions/', views.subscriptions_view, name='subscriptions'),
]
