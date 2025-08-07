from django.urls import path
from webapp.views import ArticleListView, ArticleDetailView

app_name = "webapp"

urlpatterns = [
    path('', ArticleListView.as_view(), name="index"),
    path('article/<slug:slug>/', ArticleDetailView.as_view(), name="article")
]
