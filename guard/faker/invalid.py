import copy
import inspect
import abc
from typing import Any, Type, Dict, Optional
from collections import namedtuple
from guard.faker.enums import InvalidDataType
from guard.utils import generate_random_string


class InvalidValue(namedtuple('InvalidValue', ['value', 'type'])):
    __slots__ = ()


class InvalidDictValue(namedtuple('InvalidValue', ['value', 'type', 'sub_field'])):
    __slots__ = ()


class StrategyMeta(abc.ABCMeta):

    provider_registry: Dict[str, Type['InvalidValueProvider']] = {}

    def __new__(cls, name, bases, class_attrs, **kwargs):
        new_cls = super().__new__(cls, name, bases, class_attrs, **kwargs)
        if not inspect.isabstract(new_cls):
            cls.provider_registry[new_cls.invalid_data_type] = new_cls
        return new_cls


class InvalidValueProvider(metaclass=StrategyMeta):
    """A value provider that always returns an invalid value."""

    invalid_data_type: InvalidDataType = None
    invalid_value: str = None

    def __init__(self, field):
        self.field = field

    def provide(self):
        return InvalidValue(
            self.get_invalid_value(),
            self.invalid_data_type
        )

    def get_invalid_value(self):
        return self.invalid_value

    @classmethod
    def get_provider(cls, invalid_data_type, field):
        if invalid_data_type not in cls.provider_registry:
            raise ValueError(f'Invalid invalid_data_type: {invalid_data_type}')
        return cls.provider_registry[invalid_data_type](field)


class NullValueProvider(InvalidValueProvider):

    invalid_data_type = InvalidDataType.NULL
    invalid_value = None


class BlankValueProvider(InvalidValueProvider):

    invalid_data_type = InvalidDataType.BLANK
    invalid_value = ''


class InvalidChoiceValueProvider(InvalidValueProvider):

    invalid_data_type = InvalidDataType.INVALID_CHOICE

    def get_invalid_value(self):
        assert self.field.choices is not None, "Field must have choices"
        while True:
            random_string = generate_random_string()
            if random_string not in self.field.choices:
                return random_string


class InvalidTypeValueProvider(InvalidValueProvider):

    invalid_data_type = InvalidDataType.INVALID_TYPE

    def get_invalid_value(self):
        pass


class ExceedMaxLengthValueProvider(InvalidValueProvider):

    invalid_data_type = InvalidDataType.EXCEED_MAX_LENGTH

    def get_invalid_value(self):
        assert self.field.max_length is not None, "Field must have max_length"
        return generate_random_string(self.field.max_length + 1)


class ExceedMinLengthValueProvider(InvalidValueProvider):

    invalid_data_type = InvalidDataType.EXCEED_MIN_LENGTH

    def get_invalid_value(self):
        assert self.field.min_length is not None, "Field must have min_length"
        return generate_random_string(self.field.min_length - 1)


class ExceedMaxValueValueProvider(InvalidValueProvider):

    invalid_data_type = InvalidDataType.EXCEED_MAX_VALUE

    def get_invalid_value(self):
        assert self.field.max_value is not None, "Field must have max_value"
        return self.field.max_value + 1


class ExceedMinValueValueProvider(InvalidValueProvider):

    invalid_data_type = InvalidDataType.EXCEED_MIN_VALUE

    def get_invalid_value(self):
        assert self.field.min_value is not None, "Field must have min_value"
        return self.field.min_value - 1


class InvalidDictValueProvider(InvalidValueProvider):

    invalid_data_type = InvalidDataType.INVALID_DICT

    def provide(self):
        field = self.field
        values = []

        # for field_name, field_instance in field.fields.items():

        #     if field_instance.required:
        #         valid_value_copy = copy.deepcopy(field.generate_valid_value())
        #         del valid_value_copy[field_name]
        #         values.append(
        #             InvalidDictValue(
        #                 value=valid_value_copy,
        #                 type=InvalidDataType.MISSING_REQUIRE,
        #                 sub_field=field_name
        #             )
        #         )

        #     for invalid_value in field_instance.generate_invalid_values():
        #         valid_value_copy = copy.deepcopy(field.generate_valid_value())
        #         valid_value_copy[field_name] = invalid_value.value
        #         values.append(
        #             InvalidDictValue(
        #                 value=valid_value_copy,
        #                 type=invalid_value.type,
        #                 sub_field=field_name
        #             )
        #         )

        return values
