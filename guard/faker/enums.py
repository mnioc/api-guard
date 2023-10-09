from enum import Enum


class EnumWithChoices(Enum):

    @classmethod
    def choices(cls):
        return tuple((i.value, i.name) for i in cls)

    @classmethod
    def values(cls):
        return tuple(i.value for i in cls)


class FieldType(EnumWithChoices):

    BOOLEAN = 'boolean'
    INTEGER = 'integer'
    FLOAT = 'float'
    CHAR = 'char'
    TEXT = 'text'
    LIST = 'list'
    DICT = 'dict'
    CHOICES = 'choices'


class InvalidDataType(EnumWithChoices):

    MISSING_REQUIRE = 'missing_require'
    EXCEED_MAX_VALUE = 'exceed_max_value'
    EXCEED_MIN_VALUE = 'exceed_min_value'
    INVALID_CHOICE = 'invalid_choice'
    INVALID_TYPE = 'invalid_type'
    NULL = 'null'
    BLANK = 'blank'
    EXCEED_MAX_LENGTH = 'exceed_max_length'
    EXCEED_MIN_LENGTH = 'exceed_min_length'
    INVALID_DICT = 'invalid_dict'
