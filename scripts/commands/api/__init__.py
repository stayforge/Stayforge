"""
Connect to Stayforge API via dynamically generated CLI based on OpenAPI
"""
import json
from typing import Optional, Dict, Any, Tuple
from urllib.parse import urljoin

import click
import requests
from requests.adapters import HTTPAdapter
from tqdm import tqdm
from urllib3.util.retry import Retry

from scripts import get_config_value
from scripts.commands.update import get_local_openapi, get_server_openapi, compare_openapi_specs

# HTTP methods that support request body
METHODS_WITH_BODY = {'POST', 'PUT', 'PATCH'}


def create_retry_session() -> requests.Session:
    """Create a session with retry mechanism"""
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def get_file_size(response: requests.Response) -> Optional[int]:
    """Get file size from response headers"""
    content_length = response.headers.get('content-length')
    if content_length is not None:
        return int(content_length)
    return None


def make_request(
        method: str,
        url: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None
) -> Tuple[Optional[dict], Optional[int]]:
    """Make HTTP request with specified method"""
    session = create_retry_session()
    try:
        # Set default headers for methods with body
        if method in METHODS_WITH_BODY and headers is None:
            headers = {'Content-Type': 'application/json'}

        response = session.request(
            method=method,
            url=url,
            json=data if method in METHODS_WITH_BODY else None,
            data=data if method not in METHODS_WITH_BODY else None,
            headers=headers,
            params=params,
            stream=True
        )
        response.raise_for_status()
        file_size = get_file_size(response)
        return response.json(), file_size
    except requests.exceptions.RequestException as e:
        raise APIError(f"Error making {method} request: {e}")


class APIError(Exception):
    """Base exception for API errors"""
    pass


@click.group()
def cli():
    """Stayforge API CLI (auto-generated from OpenAPI spec)"""
    pass


def get_openapi_json():
    """Get OpenAPI specification from server and compare with local version"""
    server_spec = get_server_openapi()
    
    # Compare with local spec
    local_spec = get_local_openapi()
    if local_spec and not compare_openapi_specs(local_spec, server_spec):
        click.echo("[warn] Local OpenAPI specification is out of date. Please run 'stayforge update' to update it.", err=True)
    
    return server_spec


# Automatically scan OpenAPI and register commands
try:
    spec = get_openapi_json()
    for path, methods in spec.get("paths", {}).items():
        for method, meta in methods.items():
            operation_id = meta.get("operationId") or path.strip("/").replace("/", "_")
            method = method.upper()

            def make_command(endpoint_path, http_method):
                @click.command(name=operation_id)
                @click.option("--method", "-m", default=http_method,
                              type=click.Choice(['GET', 'POST', 'PUT', 'DELETE', 'PATCH']),
                              help='HTTP request method')
                @click.option("--data", "-d", help="JSON data to send with the request")
                @click.option("--headers", "-H", help="Additional headers to send with the request")
                @click.option("--params", "-p", help="Query parameters to send with the request")
                def command(method, data, headers, params):
                    try:
                        # Parse input data
                        request_data = json.loads(data) if data else None
                        request_headers = json.loads(headers) if headers else None
                        request_params = json.loads(params) if params else None

                        # Make request
                        host = get_config_value("host")
                        if not host.startswith("http"):
                            host = "https://" + host
                        url = urljoin(host, endpoint_path)

                        spec, file_size = make_request(
                            method=method,
                            url=url,
                            data=request_data,
                            headers=request_headers,
                            params=request_params
                        )

                        if spec:
                            if file_size:
                                with tqdm(
                                        total=file_size,
                                        desc="Response",
                                        unit='B',
                                        unit_scale=True,
                                        unit_divisor=1024
                                ) as pbar:
                                    click.echo(json.dumps(spec, indent=2, ensure_ascii=False))
                                    pbar.update(file_size)
                            else:
                                click.echo(json.dumps(spec, indent=2, ensure_ascii=False))
                    except json.JSONDecodeError as e:
                        click.echo(f"Error parsing JSON data: {e}", err=True)
                    except APIError as e:
                        click.echo(str(e), err=True)
                    except Exception as e:
                        click.echo(f"Unexpected error: {e}", err=True)

                return command

            cli.add_command(make_command(path, method))

except Exception as e:
    click.echo(f"[warn] Unable to load OpenAPI: {e}", err=True)
