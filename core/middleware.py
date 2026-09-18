import logging
import uuid
from datetime import datetime

logger = logging.getLogger("core")


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        request.request_id = request_id
        start = datetime.utcnow()
        response = self.get_response(request)
        duration = (datetime.utcnow() - start).total_seconds() * 1000
        response["X-Request-ID"] = request_id
        logger.info(
            "request_id=%s method=%s path=%s status=%s duration_ms=%s",
            request_id,
            request.method,
            request.path,
            getattr(response, "status_code", 0),
            round(duration, 2),
        )
        return response
