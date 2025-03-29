"""
Stayforge CIL
"""
import logging
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PACKAGE_DIR = Path(__file__).resolve().parent

logger = logging.getLogger("Stayforge CIL")

"""
CIL Configs
"""

import tomli
import tomli_w

CONFIG_DIR = Path.home() / ".stayforge"
CIL_CONFIG_FILE = CONFIG_DIR / "cil.toml"

def load_config(section: str = None):
    if CIL_CONFIG_FILE.exists():
        with open(CIL_CONFIG_FILE, "rb") as f:
            config = tomli.load(f)
        if section:
            return config.get(section, {})
        return config
    return {} if not section else {}

def save_config(data):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CIL_CONFIG_FILE, "w", encoding="utf-8") as f:
        f.write(tomli_w.dumps(data))

def get_config_value(key, default=None, section="cli"):
    section_data = load_config(section)
    return section_data.get(key, default)

def set_config_value(key, value, section="cli"):
    config = load_config()
    if section not in config:
        config[section] = {}
    config[section][key] = value
    save_config(config)
