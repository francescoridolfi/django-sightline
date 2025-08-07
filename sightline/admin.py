from django.contrib import admin
from django.contrib.gis.geoip2 import GeoIP2
from django.http.request import HttpRequest
from django.db.models import Count
from django.db.models.functions import TruncDay
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from sightline.models import VisitLog
from sightline.settings import SIGHTLINE_GEOIP_SETTINGS
from sightline.utils import date_to_str

import json


class BaseLogAdmin(admin.ModelAdmin):
    change_list_template = "admin/dashboard.html"
    metrics_template = "fragments/metrics.html"

    def geo_data(self, request: HttpRequest):
        """
        Retrieves geographic coordinates for distinct IP addresses from model logs within a specified date interval.
        Args:
            request (HttpRequest): The HTTP request object.
        Returns:
            list: A list of dictionaries containing latitude ('lat') and longitude ('lon') for each IP address.
        Notes:
            - The date interval is determined by the 'marker_interval' setting in SIGHTLINE_GEOIP_SETTINGS.
            - Uses GeoIP2 to resolve city locations for IP addresses.
            - Handles exceptions during GeoIP2 lookup and provides a fallback for localhost IP.
        """

        g = GeoIP2()
        points = []

        interval_days = SIGHTLINE_GEOIP_SETTINGS.get("marker_interval", 10)
        start_date = timezone.now() - timezone.timedelta(days=interval_days)
        end_date = timezone.now() + timezone.timedelta(days=interval_days)
        
        queryset = self.model.objects \
                    .filter(timestamp__range=(start_date, end_date)) \
                    .values('ip_address') \
                    .distinct()

        for log in queryset:
            try:                
                location = g.city(log["ip_address"])
                points.append({
                    "lat": location["latitude"],
                    "lon": location["longitude"]
                })
            except Exception:
                if log["ip_address"] == "127.0.0.1":
                    points.append({
                        "lat": 41.9028,
                        "lon": 12.4964
                    }) # Roma regna

        return points

    def chart_queryset(self, request: HttpRequest, queryset):
        """
        Annotates the given queryset with daily aggregates.
        Groups the queryset by day (truncated from the 'timestamp' field), counts the number of occurrences of 'identifier' for each day,
        and returns a queryset ordered by day.
        Args:
            request: The current HttpRequest object.
            queryset: The initial queryset to be aggregated.
        Returns:
            QuerySet: A queryset annotated with 'day' and 'total' fields, ordered by 'day'.
        """

        return queryset.annotate(day=TruncDay("timestamp")) \
                .values("day") \
                .annotate(total=Count("identifier", distinct=True)) \
                .order_by("day")
    
    def chart_data(self, request: HttpRequest, queryset):
        """
        Generates chart data from a queryset for visualization purposes.
        Args:
            request: The HTTP request object.
            queryset: An iterable of dictionaries, each containing 'day' and 'total' keys.
        Returns:
            list: A list of dictionaries, each with:
                - 'label': A string representation of the date from 'day'.
                - 'value': The corresponding 'total' value.
        """

        return [
            {
                "label": date_to_str(d["day"]),
                "values": d["total"]
            }
            for d in queryset
        ]
    

    def metrics_builder(self, request: HttpRequest, queryset) -> list[dict]:
        """
        Builds a list of metrics dictionaries based on the provided queryset.
        Args:
            request (HttpRequest): The current HTTP request object.
            queryset: A Django queryset containing log entries with a 'total' field and a 'day' field.
        Returns:
            list[dict]: A list of dictionaries, each representing a metric:
                - "Today Logs": The total logs for the current day.
                - "Total Logs": The sum of all logs in the queryset.
        """

        metrics = []

        today_log = queryset.filter(day=TruncDay(timezone.now())).first()
        
        metrics.extend([
            {
                "name": _("Today Logs"),
                "value": today_log["total"] if today_log else 0
            },
            {
                "name": _("Total Logs"),
                "value": sum(log["total"] for log in queryset)
            }
        ])

        return metrics
    
    def metrics_render(self, request: HttpRequest, queryset):
        """
        Renders metrics for the given queryset using a specified template.
        Args:
            request (HttpRequest): The current HTTP request object.
            queryset: The queryset containing objects to compute metrics on.
        Returns:
            str: Rendered HTML string containing the metrics.
        """

        return render_to_string(
            self.metrics_template,
            {
                "metrics": self.metrics_builder(
                    request,
                    queryset
                )
            }
        )


    def changelist_view(self, request: HttpRequest, extra_context = {}):
        chart_queryset = self.chart_queryset(
            request,
            self.model.objects.all()
        )

        chart_data = self.chart_data(
            request,
            chart_queryset
        )

        extra_context = extra_context or {}

        extra_context["metrics"] = self.metrics_render(request, chart_queryset)

        extra_context["chart_data"] = json.dumps(chart_data)

        extra_context["use_geoip"] = SIGHTLINE_GEOIP_SETTINGS.get("enabled", False)

        if extra_context["use_geoip"]:
            
            extra_context["geo_points"] = json.dumps(
                self.geo_data(request)
            )

        return super().changelist_view(
            request,
            extra_context
        )


@admin.register(VisitLog)
class VisitLogAdmin(BaseLogAdmin):
    pass