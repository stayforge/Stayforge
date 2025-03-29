import json

import click
import requests

from scripts.commands import api


@click.command()
def cli():
    """Show the OpenAPI specification for Stayforge API"""
    try:
        # Get the OpenAPI spec from the local server
        api.get_openapi_json()
        formatted_json = json.dumps(
            api.get_openapi_json(),
            indent=2, ensure_ascii=False
        )

        # Print the formatted JSON
        click.echo(formatted_json)

    except requests.exceptions.ConnectionError:
        click.echo("Could not connect to the Stayforge API server. Make sure the server is running.", err=True)
    except requests.exceptions.RequestException as e:
        click.echo(f"Error fetching OpenAPI specification: {e}", err=True)
    except json.JSONDecodeError:
        click.echo("Error parsing OpenAPI specification JSON", err=True)
