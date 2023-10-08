from typing import Any


class Assertion:

    _name = 'Assertion'
    _error_message: str = None

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        pass


class AssertEqual(Assertion):

    _name = 'AssertEqual'
    _error_message: str = 'Assertion failed: {a} != {b}'

    def __call__(self, a: Any, b) -> Any:
        if a != b:
            raise AssertionError(self._error_message.format(a=a, b=b))


class AssertNotEqual(Assertion):

    _name = 'AssertNotEqual'
    _error_message: str = 'Assertion failed: {a} == {b}'

    def __call__(self, a: Any, b) -> Any:
        if a == b:
            raise AssertionError(self._error_message.format(a=a, b=b))


class AssertTrue(Assertion):

    _name = 'AssertTrue'
    _error_message: str = 'Assertion failed: {a} is not True'

    def __call__(self, a: Any) -> Any:
        if not a:
            raise AssertionError(self._error_message.format(a=a))


class AssertFalse(Assertion):

    _name = 'AssertFalse'
    _error_message: str = 'Assertion failed: {a} is not False'

    def __call__(self, a: Any) -> Any:
        if a:
            raise AssertionError(self._error_message.format(a=a))


class AssertIs(Assertion):

    _name = 'AssertIs'
    _error_message: str = 'Assertion failed: {a} is not {b}'

    def __call__(self, a: Any, b: Any) -> Any:
        if a is not b:
            raise AssertionError(self._error_message.format(a=a, b=b))


class AssertIsNot(Assertion):

    _name = 'AssertIsNot'
    _error_message: str = 'Assertion failed: {a} is {b}'

    def __call__(self, a: Any, b: Any) -> Any:
        if a is b:
            raise AssertionError(self._error_message.format(a=a, b=b))


class AssertIsNone(Assertion):

    _name = 'AssertIsNone'
    _error_message: str = 'Assertion failed: {a} is not None'

    def __call__(self, a: Any) -> Any:
        if a is not None:
            raise AssertionError(self._error_message.format(a=a))


class AssertIsNotNone(Assertion):

    _name = 'AssertIsNotNone'
    _error_message: str = 'Assertion failed: {a} is None'

    def __call__(self, a: Any) -> Any:
        if a is None:
            raise AssertionError(self._error_message.format(a=a))


class AssertIn(Assertion):

    _name = 'AssertIn'
    _error_message: str = 'Assertion failed: {a} not in {b}'

    def __call__(self, a: Any, b: Any) -> Any:
        if a not in b:
            raise AssertionError(self._error_message.format(a=a, b=b))


class AssertNotIn(Assertion):

    _name = 'AssertNotIn'
    _error_message: str = 'Assertion failed: {a} in {b}'

    def __call__(self, a: Any, b: Any) -> Any:
        if a in b:
            raise AssertionError(self._error_message.format(a=a, b=b))


class AssertIsInstance(Assertion):

    _name = 'AssertIsInstance'
    _error_message: str = 'Assertion failed: {a} is not instance of {b}'

    def __call__(self, a: Any, b: Any) -> Any:
        if not isinstance(a, b):
            raise AssertionError(self._error_message.format(a=a, b=b))


class AssertNotIsInstance(Assertion):

    _name = 'AssertNotIsInstance'
    _error_message: str = 'Assertion failed: {a} is instance of {b}'

    def __call__(self, a: Any, b: Any) -> Any:
        if isinstance(a, b):
            raise AssertionError(self._error_message.format(a=a, b=b))


class AssertLessThan(Assertion):

    _name = 'AssertLessThan'
    _error_message: str = 'Assertion failed: {a} is not less than {b}'

    def __call__(self, a: Any, b: Any) -> Any:
        if not a < b:
            raise AssertionError(self._error_message.format(a=a, b=b))


class AssertLessEqual(Assertion):

    _name = 'AssertLessEqual'
    _error_message: str = 'Assertion failed: {a} is not less than or equal to {b}'

    def __call__(self, a: Any, b: Any) -> Any:
        if not a <= b:
            raise AssertionError(self._error_message.format(a=a, b=b))


class AssertGreaterThan(Assertion):

    _name = 'AssertGreaterThan'
    _error_message: str = 'Assertion failed: {a} is not greater than {b}'

    def __call__(self, a: Any, b: Any) -> Any:
        if not a > b:
            raise AssertionError(self._error_message.format(a=a, b=b))


class AssertGreaterEqual(Assertion):

    _name = 'AssertGreaterEqual'
    _error_message: str = 'Assertion failed: {a} is not greater than or equal to {b}'

    def __call__(self, a: Any, b: Any) -> Any:
        if not a >= b:
            raise AssertionError(self._error_message.format(a=a, b=b))
