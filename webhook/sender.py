import json

from starlette.requests import Request

import settings
from api.webhooks_manager.models import webhooks_manager_repository
from webhook import mq

logger = settings.getLogger(__name__)


async def add_task(request, response):
    """
    Handles the processing of incoming webhook requests and responses by querying the
    webhooks manager repository, retrieving matching records based on specific criteria,
    and enqueueing information to a messaging queue for further processing. Operates
    asynchronously to support non-blocking operations.

    :param request: Incoming request object that contains details such as the
        URL path and HTTP method.
    :type request: Request
    :param response: Response object containing details such as HTTP status code
        related to the processed request.
    :type response: Response
    :return: None
    """
    query = {key: value for key, value in {
        "catch_path": request.url.path, "catch_method": request.method.upper(),
        "catch_status": response.status_code
    }.items() if value}

    ds = await webhooks_manager_repository.find_many(query=query, request=request)

    for d in ds:
        mq.enqueue(json.dumps({
            'endpoint': d['endpoint'],
            'request': request,
            'response': str(response),  # Use string representation of response
            'webhooks_manager_info': d,
            'retry_count': 0
        }))
        logger.debug("Added task to MQ: %s" % d)
