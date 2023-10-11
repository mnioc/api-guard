from typing import Optional, List, Dict, Any, Union, Callable
from requests.models import Request
from guard.http.client import HttpClient
from guard.usecase.bases import UseCase
from guard.http.hooks import log_response


class UnitUseCase(UseCase):
    """
    API single point testing is used to test a specific API endpoint.

    Args:
        method (str): HTTP method.
        url (str): API endpoint.
        name (str): Use case name.
        client (HttpClient): HTTP client.
        assertions (list): Assertions.
        **kwargs: Keyword arguments for requests.models.Request.

    Examples:
        >>> from guard.usecase.unit import UnitUseCase
        >>> from guard.assertion.http import AssertHttpStatusCodeEqual
        >>> use_case = UnitUseCase('GET', 'http://xxx.com', assertions=[AssertHttpStatusCodeEqual(200)])
        >>> use_case.execute()
    """

    def __init__(
        self,
        method: str,
        url: str,
        name: Optional[str] = None,
        client: Optional[HttpClient] = None,
        assertions: Optional[list] = None,
        pre_hooks: Optional[List[Dict[str, Any]]] = None,
        post_hooks: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ):
        if name is None:
            name = f'{method} {url}'
        super().__init__(name)

        self.client = client
        self.request = Request(method.upper(), url, **kwargs)
        self.assertions = assertions or []
        self.pre_hooks = pre_hooks or []
        self.post_hooks = post_hooks or []

    def set_name(self, name: str) -> None:
        """
        This method is used to set the use case name.
        """
        self.name = name

    def set_client(self, client: HttpClient) -> None:
        """
        This method is used to set the HTTP client.
        """
        self.client = client

    def add_assertion(self, assertion) -> None:
        """
        This method is used to add an assertion.
        """
        if assertion not in self.assertions:
            self.assertions.append(assertion)

    def clear_assertions(self) -> None:
        """
        This method is used to clear assertions.
        """
        self.assertions = []

    def extend_assertions(self, assertions: list) -> None:
        """
        This method is used to extend assertions.
        """
        for assertion in assertions:
            self.add_assertion(assertion)

    def set_request_method(self, method: str) -> None:
        """
        This method is used to set the HTTP method.
        """
        self.request.method = method.upper()

    def set_request_url(self, url: str) -> None:
        """
        This method is used to set the HTTP url.
        """
        self.request.url = url

    def set_request_headers(self, headers: dict) -> None:
        """
        This method is used to set the HTTP headers.
        """
        self.request.headers = headers

    def set_request_data(self, body: str) -> None:
        """
        This method is used to set the HTTP body.
        """
        self.request.data = body

    def set_request_params(self, params: dict) -> None:
        """
        This method is used to set the HTTP params.
        """
        self.request.params = params

    def set_request_cookies(self, cookies: dict) -> None:
        """
        This method is used to set the HTTP cookies.
        """
        self.request.cookies = cookies

    def set_request_auth(self, auth: tuple) -> None:
        """
        This method is used to set the HTTP auth.
        """
        self.request.auth = auth

    def set_request_files(self, files: dict) -> None:
        """
        This method is used to set the HTTP files.
        """
        self.request.files = files

    def set_request_hooks(self, hooks: dict) -> None:
        """
        This method is used to set the HTTP hooks.
        """
        self.request.hooks = hooks

    def set_request_json(self, json: dict) -> None:
        """
        This method is used to set the HTTP json.
        """
        self.request.json = json

    def execute(self, client=None) -> None:
        """
        This method is used to execute the use case.
        """
        self.execute_pre_hooks()
        self.client = client
        if self.client is None:
            self.client = HttpClient()
        response = self.client.send_request(self.request)
        try:
            for assertion in self.assertions:
                assertion(response)
        except AssertionError as e:
            self.add_failed_reason(str(e))
            self.do_fail()
        self.response = response
        self.execute_post_hooks()

    def copy(self) -> 'UnitUseCase':
        """
        This method is used to copy the use case.
        """
        return UnitUseCase(
            self.request.method,
            self.request.url,
            self.name,
            self.client,
            self.assertions,
            **{
                'headers': getattr(self.request, 'headers', None),
                'data': getattr(self.request, 'data', None),
                'params': getattr(self.request, 'params', None),
                'cookies': getattr(self.request, 'cookies', None),
                'auth': getattr(self.request, 'auth', None),
                'files': getattr(self.request, 'files', None),
                'hooks': getattr(self.request, 'hooks', None),
                'json': getattr(self.request, 'json', None)
            }
        )
