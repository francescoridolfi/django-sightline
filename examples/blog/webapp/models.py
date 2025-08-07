from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

class Article(models.Model):

    class Meta:
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")

    title = models.CharField(
        verbose_name=_("Title"),
        max_length=150,
    )

    slug = models.SlugField(unique=True)

    published_at = models.DateTimeField(
        verbose_name=_("Published At"),
        auto_now_add=True,
    )

    content = models.TextField(
        verbose_name=_("Content")
    )

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("webapp:article", kwargs={"slug": self.slug})
    

