import json
import logging
from datetime import timezone, datetime

import httpx

from api.webhooks_manager.models import webhooks_manager_repository, webhook_logger_repository
from settings import logger

WEBHOOK_FORMAT = {
    "content": "",
    "username": "StayForge",
    "avatar_url": "https://avatars.githubusercontent.com/u/183347404",
    "attachments": [
        {
            "title": "StayForge",
            "text": "Text",
            "color": "#36a64f",
            "fields": [
                {
                    "title": "key1",
                    "value": "value1",
                    "short": True
                }
            ]
        }
    ],
    "embeds": [
        {
            "title": "Stayforge Webhook",
            "description": "Stayforge Webhook",
            "url": "https://stayforge.io",
            "color": 16711680,
            "fields": [
                {
                    "name": "key2",
                    "value": "value2"
                }
            ]
        }
    ]
}


async def worker(request, response):
    query = {key: value for key, value in {
        "catch_path": request.url.path, "catch_method": request.method.upper(),
        "catch_status": response.status_code
    }.items() if value}

    ds = await webhooks_manager_repository.find_many(query=query, request=request)

    for d in ds:
        logger.debug(d)
        webhook_response = send(d['endpoint'], request, response)
        logger.debug(webhook_response)
        await webhook_logger_repository.insert_one(webhook_response, request=request)


def send(endpoint, request, response):
    logger.info(f'Sending webhook to {endpoint}')
    data = WEBHOOK_FORMAT.copy()
    data["content"] = f"Got a request from {request.url.path} {request.method.upper()} {response.status_code}"

    data = WEBHOOK_FORMAT.copy()
    data["content"] = f"Got a request from {request.url.path} {request.method.upper()} {response.status_code}"

    data["embeds"][0]["title"] = request.url.path
    data["embeds"][0]["description"] = f"Method: {request.method.upper()} Status Code: {response.status_code}"
    data["embeds"][0]["fields"][0]["name"] = "Request Headers"
    data["embeds"][0]["fields"][0]["value"] = str(request.headers)
    data["attachments"][0]["title"] = "Stayforge Webhook"
    data["attachments"][0]["title"] = data["embeds"][0]["title"]
    data["attachments"][0]["fields"][0]["title"] = "Response Headers"
    data["attachments"][0]["fields"][0]["value"] = str(response.headers)

    webhook_response = httpx.post(endpoint, json=data)

    return {
        "status": webhook_response.status_code,
        "target": str(webhook_response.request.url),
        "send_at": datetime.now(timezone.utc),
        "send": data,
        "got": {
            'header': webhook_response.headers,
            'json': webhook_response.text,
            'status_code': webhook_response.status_code
        }
    }
