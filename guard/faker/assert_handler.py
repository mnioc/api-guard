import copy
from typing import Any, Dict, Tuple
from functools import singledispatch
from guard.assertion.bases import Assertion
from guard.assertion.container import AssertDictKeyExists, AssertDictKeyNotExists, AssertDictValue
from guard.faker.invalid import InvalidValue, InvalidDictValue
from guard.faker.enums import InvalidDataType


@singledispatch
def handle_assertion(assertion: Assertion, **kwargs) -> Dict[str, Any]:
    """
    Construct valid and invalid data according to assert
    """
    ...


@handle_assertion.register(AssertDictKeyExists)
def handle_assert_dict_key_exists(assertion: AssertDictKeyExists, **kwargs) -> Tuple[Dict, Any]:
    """
    When `AssertDictKeyExists` has been raised, construct valid and invalid data
    """
    data = kwargs.get('data')
    default = kwargs.get('default')

    valid_data = copy.deepcopy(data)
    invalid_data = copy.deepcopy(data)

    keys = assertion.key

    for k in keys[:-1]:
        valid_data = valid_data.setdefault(k, {})
    valid_data[keys[-1]] = default

    to_delete_key = keys[-1]
    for key in keys:
        if key == to_delete_key:
            break
        invalid_data = invalid_data.get(key)
    del invalid_data[to_delete_key]

    from guard.faker.bases import InvalidData

    return valid_data, InvalidData(invalid_data, keys[-1], f'( missing_require  | where {assertion})', '.'.join(keys))


@handle_assertion.register(AssertDictValue)
def handle_assert_dict_value(assertion: AssertDictValue, **kwargs) -> tuple:
    data = kwargs.get('data')
    default = kwargs.get('default')
    valid_data = copy.deepcopy(data)
    invalid_data = copy.deepcopy(data)

    keys = assertion.key
    for k in keys[:-1]:
        valid_data = valid_data.setdefault(k, {})
    valid_data[keys[-1]] = default

    from guard.faker.bases import InvalidData
    return valid_data, InvalidData(invalid_data, keys[-1], f'( {assertion} )', '.'.join(keys))


@handle_assertion.register(AssertDictKeyNotExists)
def handle_assert_dict_key_not_exists(assertion: AssertDictKeyNotExists, **kwargs) -> tuple:
    data = kwargs.get('data')
    valid_data = copy.deepcopy(data)
    invalid_data = copy.deepcopy(data)
    keys = assertion.key
    to_delete_key = keys[-1]
    for key in keys:
        if key == to_delete_key:
            break
        to_delete_data = valid_data.get(key)
    del to_delete_data[to_delete_key]

    from guard.faker.bases import InvalidData
    return valid_data, InvalidData(invalid_data, keys[-1], f'( {assertion} )', '.'.join(keys))
