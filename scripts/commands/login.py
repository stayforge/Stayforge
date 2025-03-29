"""
Set the Service Account to use when logging in to the Stayforge API
"""
from urllib.parse import urljoin

import click
import requests

from scripts import set_config_value, get_config_value
from scripts.commands.host import set_host


def verify_account(account=None, secret=None, super_token=None):
    """Verify the account or super_token with the Stayforge API."""
    click.echo("Verifying account...")
    try:
        host = get_config_value("host", default=None)
        if not host:
            click.echo("No API host configured. Please set the host first.")
            set_host(
                url=click.prompt(host._enter_stayforge_host_text)
            )
            if not host:
                click.echo("Host is still not set. Aborting.", err=True)
                return False

        if not host.startswith(("http://", "https://")):
            click.echo("Invalid host URL. Please ensure it starts with http:// or https://", err=True)
            return False

        # Determine the payload based on provided inputs
        endpoint = "/auth/authenticate"
        payload = {"super_token": super_token} if super_token else {
            "account": account,
            "secret": secret,
        }

        resp = requests.post(
            urljoin(host, endpoint),
            json=payload,
            timeout=5
        )
        if resp.status_code != 200:
            try:
                detail = resp.json().get("detail", "Account verification failed")
            except Exception:
                detail = resp.text.strip() or "Account verification failed (non-JSON response)"
            click.echo(f"Account verification failed: {detail}", err=True)
            return False

        data = resp.json()
        if not data.get("access_token"):
            click.echo("Verification failed, access_token was not obtained", err=True)
            return False

        set_config_value("access_token", data["access_token"])
        set_config_value("refresh_token", data["refresh_token"])
        return True

    except Exception as e:
        click.echo(f"Unable to connect to the server to verify the account: {e}", err=True)
        return False


@click.command()
@click.argument("account", required=False)
@click.option("--secret", "-p", required=False, hide_input=True, help="Account secret or password.")
@click.option("--no-validate", is_flag=True, default=False, help="Skip the account verification request.")
@click.option("--super-token", help="Provide a SUPER_TOKEN for privileged authentication.", required=False)
def cli(account, secret, no_validate, super_token):
    """Set up Stayforge credentials for your environment for subsequent operations."""

    # Check for priority for super_token
    if super_token:
        click.echo("Super Token provided; skipping account and secret prompts.")
        account = None
        secret = None
    else:
        # If there is no super_token, please enter your account and secret
        if not account:
            account = click.prompt("Service Account")
        if not secret:
            secret = click.prompt("Secret (or Password)", hide_input=True)

    # If verification is required
    if not no_validate:
        if not verify_account(account, secret, super_token):
            return

    # Set up configuration
    if account:
        set_config_value("account", account)
    if secret:
        set_config_value("secret", secret)

    # Output service information
    click.echo(f"Service Account has been set：`{account or 'super_token@role.auth.stayforge.io'}`")
