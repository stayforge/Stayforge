import json
import yaml
import logging
import asyncio
import argparse
import os
from typing import Optional

import aiofiles

from app import app

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def export_openapi(_file_path: str, _format: str = "json"):
    try:
        api_spec = app.openapi()

        os.makedirs(os.path.dirname(_file_path), exist_ok=True)

        async with aiofiles.open(_file_path, "w", encoding="utf-8") as f:
            if _format == "json":
                await f.write(json.dumps(api_spec, indent=4))
            elif _format == "yaml":
                await f.write(yaml.dump(api_spec, sort_keys=False))
            else:
                raise ValueError("Unsupported format: only 'json' or 'yaml' allowed")

        logger.info(f"OpenAPI {_format.upper()} exported to {_file_path}")
    except Exception as e:
        logger.error(f"Failed to export OpenAPI {_format}: {e}")
        raise


async def main(output_dir: Optional[str] = ".openapi_spec"):
    json_path = os.path.join(output_dir, "openapi.json")
    yaml_path = os.path.join(output_dir, "openapi.yaml")

    await export_openapi(json_path, "json")
    await export_openapi(yaml_path, "yaml")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export FastAPI OpenAPI spec to JSON and YAML.")
    parser.add_argument(
        "--output-dir", type=str, default=".openapi_spec",
        help="Directory to save openapi.json and openapi.yaml"
    )
    args = parser.parse_args()

    asyncio.run(main(args.output_dir))