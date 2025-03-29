"""
.env.sample Generator
"""

import ast
import os
from pathlib import Path

import click
import pathspec

from scripts import PROJECT_ROOT

ENV_KEYS = set()


class GetenvVisitor(ast.NodeVisitor):
    def visit_Call(self, node):
        if (isinstance(node.func, ast.Attribute)
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id == "os"
                and node.func.attr == "getenv"):
            if len(node.args) >= 1 and isinstance(node.args[0], ast.Str):
                ENV_KEYS.add(node.args[0].s)
        self.generic_visit(node)

def load_gitignore_spec(root):
    gitignore_path = os.path.join(root, ".gitignore")
    if os.path.exists(gitignore_path):
        with open(gitignore_path) as f:
            return pathspec.PathSpec.from_lines("gitwildmatch", f)
    return pathspec.PathSpec.from_lines("gitwildmatch", [])

def scan_py_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            source = f.read()
            tree = ast.parse(source, filename=filepath)
            GetenvVisitor().visit(tree)
    except (SyntaxError, UnicodeDecodeError) as e:
        click.echo(f"Skip unresolved files: {filepath} ({type(e).__name__}: {e})", err=True)


def walk_project(path="."):
    spec = load_gitignore_spec(path)

    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if not spec.match_file(os.path.relpath(os.path.join(root, d), path))]
        for file in files:
            filepath = os.path.join(root, file)
            relpath = os.path.relpath(filepath, path)
            if file.endswith(".py") and not spec.match_file(relpath):
                scan_py_file(filepath)

@click.command()
@click.option('--output', '-o', default=".env.sample", help="Output file name.")
def cli(output):
    click.echo(
        f"Scanning project root: {PROJECT_ROOT} for .env.sample generation."
    )

    walk_project(path=str(PROJECT_ROOT))

    output_path = Path(output)
    with open(output_path, "w") as f:
        for key in sorted(ENV_KEYS):
            f.write(f"{key}=\n")
    click.echo(f"Generated {output_path} with {len(ENV_KEYS)} keys.")
