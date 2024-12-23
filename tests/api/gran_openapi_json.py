import unittest
import os
from app import export_openapi_json


class TestGenerateOpenapiFiles(unittest.TestCase):

    def setUp(self):
        # Setup logic to prepare for the test runs
        self.output_file = "_openapi.json"

    def tearDown(self):
        # Cleanup logic to run after each test
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

    def test_openapi_json_generation(self):
        # Call the function to test
        export_openapi_json(self.output_file)

        # Assert the file is created
        self.assertTrue(os.path.exists(self.output_file), "OpenAPI JSON file was not generated.")

        # Additional checks (if needed, e.g., file content validation)
        with open(self.output_file, 'r') as f:
            content = f.read()
            self.assertTrue(len(content) > 0, "Generated OpenAPI JSON file is empty.")


if __name__ == "__main__":
    unittest.main()