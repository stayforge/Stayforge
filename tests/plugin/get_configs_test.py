import unittest
import time

import faker
import requests
import socket
import os
import asyncio
import yaml
import logging
import multiprocessing
from api.plugins_manager import Plugin
from api.plugins_manager.errors import PluginNotFoundError, PluginPathError
from mock_plugin import app as mock_plugin_app

script_path = os.path.dirname(os.path.abspath(__file__))


def find_free_port():
    """Find an unused port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]


def run_mock_plugin(plugin_port, server_ready_event):
    """Start the Flask mock plugin."""
    logging.info(f"Starting Flask server on port {plugin_port}")
    logging.basicConfig(level=logging.DEBUG)  # Enable debug-level logging for Flask/werkzeug
    try:
        mock_plugin_app.run(port=plugin_port, use_reloader=False)
        server_ready_event.set()  # Signal that the server is ready
    except Exception as e:
        logging.error(f"Error while starting Flask server: {e}")
        server_ready_event.set()  # Ensure event is set in case of error


class TestPluginConfig(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test environment and start Flask plugin server."""
        cls.plugin_port = find_free_port()
        cls.plugin_server_url = f'http://127.0.0.1:{cls.plugin_port}'

        cls.namespace = 'demo-namespace'
        cls.plugin_name = 'demo-plugin'

        cls.server_ready_event = multiprocessing.Event()

        # Start Flask mock plugin server in a separate process
        cls.plugin_process = multiprocessing.Process(target=run_mock_plugin,
                                                     args=(cls.plugin_port, cls.server_ready_event))
        cls.plugin_process.start()

        # Load the configuration
        config_file_path = os.path.join(script_path, 'plugin.yaml')
        if not os.path.exists(config_file_path):
            raise FileNotFoundError(f"{config_file_path} not found.")

        with open(config_file_path, 'r') as yaml_file:
            cls.config_data = yaml.safe_load(yaml_file)

        # Wait for Flask mock plugin to start, with actual HTTP check
        timeout = 20  # Increased timeout to 20 seconds
        start_time = time.time()
        while not cls.server_ready_event.is_set():
            try:
                response = requests.get(f'{cls.plugin_server_url}/{cls.namespace}/{cls.plugin_name}/')
                if response.status_code == 200:
                    logging.info("Flask server responded successfully.")
                    cls.server_ready_event.set()
                    break
            except requests.exceptions.RequestException as e:
                logging.debug(f"Server not ready yet: {e}")

            if time.time() - start_time > timeout:
                logging.error("Server did not respond within the timeout period.")
                raise Exception("Mock Flask plugin server did not start within timeout period")
            time.sleep(0.5)

        logging.info(f"Flask server started successfully on {cls.plugin_server_url}")

    @classmethod
    def tearDownClass(cls):
        """Clean up and stop the mock plugin server."""
        if cls.plugin_process.is_alive():
            cls.plugin_process.terminate()  # Forcefully terminate the Flask process
            cls.plugin_process.join(timeout=2)
            if cls.plugin_process.is_alive():
                logging.error("Plugin server did not shut down in time.")
                raise Exception("Plugin server did not shut down in time.")

    def test_get_by_plugin_full_url_success(self):
        """Test successful reading of plugin configuration (Full URL)."""
        plugin_url = f'{self.plugin_server_url}/{self.namespace}/{self.plugin_name}'
        logging.info(f"Plugin URL: {plugin_url}")

        plugin = Plugin(plugin_url=plugin_url)

        async def run_test():
            """Run the async test."""
            config = await plugin.get_plugin_configs()
            self.assertEqual(config, self.config_data)

        # Run the async test
        asyncio.run(run_test())

    def test_get_by_namespace_no_source_success(self):
        """Test successful reading of plugin configuration (Namespace and Name)."""
        plugin_url = f'{self.namespace}/{self.plugin_name}'
        logging.info(f"Plugin URL: {plugin_url}")

        plugin = Plugin(
            plugin_url=plugin_url,
            default_source=self.plugin_server_url,
            default_namespace=self.namespace,
        )

        async def run_test():
            """Run the async test."""
            config = await plugin.get_plugin_configs()
            self.assertEqual(config, self.config_data)

        # Run the async test
        asyncio.run(run_test())

    def test_get_only_by_name_success(self):
        """Test successful reading of plugin configuration (Only name)."""
        plugin_url = f'{self.plugin_name}'
        logging.info(f"Plugin URL: {plugin_url}")

        plugin = Plugin(
            plugin_url=plugin_url,
            default_source=self.plugin_server_url,
            default_namespace=self.namespace,
        )

        async def run_test():
            """Run the async test."""
            config = await plugin.get_plugin_configs()
            self.assertEqual(config, self.config_data)

        # Run the async test
        asyncio.run(run_test())

    def test_plg_not_exist(self):
        """test a plugin not existence."""
        plugin_url = f'{faker.Faker().first_name()}-{faker.Faker().last_name()}'
        logging.info(f"Plugin URL: {plugin_url}")

        plugin = Plugin(
            plugin_url=plugin_url,
            default_source=self.plugin_server_url,
            default_namespace=self.namespace,
        )

        async def run_test():
            """Run the async test."""
            try:
                await plugin.get_plugin_configs()
            except PluginNotFoundError as e:
                logging.debug(f"Test Passed. Plugin {e} not found.")
            else:
                raise Exception("Cannot catch PluginNotFoundError.")

        # Run the async test
        asyncio.run(run_test())

    def test_plg_wrong_path(self):
        """test a plugin with wrong format."""
        plugin_url = f'{faker.Faker().first_name()}/{faker.Faker().first_name()}/{faker.Faker().first_name()}'
        logging.info(f"Plugin URL: {plugin_url}")

        async def run_test():
            """Run the async test."""
            await plugin.get_plugin_configs()

        try:
            plugin = Plugin(
                plugin_url=plugin_url,
                default_source=self.plugin_server_url,
                default_namespace=self.namespace,
            )
            # Run the async test
            asyncio.run(run_test())
        except PluginPathError as e:
            logging.debug(f"Test Passed. Plugin {e} not found.")
