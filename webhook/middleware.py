from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class WebhooksMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 捕获请求内容
        body = await request.body()
        print(f"Request PATH: {request.url.path}")
        print(f"Request Method: {request.method}")
        print(f"Request Headers: {request.headers}")
        print(f"Request Body: {body.decode('utf-8')}")

        # 获取响应
        response = await call_next(request)

        # 捕获响应内容
        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk

        print(response)

        print(f"Response Status Code: {response.status_code}")
        print(f"Response Body: {response_body.decode('utf-8')}")

        # 返回新的响应
        return Response(
            content=response_body,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type,
        )