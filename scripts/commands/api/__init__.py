"""
Connect to Stayforge API
"""
import os
from pathlib import Path

import click
import requests

from scripts import PROJECT_ROOT, get_config_value

ENV_KEYS = {}


def get_openapi_json(host: str = os.path.join(get_config_value('host'))):
    response = requests.get(host, 'openapi.json')
    response.raise_for_status()  # Raise an exception for bad status codes
    return response.json()


@click.command()
@click.option('--help', '-h', help="Show help for the current server Stayforge API version.")
def cli(output):
    click.echo(
        f"Scanning project root: {PROJECT_ROOT} for .env.sample generation."
    )

    output_path = Path(output)
    with open(output_path, "w") as f:
        for key in sorted(ENV_KEYS):
            f.write(f"{key}={ENV_KEYS[key]}\n")
    click.echo(f"Generated {output_path} with {len(ENV_KEYS)} keys.")
