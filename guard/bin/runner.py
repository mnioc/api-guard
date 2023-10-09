import os
import sys
import importlib.util
from typing import Any, Dict, Optional
from guard.http.client import HttpClient
from guard.logger import logger
from guard.usecase.loader import UseCaseLoader
from guard.usecase.evaluator import TestEvaluator
from guard.usecase.registry import registry


class Runner:

    """
    A class to run the test cases.

    Args:
        root_path (str): The root path of the test cases.
        client_path (str, optional): The path to the client. Defaults to None.
        prefix (str, optional): The prefix of the test cases. Defaults to None.

    """

    def __init__(
        self,
        root_path: str,
        client_path: Optional[str] = None,
        prefix: str | None = None,
    ) -> None:
        self.root_path = root_path
        self.client = self._get_or_create_client(client_path)
        self.cases = []
        self.evaluator = None
        self.prefix = prefix

    def _get_or_create_client(self, client_path: Optional[str] = None) -> HttpClient:
        if client_path is None:

            # if client_path is None, we assume that the client is in the root_path
            # and is named client.py
            # if it doesn't exist, we create a new client
            client_path = os.path.join(self.root_path, 'client.py')
            if not os.path.exists(client_path):
                return HttpClient()

        logger.info(f'Loading client from {client_path}...')
        spec = importlib.util.spec_from_file_location('client', client_path)
        result = importlib.util.module_from_spec(spec)
        # sys.modules['client'] = result
        _ = spec.loader.exec_module(result)

        # we assume that the client is the first HttpClient instance
        # in the client module
        # if it doesn't exist, we create a new client.
        for var_name in dir(result):
            if isinstance(client := getattr(result, var_name), HttpClient):
                return client

        logger.warning(f'No HttpClient instance found in {client_path}')
        logger.warning('Creating a new HttpClient instance.')
        return HttpClient()

    def add_case(self, case) -> None:
        """
        Add a test case to the runner.

        Args:
            case (dict): The test case.

        """
        self.cases.append(case)

    def extend_cases(self, cases: list) -> None:
        """
        Extend the test cases.

        Args:
            cases (list): The test cases.

        """
        self.cases.extend(cases)

    def auto_discover(self) -> None:
        logger.info(f'Auto discovering test cases in {self.root_path}...')
        if not os.path.exists(self.root_path):
            raise FileNotFoundError(f'No such directory: {self.root_path}')

        for root, _, files in os.walk(self.root_path):
            for file_name in files:

                if self.prefix is not None and not file_name.startswith(self.prefix):
                    continue

                # we assume that the test case is in the root_path
                # and is named test_*.py, test_*.yaml, test_*.excel
                if file_name.startswith("test_"):
                    file_path = os.path.join(root, file_name)
                    loader = UseCaseLoader.get_loader(file_path)
                    if loader is None:
                        continue
                    loader.load(self.client)
                    self.extend_cases(loader.usecases)

        self.extend_cases(registry.get_usecases())
        logger.info(f'Auto discovering test cases in {self.root_path} finished.')

    def run(self) -> None:
        self.auto_discover()
        for case in self.cases:
            if case.client is None and self.client is not None:
                case.client = self.client
            case.execute()
        self.evaluator = TestEvaluator(self.cases)
        self.evaluator.show_test_result()
