import inspect
from typing import List
from guard.usecase.suitus import UseCaseSuite
from guard.usecase.unit import UnitUseCase
from guard.assertion.http import AssertHttpStatusCodeEqual
from guard.faker.bases import UseCaseFaker


class CreateUseCaseMixin:

    create_method = 'POST'
    create_url = None
    create_headers = {'Content-Type': 'application/json'}
    create_body = {}
    create_assertions = [AssertHttpStatusCodeEqual(201)]

    def get_create_url(self):
        if self.create_url is None and self.url is None:
            raise AttributeError('`create_url` or `url` is not defined.')
        return self.create_url or self.url

    def get_create_method(self):
        return self.create_method

    def get_create_headers(self):
        return self.create_headers

    def get_create_body(self):
        return self.create_body

    def get_create_assertions(self):
        return self.create_assertions

    def add_create_use_cases(self):
        url = self.get_create_url()
        method = self.get_create_method()
        json = self.get_create_body()
        usecase = UnitUseCase(
            name=f'{method} {url}',
            method=method,
            url=url,
            headers=self.get_create_headers(),
            json=self.get_create_body(),
            assertions=self.get_create_assertions()
        )

        # TODO refactor !!
        if isinstance(self, FakerAutoRESTUseCaseSet) and not json:
            return self.get_faker().fake_use_case(usecase)
        return usecase


class UpdateUseCaseMixin:

    update_method = 'PUT'
    update_url = None
    update_headers = {'Content-Type': 'application/json'}
    update_body = {}
    update_assertions = [AssertHttpStatusCodeEqual(200)]

    def get_update_url(self):
        if self.update_url is None and self.retrieve_url is None:
            raise AttributeError('`update_url` or `retrieve_url` is not defined.')
        return self.update_url or self.retrieve_url

    def get_update_method(self):
        return self.update_method

    def get_update_headers(self):
        return self.update_headers

    def get_update_body(self):
        return self.update_body

    def get_update_assertions(self):
        return self.update_assertions

    def add_update_use_cases(self):
        url = self.get_update_url()
        method = self.get_update_method()
        json = self.get_create_body()
        usecase = UnitUseCase(
            name=f'{method} {url}',
            method=method,
            url=url,
            headers=self.get_update_headers(),
            json=json,
            assertions=self.get_update_assertions()
        )

        # TODO refactor !!
        if isinstance(self, FakerAutoRESTUseCaseSet) and not json:
            return self.get_faker().fake_use_case(usecase)
        return usecase


class PartialUpdateUseCaseMixin:

    partial_update_method = 'PATCH'
    partial_update_url = None
    partial_update_headers = {'Content-Type': 'application/json'}
    partial_update_body = {}
    partial_update_assertions = [AssertHttpStatusCodeEqual(200)]

    def get_partial_update_url(self):
        if self.partial_update_url is None and self.retrieve_url is None:
            raise AttributeError('`partial_update_url` or `retrieve_url` is not defined.')
        return self.partial_update_url or self.retrieve_url

    def get_partial_update_method(self):
        return self.partial_update_method

    def get_partial_update_headers(self):
        return self.partial_update_headers

    def get_partial_update_body(self):
        return self.partial_update_body

    def get_partial_update_assertions(self):
        return self.partial_update_assertions

    def add_partial_update_use_cases(self):
        url = self.get_partial_update_url()
        method = self.get_partial_update_method()
        json = self.get_partial_update_body()
        usecase = UnitUseCase(
            name=f'{method} {url}',
            method=method,
            url=url,
            headers=self.get_partial_update_headers(),
            json=json,
            assertions=self.get_partial_update_assertions()
        )

        # TODO refactor !!
        if isinstance(self, FakerAutoRESTUseCaseSet) and not json:
            return self.get_faker().fake_use_case(usecase)
        return usecase


