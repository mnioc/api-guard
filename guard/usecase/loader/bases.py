import abc
import inspect
from typing import Any, Type, Dict, Optional, Union
from guard.assertion.http import AssertHttpStatusCodeEqual, AssertHttpResponseValue
from guard.assertion.operator import operator_map


class StrategyMeta(abc.ABCMeta):

    ext_registry: Dict[str, Type['UseCaseLoader']] = {}

    def __new__(cls, name, bases, class_attrs, **kwargs):
        new_cls = super().__new__(cls, name, bases, class_attrs, **kwargs)
        if not inspect.isabstract(new_cls):
            if exts := getattr(new_cls, 'exts', None):
                for ext in exts:
                    cls.ext_registry[ext] = new_cls
        return new_cls


class UseCaseLoader(metaclass=StrategyMeta):

    exts: Union[list, tuple, None] = None

    def __init__(self):
        self.usecases = []

    def add_usecase(self, usecase):
        self.usecases.append(usecase)

    def load(self, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    def get_loader(cls, full_file_path: Optional[str] = None, **kwargs: Any) -> 'UseCaseLoader':
        """
        This method is used to get the `use_case_loader` object.
        """
        if not full_file_path:
            return None

        ext = full_file_path.split('.')[-1]
        kwargs['file_path'] = full_file_path

        return None if ext not in cls.ext_registry else cls.ext_registry[ext](**kwargs)

    def _get_assertions(self, expect_status_code, expect_value):
        assertions = []
        if expect_status_code:
            assertions.append(AssertHttpStatusCodeEqual(expect_status_code))
        if expect_value:
            for operator in operator_map:
                if operator in expect_value:
                    json_path, expect_value = expect_value.split(operator)
            assertions.append(AssertHttpResponseValue(json_path.strip(), expect_value.strip()))
        return assertions
