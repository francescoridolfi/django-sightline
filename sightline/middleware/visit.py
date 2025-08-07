from django.db.transaction import atomic
from django.core.exceptions import MiddlewareNotUsed
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.utils import timezone

from sightline.models import VisitLog
from sightline.settings import SIGHTLINE_VISIT_SETTINGS
from sightline.utils import time_compraration

import typing, logging, re

logger = logging.getLogger(__name__)

@atomic
def _save_log(log: VisitLog):
    try:
        log.save()
    except Exception as e:
        logger.error("Unable to save log due to error", e)


class VisitLogMiddleware:

    matcher = None

    def __init__(self, get_response: typing.Callable) -> None:
        if not SIGHTLINE_VISIT_SETTINGS.get("enabled", True):
            raise MiddlewareNotUsed("VisitLog is not enabled")
        
        self.get_response = get_response
        self.matcher = re.compile(SIGHTLINE_VISIT_SETTINGS.get("exclude_path", r"^/admin/"))

    def __call__(self, request: HttpRequest) -> typing.Optional[HttpResponse]:

        if self.matcher.match(request.path):
            return self.get_response(request)

        log: VisitLog = VisitLog.objects.build(
            request,
            timezone.now()
        )

        query = VisitLog.objects.filter(identifier=log.identifier)

        if not query.exists() or time_compraration(
            log.timestamp,
            query.last().timestamp,
            SIGHTLINE_VISIT_SETTINGS.get("interval_capturing", 5)
        ):
            _save_log(log)
        

        return self.get_response(request)
