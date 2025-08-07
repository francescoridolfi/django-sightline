from django.views.generic import ListView, DetailView

from webapp.models import Article


class ArticleListView(ListView):
    model = Article
    template_name = "index.html"
    context_object_name = "articles"
    ordering = ["-published_at"]


class ArticleDetailView(DetailView):
    model = Article
    template_name = "article.html"
    context_object_name = "article"
    slug_field = "slug"
    slug_url_kwarg = "slug"

