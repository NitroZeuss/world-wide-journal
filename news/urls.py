from django.urls import path
from . import views

urlpatterns = [
    path("search-news/", views.search_news, name="search_news"),
    path("top-news/", views.top_news, name="top_news"),
    path("search-sources/", views.search_news_sources, name="search_news_sources"),
]
