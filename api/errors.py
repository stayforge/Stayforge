import time

import settings
from api.schemas import BaseResponses

logger = settings.getLogger(__name__)


def handle_error(
        exception: Exception, str_time: float, custom_detail: str = None
):
    logger.error(exception, exc_info=True)
    return BaseResponses(
        status=500,
        detail=custom_detail if custom_detail else str(exception),
        used_time=time.perf_counter() - str_time,
        data=None
    ), 500


def handle_invalid_id_format_error(
        str_time: float
):
    return BaseResponses(
        status=400,
        detail="Invalid ID format",
        used_time=(time.perf_counter() - str_time) * 1000,
        data=None
    ), 400


def handle_resource_not_found_error(
        str_time: float, detail: str = "Resource not found"
):
    return BaseResponses(
        status=404,
        detail=detail,
        used_time=(time.perf_counter() - str_time) * 1000,
        data=None
    ), 404


def handle_after_write_resource_not_found_error(
        str_time: float,
        detail: str = "Resource maybe created/updated. But not found"
):
    return BaseResponses(
        status=409,
        detail=detail,
        used_time=(time.perf_counter() - str_time) * 1000,
        data=None
    ), 409
