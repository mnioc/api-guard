import inspect
import copy
from typing import List, Dict, Union, Any
from collections import namedtuple
from guard.faker.fields import Field, DictField
from guard.faker.enums import InvalidDataType
from guard.faker.invalid import InvalidValue, InvalidDictValue
from guard.assertion.bases import Assertion
from guard.usecase.unit import UnitUseCase
from guard.usecase.suitus import UseCaseSuite
from guard.assertion.container import AssertDict
from guard.logger import logger
from guard.faker.assert_handler import handle_assertion


class InvalidData(namedtuple('InvalidData', ['data', 'field_name', 'type', 'whold_field'])):
    __slots__ = ()


class RelationConstraint:

    def __init__(self, condition: AssertDict, constraints: List[AssertDict]) -> None:
        assert isinstance(condition, AssertDict), 'condition must be an instance of AssertDict'
        self.condition = condition

        assert all(isinstance(constraint, AssertDict) for constraint in constraints), \
            'constraints must be a list of AssertDict'
        self.constraints = constraints


class RegisterFieldMetaclass(type):
    """
    This metaclass sets a dictionary named `_declared_fields` on the class.
    Any instances of `Field` included as attributes on either the class
    or on any of its superclasses will be included in the
    `_declared_fields` dictionary.
    """

    def __new__(cls, name, bases, class_attrs, **kwargs):
        new_cls = super().__new__(cls, name, bases, class_attrs, **kwargs)
        if not inspect.isabstract(new_cls):
            new_cls._declared_fields = {
                field_name: field
                for field_name, field in new_cls.__dict__.items()
                if isinstance(field, Field)
            }
        return new_cls


class Faker(metaclass=RegisterFieldMetaclass):
    """
    A generic virtual data generator class that generates valid and invalid data based on declared fields
    and handles relation constraints.
    """

    _declared_fields: Dict[str, Field] = {}

    class Meta:
        relation_constraints: List[RelationConstraint] = []

    def __init__(self, **kwargs):
        self._valid_data: Dict[str, Any] = {}
        self._invalid_data: List[InvalidData] = []
        self._relation_invalid_data: List[InvalidData] = []

    def fake_valid(self):
        """
        Generate valid data.
        """
        valid_data = {
            field_name: field.valid_value
            for field_name, field in self._declared_fields.items()
        }
        valid_data = self.check_relation_constraint(valid_data)
        self._valid_data = valid_data
        return valid_data

    def fake_invalid(self):
        """
        Generate invalid data.
        """
        for field_name, field in self._declared_fields.items():

            if field.required:
                self._fake_missing_required_data(field_name)

            invalid_values: List[Union[InvalidValue, InvalidDictValue]] = field.fake_invalid()
            for invalid_value in invalid_values:

                valid = copy.deepcopy(self._valid_data)
                valid[field_name] = invalid_value.value
                whole_field = field_name

                if isinstance(invalid_value, InvalidDictValue):
                    whole_field = f'{field_name}.{invalid_value.sub_field}'

                self.add_invalid_data(
                    InvalidData(valid, field_name, invalid_value.type, whole_field)
                )

    def add_invalid_data(self, invalid_data: InvalidData) -> None:
        self._invalid_data.append(invalid_data)

    def _fake_missing_required_data(self, field_name: str) -> InvalidData:
        missing_require_data = copy.deepcopy(self._valid_data)
        del missing_require_data[field_name]
        self.add_invalid_data(
            InvalidData(missing_require_data, field_name, InvalidDataType.MISSING_REQUIRE.value, field_name)
        )
        return missing_require_data

    def get_relation_constraints(self) -> List[RelationConstraint]:
        if not hasattr(self, 'Meta') or not getattr(self.Meta, 'relation_constraints', None):
            return []

        return self.Meta.relation_constraints

    @property
    def relation_constraints(self) -> List[RelationConstraint]:
        return self.get_relation_constraints()

    def check_relation_constraint(self, valid_data) -> Dict[str, Any]:
        for relation_constraint in self.relation_constraints:
            condition = relation_constraint.condition

            # If condition is not satisfied
            # then skip this relation constraint
            try:
                condition(valid_data)
            except AssertionError:
                continue

            logger.info(f'Condition: {condition} is `True`')

            for constraint in relation_constraint.constraints:

                # If constraint is satisfied
                # then set valid value for constraint
                try:
                    constraint(valid_data)
                except AssertionError:
                    logger.info(f'Constraint {constraint} is `False`. change valid value.')

                    if len(constraint.key) == 1:
                        default_valid_data = self._declared_fields[constraint.key[0]].valid_value
                    else:
                        field = self._declared_fields[constraint.key[0]]
                        for key in constraint.key[1:]:
                            if isinstance(field, DictField):
                                field = field.fields[key]
                        default_valid_data = field.valid_value
                    valid_data, invalid_data = handle_assertion(constraint, data=valid_data, default=default_valid_data)

                    # Generate invalid data
                    self._relation_invalid_data.append(invalid_data)
                    logger.info(f'Generate invalid data for constraint {constraint}')

        return valid_data


