"""
.env.sample Generator
"""

import ast
import os
import uuid
from pathlib import Path

import click
import pathspec

from scripts import PROJECT_ROOT

ENV_KEYS = {}

class GetenvVisitor(ast.NodeVisitor):
    def visit_Call(self, node):
        if (isinstance(node.func, ast.Attribute)
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id == "os"
                and node.func.attr == "getenv"):
            if len(node.args) >= 1 and isinstance(node.args[0], ast.Str):
                var_name = node.args[0].s
                default = ""
                if len(node.args) >= 2:
                    default_node = node.args[1]
                    if isinstance(default_node, ast.Str):
                        default = default_node.s
                    elif isinstance(default_node, ast.Constant) and isinstance(default_node.value, str):
                        default = default_node.value
                    elif isinstance(default_node, ast.Call):
                        # 嘗試執行簡單的像 uuid.uuid4()
                        try:
                            if (isinstance(default_node.func, ast.Attribute)
                                    and isinstance(default_node.func.value, ast.Name)
                                    and default_node.func.value.id == "uuid"):
                                func = getattr(uuid, default_node.func.attr)
                                default = str(func())
                        except Exception as e:
                            default = ""
                ENV_KEYS[var_name] = default
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
            f.write(f"{key}={ENV_KEYS[key]}\n")
    click.echo(f"Generated {output_path} with {len(ENV_KEYS)} keys.")
