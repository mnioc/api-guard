import inspect
from typing import Any, List, Optional, Tuple, Union
import random
import string
from guard.faker.enums import FieldType, InvalidDataType
from guard.faker.invalid import InvalidValueProvider, InvalidValue, InvalidDictValue


class Field:
    """
    Base class for all fields.
    Fake data will be provided for test cases,
    where fake data includes valid data and invalid data.
    The generation of invalid data depends on the constraints defined by the fields.

    Args:
        [1] required (bool): Whether the field is required.
            If required is True:
                - valid_value: must be provided.
                - invalid_value: missing

        [2] allow_null (bool): Whether the field can be null.
            If allow_null is False:
                - valid_value: not None.
                - invalid_value: None
    """

    field_type: Union[None, FieldType] = None

    def __init__(
        self,
        required=False,
        allow_null=True,
    ):
        self.required = required
        self.allow_null = allow_null

        self._invalid_provider: List[InvalidValueProvider] = []

        self._valid: Any = ...
        self._invalid: List[InvalidValue | InvalidDictValue] = []

        if not self.allow_null:
            self.register_invalid_provider(
                InvalidValueProvider.get_provider(InvalidDataType.NULL.value, self)
            )

        self._already_valid = False

    @property
    def valid_value(self):
        if self._valid is Ellipsis:
            self._valid = self.fake_valid()
        return self._valid

    @property
    def invalid_value(self):
        if self._invalid is None:
            self._invalid = []
            self.fake_invalid()
        return self._invalid

    def register_invalid_provider(self, provider):
        """
        Register a custom invalid value provider.
        """
        assert isinstance(provider, InvalidValueProvider), (
            'provider must be an instance of InvalidValueProvider.'
        )
        self._invalid_provider.append(provider)

    def fake_valid(self):
        """
        Generate valid data.
        """
        raise NotImplementedError(
            'You must implement the generate_valid_value() method.'
        )

    def fake_invalid(self):
        """
        Generate invalid data.
        """
        for provider in self._invalid_provider:
            # breakpoint()
            self._invalid.extend(
                provider.provide()
            )
        return self._invalid


class BooleanField(Field):

    field_type = FieldType.BOOLEAN.value

    def fake_valid(self):
        return random.choice([True, False])


class CharField(Field):

    field_type = FieldType.CHAR.value

    def __init__(
        self,
        max_length: Optional[int] = 20,
        min_length: Optional[int] = 1,
        allow_blank: bool = True,
        allow_strings: Optional[Union[List[str], str]] = None,
        prefix: str = '',
        suffix: str = '',
        *args,
        **kwargs
    ):
        """
        Generates a random string of upper and lowercase letters.
        Args:
            max_length (int): Maximum length of the string.
            min_length (int): Minimum length of the string.
            allow_blank (bool): Whether the string can be blank.
            allow_strings (list): List of strings to allow.
                options:
                    - '*': Allow any char.
                    - 'whitespace': Allow '\t\n\r\v\f'.
                    - 'ascii_lowercase': Allow 'abcdefghijklmnopqrstuvwxyz'.
                    - 'ascii_uppercase': Allow 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.
                    - 'ascii_letters': Allow 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'.
                    - 'digits': Allow '0123456789'.
                    - 'hexdigits': Allow '0123456789abcdefABCDEF'.
                    - 'octdigits': Allow '01234567'.
                    - 'punctuation': Allow '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'.
                if allow_strings is None, allow_strings will be set to ['*'].
            prefix (str): Prefix to add to the string.
            suffix (str): Suffix to add to the string.
        """
        super().__init__(*args, **kwargs)
        self.max_length = max_length
        self.min_length = min_length
        self.allow_blank = allow_blank

        assert self.max_length >= self.min_length, "Maximum length must be greater than or equal to minimum length"

        self.prefix = prefix
        self.suffix = suffix

        self.allow_strings = allow_strings
        if (
            self.allow_strings is None
            or self.allow_strings == '*'
            or self.allow_strings == ['*']
        ):
            self.allow_strings = [
                'ascii_letters', 'digits',
            ]

        if not self.allow_blank:
            self.register_invalid_provider(InvalidValueProvider.get_provider(InvalidDataType.BLANK.value, self))

    def fake_valid(self):
        allow_strings = ''.join(
            getattr(string, allow_string) for allow_string in self.allow_strings
        )
        random_length = random.randint(1, 20)
        random_string = ''.join(random.choice(allow_strings) for _ in range(random_length))
        random_string = self.prefix + random_string + self.suffix
        if self.allow_blank:
            random_string = random.choice([random_string, ''])
        return random_string


