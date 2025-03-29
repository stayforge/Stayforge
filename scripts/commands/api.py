"""
Connect to Stayforge API
"""

import ast
import os
import uuid
from pathlib import Path

import click
import pathspec

from scripts import PROJECT_ROOT

ENV_KEYS = {}


@click.command()
@click.option('--output', '-o', default=".env.sample", help="Output file name.")
def cli(output):
    click.echo(
        f"Scanning project root: {PROJECT_ROOT} for .env.sample generation."
    )


    output_path = Path(output)
    with open(output_path, "w") as f:
        for key in sorted(ENV_KEYS):
            f.write(f"{key}={ENV_KEYS[key]}\n")
    click.echo(f"Generated {output_path} with {len(ENV_KEYS)} keys.")
