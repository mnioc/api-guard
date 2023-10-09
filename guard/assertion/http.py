from typing import Any
from requests.models import Response
from guard.assertion.bases import Assertion
from requests.exceptions import JSONDecodeError
from jsonpath_rw import parse
from guard.assertion.operator import operator_map


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
