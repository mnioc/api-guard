from typing import Any, Union
from guard.assertion.bases import Assertion
from guard.assertion.operator import operator_map


class AssertDict(Assertion):
    ...


class AssertDictKeyExists(AssertDict):

    _name = 'AssertDictKeyExists'
    _error_message: str = 'Assertion failed: {key} does not exist in {data}'

    def __init__(self, key: Union[str, list, tuple]) -> None:
        self.key = key
        if isinstance(self.key, str):
            self.key = [self.key]

    @property
    def repr_key(self) -> str:
        return '.'.join(self.key)

    def __call__(self, data) -> Any:
        for key in self.key:
            if key not in data:
                raise AssertionError(self._error_message.format(key=key, data=data))
            data = data.get(key)

    def __str__(self) -> str:
        return f'`{self.repr_key}` does exist in dict'


class AssertDictKeyNotExists(AssertDict):

    _name = 'AssertDictKeyNotExists'
    _error_message: str = 'Assertion failed: {key} exists in {data}'

    def __init__(self, key: Union[str, list, tuple]) -> None:
        self.key = key
        if isinstance(self.key, str):
            self.key = [self.key]
    
    @property
    def repr_key(self) -> str:
        return '.'.join(self.key)

    def __call__(self, data) -> Any:
        for key in self.key:
            if key in data:
                raise AssertionError(self._error_message.format(key=key, data=data))
            data = data.get(key)

    def __str__(self) -> str:
        return f'`{self.repr_key}` does not exist in dict'


class AssertDictValue(AssertDict):

    def __init__(self, key: str, operator, expected_value: Any) -> None:
        self.key = key
        if isinstance(self.key, str):
            self.key = [self.key]
        self.expected_value = expected_value
        self.operator = operator

    @property
    def repr_key(self) -> str:
        return '.'.join(self.key)

    def __call__(self, data) -> Any:
        if self.operator not in operator_map:
            raise KeyError(f'Operator {self.operator} is not supported.')

        for key in self.key:
            if key not in data:
                raise AssertionError(
                    f'Assertion failed: {key} does not exist in {data}'
                )

            data = data.get(key)

            if not operator_map[self.operator](data, self.expected_value):
                raise AssertionError(
                    f'Assertion failed: {data} {self.operator} {self.expected_value} is False.'
                )

    def __str__(self) -> str:
        return f'`{self.repr_key} {self.operator} {self.expected_value}`'
