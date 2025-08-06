from django.contrib import admin

from sightline.models import VisitLog

@admin.register(VisitLog)
class VisitLogAdmin(admin.ModelAdmin):
    pass