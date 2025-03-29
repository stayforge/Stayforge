"""
Set Stayforge API host location
"""

import click

from scripts import set_config_value

_enter_stayforge_host_text = "Please enter the Stayforge API host (e.g. https://api.example.stayforge.io)"

def set_host(url):
    if not url:
        url = click.prompt(_enter_stayforge_host_text)

    if not url.startswith(("http://", "https://")):
        click.echo("Invalid host URL. Please ensure it starts with http:// or https://", err=True)
        return

    set_config_value("host", url)
    click.echo(f"The Stayforge API host has been set as: {url}")


@click.command()
@click.argument("url", required=False)
def cli(url):
    """Set Stayforge API host location"""
    set_host(url)