class IntegerField(Field):

    field_type = FieldType.INTEGER.value

    def __init__(
        self,
        max_value: Optional[int] = None,
        min_value: Optional[int] = None,
        *args,
        **kwargs
    ):
        """
        Generates a random integer.
        Args:
            max_value (int): Maximum value of the integer.
            min_value (int): Minimum value of the integer.
        """
        super().__init__(*args, **kwargs)
        self.max_value = max_value
        self.min_value = min_value

        if self.max_value:
            self.register_invalid_provider(InvalidValueProvider.get_provider(InvalidDataType.EXCEED_MAX_VALUE.value, self))

        if self.min_value:
            self.register_invalid_provider(InvalidValueProvider.get_provider(InvalidDataType.EXCEED_MIN_VALUE.value, self))

    def fake_valid(self):

        min_value = self.min_value
        if self.min_value is None:
            min_value = -1000
        max_value = self.max_value
        if self.max_value is None:
            max_value = 1000

        assert max_value >= min_value, "Maximum value must be greater than or equal to minimum value"
        return random.randint(min_value, max_value)


class ChoiceField(Field):

    field_type = FieldType.CHOICES.value

    def __init__(
        self,
        choices: Optional[Union[List[Any], Tuple[Any, ...]]] = None,
        allow_blank: bool = True,
        *args,
        **kwargs
    ):
        """
        Generates a random choice.
        Args:
            choices (list): List of choices.
        """
        super().__init__(*args, **kwargs)
        self.choices = choices or []
        self.allow_blank = allow_blank

        if self.choices:
            self.register_invalid_provider(
                InvalidValueProvider.get_provider(
                    InvalidDataType.INVALID_CHOICE.value,
                    self
                )
            )

        if not self.allow_blank:
            self.register_invalid_provider(
                InvalidValueProvider.get_provider(
                    InvalidDataType.BLANK.value,
                    self
                )
            )

    def fake_valid(self):
        return random.choice(self.choices)


class FloatField(IntegerField):

    field_type = FieldType.FLOAT.value

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def fake_valid(self):

        min_value = self.min_value
        if self.min_value is None:
            min_value = -1000
        max_value = self.max_value
        if self.max_value is None:
            max_value = 1000

        assert max_value >= min_value, "Maximum value must be greater than or equal to minimum value"
        return round(random.uniform(min_value, max_value), 2)


class DictField(Field):

    field_type = FieldType.DICT.value

    def __init__(self, *args, **kwargs):
        """
        Args:
            fields (dict): Dictionary of fields.
        """

        # Collect sub fields from kwargs.
        super_signature = inspect.signature(super().__init__)
        super_params = super_signature.parameters.keys()
        kwargs_keys = list(kwargs.keys())
        fields = {
            key: kwargs.pop(key)
            for key in kwargs_keys
            if key not in super_params and isinstance(kwargs[key], Field)
        }
        super().__init__(*args, **kwargs)

        self.fields = fields
        self.register_invalid_provider(
            InvalidValueProvider.get_provider(
                InvalidDataType.INVALID_DICT.value,
                self
            )
        )

    def fake_valid(self):
        return {
            field_name: field_instance.valid_value
            for field_name, field_instance in self.fields.items()
        }


class ListField(Field):

    field_type = FieldType.LIST.value

    def __init__(
        self,
        fields: Optional[List[Field]] = None,
        length: Optional[int] = None,
        min_length: Optional[int] = 1,
        max_length: Optional[int] = 10,
        *args,
        **kwargs
    ):
        """
        Generates a random list.
        Args:
            fields (list): List of fields.
            length (int): Length of the list.
            min_length (int): Minimum length of the list.
            max_length (int): Maximum length of the list.
        """
        super().__init__(*args, **kwargs)
        self.fields = fields or []
        self.length = length
        self.min_length = min_length
        self.max_length = max_length

        assert self.max_length >= self.min_length, "Maximum length must be greater than or equal to minimum length"

    def fake_valid(self):
        random_length = self.length or random.randint(self.min_length, self.max_length)
        return [
            field.valid_value
            for field in self.fields
        ][:random_length]
