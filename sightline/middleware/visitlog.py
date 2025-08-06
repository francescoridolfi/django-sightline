from django.db.transaction import atomic
from django.core.exceptions import MiddlewareNotUsed
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.utils import timezone

from sightline.models import VisitLog
from sightline.settings import SIGHTLINE_VISIT_SETTINGS
from sightline.utils import time_compraration

import typing, logging

logger = logging.getLogger(__name__)

@atomic
def _save_log(log: VisitLog):
    try:
        log.save()
    except Exception as e:
        logger.error("Unable to save log due to error", e)


class VisitLogMiddleware:

    def __init__(self, get_response: typing.Callable) -> None:
        if not SIGHTLINE_VISIT_SETTINGS["enabled"]:
            raise MiddlewareNotUsed("VisitLog is not enabled")
        
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> typing.Optional[HttpResponse]:
        log: VisitLog = VisitLog.objects.build(
            request,
            timezone.now()
        )

        query = VisitLog.objects.filter(identifier=log.identifier)

        if not query.exists() or time_compraration(
            log.timestamp,
            query.last().timestamp,
            SIGHTLINE_VISIT_SETTINGS["interval_capturing"]
        ):
            _save_log(log)
        

        return self.get_response(request)
