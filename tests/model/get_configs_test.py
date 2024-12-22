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
from api.models_manager import Model
from api.models_manager.errors import ModelNotFoundError, ModelPathError
from mock_model import app as mock_model_app

script_path = os.path.dirname(os.path.abspath(__file__))


def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]


def run_mock_model(model_port, server_ready_event):
    logging.info(f"Starting Flask server on port {model_port}")
    logging.basicConfig(level=logging.DEBUG)
    try:
        mock_model_app.run(port=model_port, use_reloader=False)
        server_ready_event.set()
    except Exception as e:
        logging.error(f"Error while starting Flask server: {e}")
        server_ready_event.set()


class TestModelConfig(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model_port = find_free_port()
        cls.model_server_url = f'http://127.0.0.1:{cls.model_port}'
        cls.namespace = 'demo-namespace'
        cls.model_name = 'demo-model'
        cls.server_ready_event = multiprocessing.Event()

        cls.model_process = multiprocessing.Process(
            target=run_mock_model, args=(cls.model_port, cls.server_ready_event)
        )
        cls.model_process.start()

        config_file_path = os.path.join(script_path, 'model.yaml')
        if not os.path.exists(config_file_path):
            raise FileNotFoundError(f"{config_file_path} not found.")

        with open(config_file_path, 'r') as yaml_file:
            cls.config_data = yaml.safe_load(yaml_file)

        timeout = 20
        start_time = time.time()
        while not cls.server_ready_event.is_set():
            try:
                response = requests.get(f'{cls.model_server_url}/{cls.namespace}/{cls.model_name}/')
                if response.status_code == 200:
                    logging.info("Flask server responded successfully.")
                    cls.server_ready_event.set()
                    break
            except requests.RequestException as e:
                logging.debug(f"Server not ready yet: {e}")

            if time.time() - start_time > timeout:
                logging.error("Server did not respond within the timeout period.")
                raise Exception("Mock Flask model server did not start within timeout period")
            time.sleep(0.5)

        logging.info(f"Flask server started successfully on {cls.model_server_url}")

    @classmethod
    def tearDownClass(cls):
        if cls.model_process.is_alive():
            cls.model_process.terminate()
            cls.model_process.join(timeout=2)
            if cls.model_process.is_alive():
                logging.error("Model server did not shut down in time.")
                raise Exception("Model server did not shut down in time.")

    def test_get_by_model_full_url_success(self):
        model_url = f'{self.model_server_url}/{self.namespace}/{self.model_name}'
        logging.info(f"Model URL: {model_url}")
        model = Model(model_url=model_url)

        async def run_test():
            config = await model.get_model_configs()
            self.assertEqual(config, self.config_data)

        asyncio.run(run_test())

    def test_get_by_namespace_no_source_success(self):
        model_url = f'{self.namespace}/{self.model_name}'
        logging.info(f"Model URL: {model_url}")
        model = Model(
            model_url=model_url,
            default_source=self.model_server_url,
            default_namespace=self.namespace,
        )

        async def run_test():
            config = await model.get_model_configs()
            self.assertEqual(config, self.config_data)

        asyncio.run(run_test())

    def test_get_only_by_name_success(self):
        model_url = f'{self.model_name}'
        logging.info(f"Model URL: {model_url}")
        model = Model(
            model_url=model_url,
            default_source=self.model_server_url,
            default_namespace=self.namespace,
        )

        async def run_test():
            config = await model.get_model_configs()
            self.assertEqual(config, self.config_data)

        asyncio.run(run_test())

    def test_plg_not_exist(self):
        model_url = f'{faker.Faker().first_name()}-{faker.Faker().last_name()}'
        logging.info(f"Model URL: {model_url}")
        model = Model(
            model_url=model_url,
            default_source=self.model_server_url,
            default_namespace=self.namespace,
        )

        async def run_test():
            try:
                await model.get_model_configs()
            except ModelNotFoundError as e:
                logging.debug(f"Test Passed. Model {e} not found.")
            else:
                raise Exception("Cannot catch ModelNotFoundError.")

        asyncio.run(run_test())

    def test_plg_wrong_path(self):
        model_url = f'{faker.Faker().first_name()}/{faker.Faker().first_name()}/{faker.Faker().first_name()}'
        logging.info(f"Model URL: {model_url}")

        async def run_test():
            await model.get_model_configs()

        try:
            model = Model(
                model_url=model_url,
                default_source=self.model_server_url,
                default_namespace=self.namespace,
            )
            asyncio.run(run_test())
        except ModelPathError as e:
            logging.debug(f"Test Passed. Model {e} not found.")
