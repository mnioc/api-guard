import inspect
from typing import List
from guard.usecase.suitus import UseCaseSuite
from guard.usecase.unit import UnitUseCase
from guard.assertion.http import AssertHttpStatusCodeEqual, AssertHttpResponseListDict
from guard.faker.bases import UseCaseFaker


class CreateUseCaseMixin:

    create_method = 'POST'
    create_url = None
    create_headers = {'Content-Type': 'application/json'}
    create_body = {}
    create_assertions = [AssertHttpStatusCodeEqual(201)]
    create_post_hooks = []
    create_pre_hooks = []

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
            usecase = self.get_faker().fake_use_case(usecase)

        if self.create_post_hooks:
            usecase.extend_post_hooks(self.create_post_hooks)
        
        if self.create_pre_hooks:
            usecase.extend_pre_hooks(self.create_pre_hooks)

        return usecase


class UpdateUseCaseMixin:

    update_method = 'PUT'
    update_url = None
    update_headers = {'Content-Type': 'application/json'}
    update_body = {}
    update_assertions = [AssertHttpStatusCodeEqual(200)]
    update_post_hooks = []
    update_pre_hooks = []

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
            usecase = self.get_faker().fake_use_case(usecase)

        if self.update_post_hooks:
            usecase.extend_post_hooks(self.update_post_hooks)
        
        if self.update_pre_hooks:
            usecase.extend_pre_hooks(self.update_pre_hooks)

        return usecase


class PartialUpdateUseCaseMixin:

    partial_update_method = 'PATCH'
    partial_update_url = None
    partial_update_headers = {'Content-Type': 'application/json'}
    partial_update_body = {}
    partial_update_assertions = [AssertHttpStatusCodeEqual(200)]
    partial_update_post_hooks = []
    partial_update_pre_hooks = []

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

        if self.partial_update_post_hooks:
            usecase.extend_post_hooks(self.partial_update_post_hooks)

        if self.partial_update_pre_hooks:
            usecase.extend_pre_hooks(self.partial_update_pre_hooks)

        return usecase


class DeleteUseCaseMixin:

    delete_method = 'DELETE'
    delete_url = None
    delete_assertions = [AssertHttpStatusCodeEqual(204)]
    delete_post_hooks = []
    delete_pre_hooks = []

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
        case = UnitUseCase(
            name=f'{method} {url}',
            method=method,
            url=url,
            assertions=self.get_delete_assertions()
        )
        if self.delete_post_hooks:
            case.extend_post_hooks(self.delete_post_hooks)
        
        if self.delete_pre_hooks:
            case.extend_pre_hooks(self.delete_pre_hooks)


class RetrieveUseCaseMixin:

    retrieve_method = 'GET'
    retrieve_url = None
    retrieve_assertions = [AssertHttpStatusCodeEqual(200)]
    retrieve_post_hooks = []
    retrieve_pre_hooks = []

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
        case = UnitUseCase(
            name=f'{method} {url}',
            method=method,
            url=url,
            assertions=self.get_retrieve_assertions()
        )
        if self.retrieve_post_hooks:
            case.extend_post_hooks(self.retrieve_post_hooks)

        if self.retrieve_pre_hooks:
            case.extend_pre_hooks(self.retrieve_pre_hooks)

        return case


class ListUseCaseMixin:

    list_method = 'GET'
    list_url = None
    list_assertions = [
        AssertHttpStatusCodeEqual(200)
    ]
    list_post_hooks = []
    list_pre_hooks = []
    list_root_json_path = None

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
        case = UnitUseCase(
            name=f'{method} {url}',
            method=method,
            url=url,
            assertions=self.get_list_assertions()
        )
        if self.list_post_hooks:
            case.extend_post_hooks(self.list_post_hooks)

        if self.list_pre_hooks:
            case.extend_pre_hooks(self.list_pre_hooks)

        return case


class ListParamSearchUseCaseMixin:

    search_method = 'GET'
    search_url = None
    search_param_key = 'search'
    search_json_path = None
    search_param = {}

    def get_search_url(self):
        if self.search_url is None and self.url is None:
            raise AttributeError('`search_url` or `url` is not defined.')
        return self.search_url or self.url

    def get_search_method(self):
        return self.search_method

    def get_search_param_key(self):
        return self.search_param_key

    def get_search_json_path(self):
        if self.search_json_path is None and self.list_root_json_path is None:
            raise AttributeError('`search_json_path` or `list_root_json_path` is not defined.')
        return self.search_json_path or self.list_root_json_path

    def get_search_param(self):
        return self.search_param

    def add_search_use_cases(self):
        url = self.get_search_url()
        method = self.get_search_method()
        param_key = self.get_search_param_key()
        param = self.get_search_param()
        cases = []
        for key, search_options in param.items():
            values = search_options.get('values')
            assert isinstance(values, list), '`search_param` value must be a list.'
            for value in values:
                param = {param_key: value}
                asserttions = [
                    AssertHttpStatusCodeEqual(200),
                    AssertHttpResponseListDict(
                        json_path=self.get_search_json_path(),
                        key=key,
                        operator_range='all',
                        operator='contains',
                        expected_value=value,
                        allow_empty=search_options.get('allow_empty', True)
                    )
                ]
                case = UnitUseCase(
                    name=f'{method} {url}',
                    method=method,
                    url=url,
                    params=param,
                    assertions=asserttions
                )
                if getattr(self, 'search_post_hooks', None):
                    case.extend_post_hooks(self.search_post_hooks)

                if getattr(self, 'search_pre_hooks', None):
                    case.extend_pre_hooks(self.search_pre_hooks)

                cases.append(case)

        return UseCaseSuite(cases)


