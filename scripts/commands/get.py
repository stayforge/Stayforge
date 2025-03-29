"""
Get something you need.
"""
import sys
from urllib.parse import urljoin

import click
import requests

from scripts import get_config_value, CIL_CONFIG_FILE


def authenticate_and_tokens():
    """
    Authenticate with the server and return tokens (both access and refresh).
    """
    host = get_config_value('host')
    if not host:
        click.echo(
            "Error: No host configured. Please use the command `stayforge host` to set your host information.",
            err=True
        )
        sys.exit(1)

    url = urljoin(
        host,
        "/auth/authenticate"
    )

    click.echo(f"Attempting to authenticate with the server at `{url}`...")

    try:
        super_token = get_config_value('super_token', default=None)
        if super_token:
            click.echo(
                "Warning: Using SUPER_TOKEN for authentication. This is not recommended and may lead to "
                "unauthorized access to the Stayforge API."
            )
            data = {
                'super_token': super_token,
            }
        else:
            data = {
                "account": get_config_value('account'),
                "secret": get_config_value('password')
            }

        response = requests.post(url, json=data)
        response.raise_for_status()
        tokens = response.json()

        if "access_token" in tokens and "refresh_token" in tokens:
            return tokens
        else:
            click.echo("Error: Server response does not contain required tokens.", err=True)
            sys.exit(1)

    except requests.exceptions.ConnectionError:
        click.echo("Unable to connect to the server. Please check your network or server URL.", err=True)
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        click.echo(f"Error during authentication: {e}", err=True)
        sys.exit(1)


@click.group()
def cli():
    """Quickly obtain tokens, configuration files and other information"""
    pass


@cli.command()
def accesstoken():
    """Retrieve and display a new Access Token."""
    tokens = authenticate_and_tokens()
    access_token = tokens.get("access_token")
    if access_token:
        click.echo(click.style(f"New Access Token:\n{access_token}", fg="green"))
    else:
        click.echo("Error: Unable to retrieve Access Token.", err=True)
        sys.exit(1)


@cli.command()
def refreshtoken():
    """Retrieve and display the latest Refresh Token."""
    tokens = authenticate_and_tokens()
    refresh_token = tokens.get("refresh_token")
    if refresh_token:
        click.echo(click.style(f"New Refresh Token:\n{refresh_token}", fg="blue"))
    else:
        click.echo("Error: Unable to retrieve Refresh Token.", err=True)
        sys.exit(1)


@cli.command()
def cli_config():
    """Retrieve and display the CLI configuration content on `~/.stayforge/cil.toml`."""
    try:
        with open(CIL_CONFIG_FILE, 'r') as config_file:
            config_data = config_file.read()
        click.echo(config_file.name)
        click.echo("=" * len(config_file.name))
        click.echo(config_data)


    except FileNotFoundError:
        click.echo("Error: Configuration file not found.", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Unexpected Error: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    cli()
