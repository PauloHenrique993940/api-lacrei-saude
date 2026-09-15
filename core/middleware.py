import logging
from datetime import datetime

logger = logging.getLogger("core")


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = datetime.utcnow()
        response = self.get_response(request)
        duration = (datetime.utcnow() - start).total_seconds() * 1000
        logger.info(
            "%s %s %s %s ms",
            request.method,
            request.path,
            getattr(response, "status_code", 0),
            round(duration, 2),
        )
        return response
