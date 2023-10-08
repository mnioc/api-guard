from typing import Optional
from requests.models import Request
from guard.http.client import HttpClient
from guard.usecase.bases import UseCase


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
        **kwargs
    ):
        if name is None:
            name = f'{method} {url}'
        super().__init__(name)

        self.client = client
        self.request = Request(method.upper(), url, **kwargs)
        self.assertions = assertions or []

    def execute(self) -> None:
        """
        This method is used to execute the use case.
        """
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
