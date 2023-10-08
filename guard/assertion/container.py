from typing import Any, Union
from guard.assertion.bases import Assertion


class AssertDictKeyExists(Assertion):

    _name = 'AssertDictKeyExists'
    _error_message: str = 'Assertion failed: {key} does not exist in {data}'

    def __init__(self, key: Union[str, list, tuple]) -> None:
        self.key = key
        if isinstance(self.key, str):
            self.key = [self.key]

    def __call__(self, data) -> Any:
        for key in self.key:
            if key not in data:
                raise AssertionError(self._error_message.format(key=key, data=data))
            data = data.get(key)


class AssertDictKeyNotExists(Assertion):

    _name = 'AssertDictKeyNotExists'
    _error_message: str = 'Assertion failed: {key} exists in {data}'

    def __init__(self, key: Union[str, list, tuple]) -> None:
        self.key = key
        if isinstance(self.key, str):
            self.key = [self.key]

    def __call__(self, data) -> Any:
        for key in self.key:
            if key in data:
                raise AssertionError(self._error_message.format(key=key, data=data))
            data = data.get(key)


class AssertDictValue(Assertion):

    def __init__(self, key: str, expected_value: Any, assertion: Assertion) -> None:
        self.key = key
        if isinstance(self.key, str):
            self.key = [self.key]
        self.expected_value = expected_value
        self.assertion = assertion

    def __call__(self, data) -> Any:
        while True:
            try:
                key = next(self.key)
                data = data.get(key)
            except StopIteration:
                self.assertion(data, self.expected_value)
                return
