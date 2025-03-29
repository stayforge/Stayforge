import json
import click
import requests
from scripts import get_config_value, logger
import os

@click.command()
def cli():
    """Show the OpenAPI specification for Stayforge API"""
    try:
        # Get the OpenAPI spec from the local server
        response = requests.get(os.path.join(get_config_value('host'), 'openapi.json'))
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Parse and format the JSON
        spec = response.json()
        formatted_json = json.dumps(spec, indent=2, ensure_ascii=False)
        
        # Print the formatted JSON
        print(formatted_json)
        
    except requests.exceptions.ConnectionError:
        logger.error("Could not connect to the Stayforge API server. Make sure the server is running.")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching OpenAPI specification: {e}")
    except json.JSONDecodeError:
        logger.error("Error parsing OpenAPI specification JSON") 