"""
Stayforge CLI
"""

import click
import importlib
import pkgutil

from scripts import PACKAGE_DIR

package_dir = PACKAGE_DIR / "commands"
package_name = "scripts.commands"

@click.group()
def main():
    """Stayforge CLI Tool"""
    pass

def register_commands():
    for _, module_name, _ in pkgutil.iter_modules([str(package_dir)]):
        module = importlib.import_module(f"{package_name}.{module_name}")
        if hasattr(module, "cli"):
            main.add_command(module.cli, name=module_name.replace("_", "-"))

register_commands()

if __name__ == "__main__":
    main()
