import json
import os
from pathlib import Path
from typing import Optional
from urllib.parse import urljoin

import click
import requests
from tqdm import tqdm

from scripts import get_config_value

# Path to local OpenAPI spec
CONFIG_DIR = Path(os.path.expanduser("~/.stayforge"))
LOCAL_OPENAPI_PATH = CONFIG_DIR / "openapi.json"


def get_file_size(response: requests.Response) -> int:
    """Get file size from response headers"""
    content_length = response.headers.get('content-length')
    if content_length is not None:
        return int(content_length)
    return 0


def compare_openapi_specs(local_spec: dict, server_spec: dict) -> bool:
    """Compare local and server OpenAPI specs"""
    # Compare version and paths
    if local_spec.get("info", {}).get("version") != server_spec.get("info", {}).get("version"):
        return False
    if set(local_spec.get("paths", {}).keys()) != set(server_spec.get("paths", {}).keys()):
        return False
    return True


def get_local_openapi() -> Optional[dict]:
    """Get local OpenAPI specification"""
    try:
        if LOCAL_OPENAPI_PATH.exists():
            with open(LOCAL_OPENAPI_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception:
        pass
    return None


def get_server_openapi() -> dict:
    """Get OpenAPI specification from server"""
    host = get_config_value('host')
    if not host.startswith("http"):
        host = "https://" + host
    url = urljoin(host, '/openapi.json')

    response = requests.get(url, stream=True)
    response.raise_for_status()

    return response.json()


@click.command()
def cli():
    """Update the OpenAPI specification for Stayforge API"""
    try:
        # Get the OpenAPI spec from the server
        spec = get_server_openapi()
        file_size = len(json.dumps(spec, indent=2, ensure_ascii=False))

        # Save with progress bar
        with tqdm(
                total=file_size,
                desc="Updating OpenAPI specification",
                unit='B',
                unit_scale=True,
                unit_divisor=1024
        ) as pbar:
            formatted_json = json.dumps(spec, indent=2, ensure_ascii=False)
            LOCAL_OPENAPI_PATH.parent.mkdir(parents=True, exist_ok=True)
            with open(LOCAL_OPENAPI_PATH, 'w', encoding='utf-8') as f:
                f.write(formatted_json)
                pbar.update(file_size)
            click.echo("OpenAPI specification has been updated successfully")

    except requests.exceptions.ConnectionError:
        click.echo("Could not connect to the Stayforge API server. Make sure the server is running.", err=True)
    except requests.exceptions.RequestException as e:
        click.echo(f"Error fetching OpenAPI specification: {e}", err=True)
    except json.JSONDecodeError:
        click.echo("Error parsing OpenAPI specification JSON", err=True)
    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)
