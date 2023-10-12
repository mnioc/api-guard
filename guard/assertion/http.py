from typing import Any
from requests.models import Response
from guard.assertion.bases import Assertion
from requests.exceptions import JSONDecodeError
from jsonpath_rw import parse
from guard.assertion.operator import operator_map, operator_range_map
from guard.http.hooks import show_response_table
from guard.logger import logger


def get_json_path_value(response: Response, json_path: str) -> Any:
    try:
        data = response.json()
    except JSONDecodeError as e:
        raise AssertionError('Assertion failed: invalid JSON response.') from e

    json_path_parser = parse(json_path)

    return match[0].value if (match := json_path_parser.find(data)) else None


class AssertHttpStatusCodeEqual(Assertion):
    """
    Assert HTTP status code equal.

    Args:
        expected_status_code (int): Expected status code.

    Examples:
        >>> from guard.assertion.http import AssertHttpStatusCodeEqual
        >>> from guard.http.client import HttpClient
        >>> response = HttpClient().get('http://xxx.com')
        >>> AssertHttpStatusCodeEqual(200)(response)
    """

    _name = 'AssertHttpStatusCodeEqual'
    _error_message: str = 'Assertion failed: invalid status code. Expected {expected_status_code}, but got {code}.'

    def __init__(self, expected_status_code: int) -> None:
        self.expected_status_code = expected_status_code

    def __call__(self, response) -> None:
        if response.status_code != self.expected_status_code:
            raise AssertionError(self._error_message.format(
                expected_status_code=self.expected_status_code,
                code=response.status_code
            ))


class AssertHttpResponseValue(Assertion):

    """
    Assert HTTP response value.

    Args:
        json_path (str): JSON path.
        operator (operator): Operator.
            e.g.
                ==, !=, >, <, >=, <=, in, not in, is, is not...
        expected_value (Any): Expected value.
        assertion (Assertion): Assertion.

    Examples:
        >>> from guard.assertion.http import AssertHttpResponseValue
        >>> from guard.http.client import HttpClient
        >>> response = HttpClient().get('http://xxx.com')
        >>> AssertHttpResponseValue('$.data.id', '==', '000000')(response)

        # if {'data': {'id': '000000'}} not in response.json():
        # raise AssertionError('Assertion failed: invalid value. Expected 000000, but got {value}.')

    """
    def __init__(self, json_path: str, operator, expected_value: Any) -> None:
        self.json_path = json_path
        self.expected_value = expected_value
        self.operator = operator

    def __call__(self, response: Response) -> Any:
        value = get_json_path_value(response, self.json_path)
        if self.operator not in operator_map:
            raise KeyError(f'Operator {self.operator} is not supported.')

        if not operator_map[self.operator](value, self.expected_value):
            raise AssertionError(f'Assertion failed: {value} {self.operator} {self.expected_value} is False.')


class AssertHttpResponseListItem(Assertion):

    def __init__(
        self,
        json_path: str,
        operator_range: str,
        operator: str,
        expected_value: int,
    ) -> None:
        self.json_path = json_path
        self.expected_value = expected_value
        assert operator_range in operator_range_map, f'Operator range {operator_range} is not supported.'
        self.operator_range = operator_range
        assert operator in operator_map, f'Operator {operator} is not supported.'
        self.operator = operator

    def __call__(self, response: Response) -> Any:
        value = get_json_path_value(response, self.json_path)
        if self.operator not in operator_map:
            raise KeyError(f'Operator {self.operator} is not supported.')

        if not operator_range_map[self.operator_range](self.expected_value, self.operator, value):
            raise AssertionError(f'Assertion failed: {self.operator_range} {value} {self.operator} {self.expected_value} is False.')


class AssertHttpResponseListDict(Assertion):

    def __init__(
        self,
        json_path: str,
        key: str,
        operator_range: str,
        operator: str,
        expected_value: int,
        allow_empty: bool = True,
        show_table: bool = True,
        assert_value_hook: callable = None,
        assert_value_hook_kwargs: dict = None
    ) -> None:
        if assert_value_hook_kwargs is None:
            assert_value_hook_kwargs = {}
        self.json_path = json_path
        self.expected_value = expected_value
        assert operator_range in operator_range_map, f'Operator range {operator_range} is not supported.'
        self.operator_range = operator_range
        assert operator in operator_map, f'Operator {operator} is not supported.'
        self.operator = operator
        self.key = key
        self.show_table = show_table
        self.allow_empty = allow_empty
        self.assert_value_hook = assert_value_hook
        self.assert_value_hook_kwargs = assert_value_hook_kwargs

    def __call__(self, response: Response) -> Any:
        data = get_json_path_value(response, self.json_path)
        error_message = f'Assertion failed: {self.operator_range} `{self.key}` {self.operator} `{self.expected_value}` is False.'

        if not data:
            if self.allow_empty:
                return
            logger.error(error_message)
            logger.error(f'Response data is empty: {response.text}')
            print(response.url)
            raise AssertionError(error_message)

        value = [item.get(self.key) for item in data]

        if self.assert_value_hook:
            value = [self.assert_value_hook(item, **self.assert_value_hook_kwargs) for item in value]

        if not operator_range_map[self.operator_range](self.expected_value, self.operator, value):
            if self.show_table:
                logger.error(error_message)
                show_response_table(response, self.json_path, only_keys=[self.key])
            raise AssertionError(error_message)
