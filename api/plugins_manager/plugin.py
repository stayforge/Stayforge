# plugin.py
import re
import os
from typing import Any
from urllib.parse import urlparse

import httpx
import yaml
import logging

from requests import Response

from settings import *

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Plugin:
    def __init__(
            self,
            plugin_path: str,
            default_source: str = DEFAULT_PLUGIN_SOURCE,
            default_namespace: str = DEFAULT_PLUGIN_NAMESPACE
    ):
        # Compile regex for validation
        name_pattern = re.compile(r'^[a-z0-9\-]+$')

        # Extract parts from the path
        self.parts = plugin_path.strip('/').split('/')

        # If the path is too short, set source to default_source
        if len(self.parts) > 2:
            # The source URL is everything except the last two parts (namespace and repo)
            self.source_url = '/'.join(self.parts[:-2])
        else:
            # Use default source if namespace/repo are missing
            self.source_url = default_source

        # Determine namespace (penultimate part if available, else default)
        self.plugin_namespace = self.parts[-2].lower() if len(self.parts) > 1 else default_namespace

        # Determine plugin name (last part if available)
        self.plugin_name = self.parts[-1].lower() if len(self.parts) > 0 else None

        # Ensure source_url ends with a valid trailing slash (optional, depending on your URL format)
        if not self.source_url.endswith('/'):
            self.source_url += '/'

        # Validate source_url using urlparse
        parsed_url = urlparse(self.source_url)
        if not (parsed_url.scheme and parsed_url.netloc):
            raise ValueError(f"Invalid source URL in plugin path: {self.source_url}")

        # Validate plugin_namespace
        if not name_pattern.match(self.plugin_namespace):
            raise ValueError(f"Invalid plugin namespace (allowed: a-z0-9 or -): {self.plugin_namespace}")

        # Validate plugin_name
        if not self.plugin_name or not name_pattern.match(self.plugin_name):
            raise ValueError(f"Invalid or missing plugin name (allowed: a-z0-9 or -): {self.plugin_name}")

    async def _fetch_plugin_configs(self) -> Response:
        async with httpx.AsyncClient() as client:
            url = f"{os.path.join(self.source_url, self.plugin_namespace, self.plugin_name)}/"
            print(url)
            response = await client.get(url)
            if response.status_code not in [200, 308]:
                raise ValueError(f"Failed to fetch plugin config: {response.status_code}")
            return response

    async def get_plugin_configs(self) -> Any:
        response = await self._fetch_plugin_configs()
        return yaml.safe_load(response.text)