class ListParamFilterUseCaseMixin:

    filter_method = 'GET'
    filter_url = None
    filter_param = {}
    """
    e.g.
        filter_param = {
            'name': {
                'operator': '==',
                'values': ['test'],
                'result_key': 'name
            },
        }
    """
    filter_json_path = None

    def get_filter_url(self):
        if self.filter_url is None and self.url is None:
            raise AttributeError('`filter_url` or `url` is not defined.')
        return self.filter_url or self.url

    def get_filter_method(self):
        return self.filter_method

    def get_filter_param(self):
        return self.filter_param

    def get_filter_json_path(self):
        if self.filter_json_path is None and self.list_root_json_path is None:
            raise AttributeError('`filter_json_path` or `list_root_json_path` is not defined.')
        return self.filter_json_path or self.list_root_json_path

    def add_filter_use_cases(self):
        param = self.get_filter_param()
        if not param:
            return
        url = self.get_filter_url()
        method = self.get_filter_method()
        cases = []
        for filter_key, filter_options in param.items():
            filter_values = filter_options.get('values')
            assert isinstance(filter_values, list), '`filter_param` value must be a list.'
            for filter_value in filter_values:
                assertions = [
                    AssertHttpStatusCodeEqual(200),
                    AssertHttpResponseListDict(
                        json_path=self.get_filter_json_path(),
                        key=filter_options.get('result_key', filter_key),
                        operator_range='all',
                        operator=filter_options.get('operator', '=='),
                        expected_value=filter_value,
                        allow_empty=filter_options.get('allow_empty', True),
                        assert_value_hook=filter_options.get('assert_value_hook', {}).get('func'),
                        assert_value_hook_kwargs=filter_options.get('assert_value_hook', {}).get('kwargs', {})
                    )
                ]
                case = UnitUseCase(
                    name=f'{method} {url}',
                    method=method,
                    url=url,
                    params={filter_key: filter_value},
                    assertions=assertions
                )

                if getattr(self, 'filter_post_hooks', None):
                    case.extend_post_hooks(self.filter_post_hooks)

                if getattr(self, 'filter_pre_hooks', None):
                    case.extend_pre_hooks(self.list_pre_hooks)

                cases.append(case)

        return UseCaseSuite(cases)


class ListParamFilterAndSearchUseCaseMixin:

    def add_filter_and_search_use_cases(self):
        method = self.get_filter_method()
        url = self.get_filter_url()
        filter_param = self.get_filter_param()
        search_param = self.get_search_param()
        search_param_key = self.get_search_param_key()
        filter_json_path = self.get_filter_json_path()
        search_json_path = self.get_search_json_path()

        if (
            not filter_param
            or not search_param
            or not search_param_key
            or not filter_json_path
            or not search_json_path
        ):
            return

        cases = []
        for filter_key, filter_options in filter_param.items():
            filter_values = filter_options.get('values')
            assert isinstance(filter_values, list), '`filter_param` value must be a list.'
            for filter_value in filter_values:
                for search_key, search_values in search_param.items():
                    search_values = search_values.get('values')
                    assert isinstance(search_values, list), '`search_values` value must be a list.'
                    for search_value in search_values:
                        param = {
                            search_param_key: search_value,
                            filter_key: filter_value
                        }
                        assertions = [
                            AssertHttpStatusCodeEqual(200),
                            AssertHttpResponseListDict(
                                json_path=self.get_filter_json_path(),
                                key=filter_options.get('result_key', filter_key),
                                operator_range='all',
                                operator=filter_options.get('operator', '=='),
                                expected_value=filter_value,
                                allow_empty=filter_options.get('allow_empty', True),
                                assert_value_hook=filter_options.get('assert_value_hook', {}).get('func'),
                                assert_value_hook_kwargs=filter_options.get('assert_value_hook', {}).get('kwargs', {})
                            ),
                            AssertHttpResponseListDict(
                                json_path=self.get_search_json_path(),
                                key=search_key,
                                operator_range='all',
                                operator='contains',
                                expected_value=search_value
                            )
                        ]
                        case = UnitUseCase(
                            name=f'{method} {url}',
                            method=method,
                            url=url,
                            params=param,
                            assertions=assertions
                        )

                        if getattr(self, 'filter_and_search_post_hooks', None):
                            case.extend_post_hooks(self.filter_and_search_post_hooks)

                        if getattr(self, 'filter_and_search_pre_hooks', None):
                            case.extend_pre_hooks(self.filter_and_search_pre_hooks)

                        cases.append(case)

        return UseCaseSuite(cases)


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
