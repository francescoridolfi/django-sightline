from django.contrib import admin

from webapp.models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    pass