class UseCaseFaker(Faker):

    class Meta:
        relation_constraints: List[RelationConstraint] = []
        valid_assertions: List[Assertion] = []
        invalid_assertions: Dict[str, Dict[str, List[Assertion]]] = {}
        default_invalid_assertions: List[Assertion] = []

    def fake_use_case(self, usecase) -> str:
        usecases = self.faker_valid_use_case(usecase) + self.faker_invalid_use_case(usecase)
        return UseCaseSuite(usecases)

    def get_default_invalid_assertions(self) -> List[Assertion]:
        if not hasattr(self, 'Meta') or not getattr(self.Meta, 'default_invalid_assertions', None):
            return []
        return self.Meta.default_invalid_assertions

    def get_valid_assertions(self) -> List[Assertion]:
        if not hasattr(self, 'Meta') or not getattr(self.Meta, 'valid_assertions', None):
            return []
        return self.Meta.valid_assertions

    def get_invalid_assertions(self) -> Dict[str, Dict[str, List[Assertion]]]:
        if not hasattr(self, 'Meta') or not getattr(self.Meta, 'invalid_assertions', None):
            return {}
        return self.Meta.invalid_assertions

    def get_assertions_by_field_name(self, field_name: str, invalid_data_type: str) -> List[Assertion]:
        assertions = self.get_invalid_assertions()
        if field_name in assertions:
            assertions = assertions[field_name]

            if invalid_data_type in assertions:
                return assertions[invalid_data_type]

        return []

    def faker_valid_use_case(
        self,
        use_case: UnitUseCase
    ) -> List[UnitUseCase]:
        use_case.set_request_json(self.fake_valid())
        use_case.extend_assertions(self.get_valid_assertions())
        return [use_case]

    def faker_invalid_use_case(
        self,
        use_case: UnitUseCase
    ) -> UnitUseCase:

        usecases = []

        for field_name, field in self._declared_fields.items():

            if field.required:
                _case = use_case.copy()
                _case.clear_assertions()
                _case.set_request_json(self._fake_missing_required_data(field_name))
                _case.extend_assertions(self.get_assertions_by_field_name(field_name, InvalidDataType.MISSING_REQUIRE.value))
                _case.set_name(f'<{_case.request.method} {_case.request.url} | {field_name} | {InvalidDataType.MISSING_REQUIRE.value}>')
                usecases.append(_case)

            invalid_values: List[Union[InvalidValue, InvalidDictValue]] = field.fake_invalid()
            for invalid_value in invalid_values:

                valid = copy.deepcopy(self._valid_data)
                valid[field_name] = invalid_value.value
                whole_field = field_name

                if isinstance(invalid_value, InvalidDictValue):
                    whole_field = f'{field_name}.{invalid_value.sub_field}'

                _case = use_case.copy()
                _case.clear_assertions()
                _case.set_request_json(valid)
                if assertions := self.get_assertions_by_field_name(whole_field, invalid_value.type):
                    _case.extend_assertions(assertions)
                else:
                    _case.extend_assertions(self.get_default_invalid_assertions())
                _case.set_name(f'<{_case.request.method} {_case.request.url} | {whole_field} | {invalid_value.type}>')
                usecases.append(_case)

        for invalid_relation in self._relation_invalid_data:
            _case = use_case.copy()
            _case.set_request_json(invalid_relation.data)
            _case.clear_assertions()
            _case.set_name(f'<{_case.request.method} {_case.request.url} | {invalid_relation.type}')

            # TODO Add assertion for relation invalid data.
            _case.extend_assertions(self.get_default_invalid_assertions())
            usecases.append(_case)

        return usecases
