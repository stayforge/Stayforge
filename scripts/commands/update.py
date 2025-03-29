import json
from pathlib import Path
from urllib.parse import urljoin
from typing import Optional, Tuple

import click
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from tqdm import tqdm

from scripts import CONFIG_DIR, get_config_value

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

def fetch_openapi_spec(url: str) -> Tuple[Optional[dict], Optional[int]]:
    """Fetch OpenAPI specification from the server"""
    session = create_retry_session()
    try:
        response = session.get(url, stream=True)
        response.raise_for_status()
        file_size = get_file_size(response)
        return response.json(), file_size
    except requests.exceptions.RequestException as e:
        click.echo(f"Error fetching OpenAPI specification: {e}", err=True)
        return None, None

def save_openapi_spec(spec: dict, output_path: Path) -> bool:
    """Save OpenAPI specification to file"""
    try:
        formatted_json = json.dumps(spec, indent=2, ensure_ascii=False)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(formatted_json)
        return True
    except (IOError, TypeError) as e:
        click.echo(f"Error saving OpenAPI specification: {e}", err=True)
        return False

@click.command()
def cli():
    """Update the OpenAPI specification for Stayforge API"""
    try:
        api_url = urljoin(get_config_value('host'), '/openapi.json')
        output_path = CONFIG_DIR / 'openapi.json'

        # Fetch specification
        spec, file_size = fetch_openapi_spec(api_url)
        if not spec:
            return 1

        # Save specification with progress bar
        if file_size:
            with tqdm(
                total=file_size,
                desc="Saving OpenAPI specification",
                unit='B',
                unit_scale=True,
                unit_divisor=1024
            ) as pbar:
                formatted_json = json.dumps(spec, indent=2, ensure_ascii=False)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(formatted_json)
                    pbar.update(file_size)
                click.echo(f"OpenAPI specification has been saved to {output_path}")
        else:
            # Fallback to simple save if file size is not available
            if save_openapi_spec(spec, output_path):
                click.echo(f"OpenAPI specification has been saved to {output_path}")
            else:
                return 1

        return 0

    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)
        return 1
