# model.py
import re
from typing import Any
from urllib.parse import urlparse

import httpx
import yaml
from httpx import HTTPError

from requests import Response

from api.models_manager.errors import *
from settings import *

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Model:
    def __init__(
            self,
            model_url: str,
            default_source: str = DEFAULT_MODEL_SOURCE,
            default_namespace: str = DEFAULT_MODEL_NAMESPACE
    ):
        self.default_source = default_source
        self.default_namespace = default_namespace

        source, namespace, name = self.parse_url(model_url)

        self.source_url = source if source else self.default_source
        self.namespace = namespace if namespace else self.default_namespace
        self.name = name

        self.config_url = self.add_trailing_slash(f"{self.source_url}/{self.namespace}/{self.name}")

    @staticmethod
    def parse_url(input_str):
        def _trim_url(url):
            parsed_url = urlparse(url)
            path_parts = parsed_url.path.strip('/').split('/')
            trimmed_path = '/'.join(path_parts[:-2]) if len(path_parts) > 2 else ''
            trimmed_url = parsed_url._replace(path='/' + trimmed_path).geturl()

            return trimmed_url

        input_str = input_str.lower()

        # Check if the input is a complete URL
        url_pattern = re.compile(r'http(s)?://')
        if url_pattern.match(input_str):
            # Split the URL and check if it has at least two path segments
            parts = input_str.strip().split('/')[2:]  # Ignore the "http://model.exmaple.com"

            if len(parts) <= 2:
                raise ModelPathError("Complete URL must include `namespace/name`")

            # Extract source, namespace, and name from the path
            source = _trim_url(input_str)
            namespace = parts[-2] if len(parts) >= 1 else None
            name = parts[-1] if len(parts) >= 2 else None

            return source, namespace, name

        # Handle simple relative path cases (no "http://")
        parts = input_str.strip().split('/')
        parts = [part for part in parts if part not in (None, '', False)]

        # For len = 2 or 1 (valid cases), otherwise raise an error
        if len(parts) == 1:
            # If only one part, it's treated as name, and namespace is None
            source = None
            namespace = None
            name = parts[-1]
        elif len(parts) == 2:
            # If two parts, it's source and name, namespace is None
            source = None
            namespace = parts[-2]
            name = parts[-1]
        else:
            # Raise error if there are more than 2 parts in the relative path
            raise ModelPathError(
                f"Invalid path format: {parts}. For relative paths, the format must be `name` or `namespace/name`."
            )

        return (
            source if source not in (None, '', False) else None,
            namespace if namespace not in (None, '', False) else None,
            name
        )

    @staticmethod
    def add_trailing_slash(url):
        if url.endswith('/'):
            return url
        else:
            return url + '/'

    async def _fetch_model_configs(self) -> Response:
        async with httpx.AsyncClient() as client:
            url = self.config_url
            response = await client.get(url)
            if response.status_code in [200, 308]:
                return response
            elif response.status_code == 404:
                raise ModelNotFoundError(f"{response.status_code}, Model not found: {url}")
            else:
                raise Exception(f"{response.status_code}, Error: {response}")

    async def get_model_configs(self) -> Any:
        response = await self._fetch_model_configs()
        return yaml.safe_load(response.text)