class DeleteUseCaseMixin:

    delete_method = 'DELETE'
    delete_url = None
    delete_assertions = [AssertHttpStatusCodeEqual(204)]

    def get_delete_url(self):
        if self.delete_url is None and self.retrieve_url is None:
            raise AttributeError('`delete_url` or `retrieve_url` is not defined.')
        return self.delete_url or self.retrieve_url

    def get_delete_method(self):
        return self.delete_method

    def get_delete_assertions(self):
        return self.delete_assertions

    def add_delete_use_cases(self):
        url = self.get_delete_url()
        method = self.get_delete_method()
        return UnitUseCase(
            name=f'{method} {url}',
            method=method,
            url=url,
            assertions=self.get_delete_assertions()
        )


class RetrieveUseCaseMixin:

    retrieve_method = 'GET'
    retrieve_url = None
    retrieve_assertions = [AssertHttpStatusCodeEqual(200)]

    def get_retrieve_url(self):
        if self.retrieve_url is None and self.url is None:
            raise AttributeError('`retrieve_url` or `url` is not defined.')
        return self.retrieve_url or self.url

    def get_retrieve_method(self):
        return self.retrieve_method

    def get_retrieve_assertions(self):
        return self.retrieve_assertions

    def add_retrieve_use_cases(self):
        url = self.get_retrieve_url()
        method = self.get_retrieve_method()
        return UnitUseCase(
            name=f'{method} {url}',
            method=method,
            url=url,
            assertions=self.get_retrieve_assertions()
        )


class ListUseCaseMixin:

    list_method = 'GET'
    list_url = None
    list_assertions = [AssertHttpStatusCodeEqual(200)]

    def get_list_url(self):
        if self.list_url is None and self.url is None:
            raise AttributeError('`list_url` or `url` is not defined.')
        return self.list_url or self.url

    def get_list_method(self):
        return self.list_method

    def get_list_assertions(self):
        return self.list_assertions

    def add_list_use_cases(self):
        url = self.get_list_url()
        method = self.get_list_method()
        return UnitUseCase(
            name=f'{method} {url}',
            method=method,
            url=url,
            assertions=self.get_list_assertions()
        )


class ListParamSearchUseCaseMixin:

    list_method = 'GET'
    list_url = None


class ListParamFilterUseCaseMixin:

    list_method = 'GET'
    list_url = None


class ListParamFilterAndSearchUseCaseMixin:

    list_method = 'GET'
    list_url = None


class RESTUseCaseSet(
    UseCaseSuite,
    CreateUseCaseMixin,
    UpdateUseCaseMixin,
    PartialUpdateUseCaseMixin,
    DeleteUseCaseMixin,
    RetrieveUseCaseMixin,
    ListUseCaseMixin,
    ListParamSearchUseCaseMixin,
    ListParamFilterUseCaseMixin,
    ListParamFilterAndSearchUseCaseMixin
):
    """
    This class is used to define a RESTful use case set.
    """

    url = None
    enable = []
    disable = []

    def __init__(self, cases: List[UnitUseCase] | None = None):
        super().__init__(cases)
        self.discover_cases()

    def discover_cases(self):
        """
        This method is used to discover use cases from class methods.
        so, if you want to add use cases, you can define a method like this:

        >>> def add_create_use_cases(self) -> List[UnitUseCase]:
        >>>     ...
        """

        for member_name, member in inspect.getmembers(self):
            if (
                inspect.ismethod(member)
                and member_name.startswith('add_')
                and member_name.endswith('_use_cases')
                and all(disable not in member_name for disable in self.disable)
            ):
                if _cases := member():
                    if isinstance(_cases, (list, tuple)):
                        self.add_cases(_cases)
                    else:
                        self.add_case(_cases)


class FakerAutoRESTUseCaseSet(RESTUseCaseSet):

    def get_faker(self):
        assert hasattr(self, 'faker_class'), 'You must define `faker_class` attribute in your class.'
        faker_class = self.faker_class
        assert isinstance(faker_class, type), '`faker_class` must be a class.'
        assert issubclass(faker_class, UseCaseFaker), '`faker_class` must be a subclass of `UseCaseFaker`.'
        return faker_class()
