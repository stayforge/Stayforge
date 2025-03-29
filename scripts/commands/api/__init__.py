"""
Connect to Stayforge API via dynamically generated CLI based on OpenAPI
"""
from urllib.parse import urljoin

import click
import requests

from scripts import get_config_value


@click.group()
def cli():
    """Stayforge API CLI (auto-generated from OpenAPI spec)"""
    pass


def get_openapi_json():
    host = get_config_value("host")
    if not host.startswith("http"):
        host = "https://" + host
    url = urljoin(host, "/openapi.json")
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


# Automatically scan OpenAPI and register GET directives
try:
    spec = get_openapi_json()
    for path, methods in spec.get("paths", {}).items():
        for method, meta in methods.items():
            if method.lower() != "get":
                continue
            operation_id = meta.get("operationId") or path.strip("/").replace("/", "_")


            def make_command(endpoint_path):
                @click.command(name=operation_id)
                @click.option("--params", help="Query string like key=value&x=123")
                def command(params):
                    host = get_config_value("host")
                    url = urljoin(host, endpoint_path)
                    query = dict(p.split("=", 1) for p in params.split("&")) if params else {}
                    resp = requests.get(url, params=query)
                    click.echo(resp.text)

                return command


            cli.add_command(make_command(path))

except Exception as e:
    click.echo(f"[warn] Unable to load OpenAPI：{e}", err=True)
