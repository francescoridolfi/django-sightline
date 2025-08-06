from django.db import models
from django.http.request import HttpRequest
from django.utils.translation import gettext_lazy as _

from sightline.models.base import BaseLog
from sightline.utils import get_ip_addr, get_user_agent, timestamp_to_str

import datetime


class VisitLogManager(models.Manager):

    def build(
        self,
        request: HttpRequest,
        timestamp: datetime.datetime
    ) -> "VisitLog":
        """
        Builds and returns a VisitLog instance populated with request and timestamp data.
        Args:
            request (HttpRequest): The HTTP request object containing user, path, and agent information.
            timestamp (datetime.datetime): The timestamp to associate with the visit log.
        Returns:
            VisitLog: A VisitLog instance with details from the request and timestamp.
        Notes:
            - If the user is authenticated, their instance and username are also recorded in the log.
        """
        
        log = VisitLog(
            timestamp=timestamp,
            raw_user_agent=get_user_agent(request),
            ip_address=get_ip_addr(request),
            path=request.path
        )

        if request.user.is_authenticated:
            log.user_instance = request.user
            log.user_username = request.user.username

        return log


class VisitLog(BaseLog):
    """
    Model representing a log entry for a user's visit to a specific path.
    Attributes:
        path (CharField): The URL path that was visited, with a maximum length of 255 characters.
    Inherits:
        BaseLog: Base model for logging actions.
    Usages:
        To generate a new visit log, use:

        VisitLog.objects.build(request, timestamp)

        This will create a VisitLog instance populated with details from the given request and timestamp.
    """

    class Meta:
        verbose_name = _("Visit Log")
        verbose_name_plural = _("Visit Logs")

    objects = VisitLogManager()

    path = models.CharField(
        verbose_name=_("Path"),
        max_length=255,
    )

    def __str__(self):
        return _("%(user)s visited path: %(path)s at %(datetime)s") % {
            "user": self.user_username if self.is_logged else _("Guest"),
            "path": self.path,
            "datetime": timestamp_to_str(self.timestamp)
        }
    
