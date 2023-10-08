import requests
import abc
import inspect
from typing import Any, Type, Dict, Optional
from requests.models import Response, Request
from guard.http.enums import HttpAuthType
from guard.http.auth import Authentication
from guard.http.hooks import show_response_table


class StrategyMeta(abc.ABCMeta):

    auth_registry: Dict[str, Type['HttpClient']] = {}

    def __new__(cls, name, bases, class_attrs, **kwargs):
        new_cls = super().__new__(cls, name, bases, class_attrs, **kwargs)
        if not inspect.isabstract(new_cls):
            cls.auth_registry[new_cls.auth_type] = new_cls
        return new_cls


class HttpClient(requests.Session, metaclass=StrategyMeta):
    """
    This class is used to send HTTP requests.
    """
    _instance_ = {}

    auth_type: str = None

    # This method is used to implement the singleton pattern.
    # For the same `endpoint` it ensures that only one instance of the class is created.
    # The instance is stored in the class variable _instance_.
    def __new__(cls, endpoint: str = None, **kwargs: Any):
        if not endpoint:
            return super().__new__(cls)
        if endpoint not in cls._instance_:
            cls._instance_[endpoint] = super().__new__(cls)
        return cls._instance_[endpoint]

    def __init__(self, endpoint: str = None, authentication: Optional[Authentication] = None, **kwargs: Any):
        self.endpoint = endpoint
        self.authentication = authentication

    @classmethod
    def get_client(cls, auth_type: Optional[str] = None, **kwargs: Any) -> 'HttpClient':
        """
        This method is used to get the client object.
        """
        if not auth_type:
            return cls(**kwargs)
        if auth_type not in cls.auth_registry:
            raise ValueError(f'Invalid auth type: {auth_type}')
        return cls.auth_registry[auth_type](**kwargs)

    def request(
        self,
        method,
        url,
        timeout=None,
        allow_redirects=True,
        proxies=None,
        verify=None,
        cert=None,
        stream=None,
        show_table=False,
        json_path=None,
        ignore_show_keys=None,
        **kwargs,
    ):
        if self.endpoint and not url.startswith('http'):
            url = self.endpoint + url

        req = Request(method=method.upper(), url=url, **kwargs)
        if self.authentication:
            req = self.authentication.set_authentication(req)
        prep = self.prepare_request(req)

        proxies = proxies or {}
        settings = self.merge_environment_settings(
            prep.url, proxies, stream, verify, cert
        )

        # Send the request.
        send_kwargs = {
            "timeout": timeout,
            "allow_redirects": allow_redirects,
        }
        send_kwargs |= settings
        res = self.send(prep, **send_kwargs)
        if show_table:
            show_response_table(res, json_path, ignore_show_keys)
        return res

    def send_request(self, request: Request, **kwargs: Any) -> Response:
        """
        This method is used to send a request.
        """

        if self.endpoint and not request.url.startswith('http'):
            request.url = self.endpoint + request.url

        if self.authentication:
            request = self.authentication.set_authentication(request)

        prep = self.prepare_request(request)
        return self.send(prep, **kwargs)

    def get(self, url: str, **kwargs: Any) -> Response:
        """
        This method is used to send a GET request.
        """
        return self.request('GET', url, **kwargs)

    def post(self, url: str, **kwargs: Any) -> Response:
        """
        This method is used to send a POST request.
        """
        return self.request('POST', url, **kwargs)

    def delete(self, url: str, **kwargs: Any) -> Response:
        """
        This method is used to send a DELETE request.
        """
        return self.request('DELETE', url, **kwargs)

    def put(self, url: str, **kwargs: Any) -> Response:
        """
        This method is used to send a PUT request.
        """
        return self.request('PUT', url, **kwargs)

    def patch(self, url: str, **kwargs: Any) -> Response:
        """
        This method is used to send a PATCH request.
        """
        return self.request('PATCH', url, **kwargs)


class BasicAuthenticatedClient(HttpClient):
    """
    This class is used to send HTTP requests with basic authentication.
    """
    auth_type = HttpAuthType.BASIC


class BearerAuthenticatedHttpClient(HttpClient):
    """
    This class is used to send HTTP requests with bearer authentication.
    """
    auth_type = HttpAuthType.BEARER

    def __init__(self, endpoint: str = None, authentication: Authentication | None = None, **kwargs: Any):
        assert authentication, 'BearerAuthenticatedHttpClient must be initialized with an authentication object.'
        super().__init__(endpoint, authentication, **kwargs)

    def request(self, method: str, url: str, **kwargs: Any) -> Response:
        response = super().request(method, url, **kwargs)

        # If the response status code is 401, it means that the token has expired.
        # Then we need to refresh the token and retry the request.
        if response.status_code == 401:
            self.authentication.refresh_token()
            response = super().request(method, url, **kwargs)

        return response

    def send_request(self, request: Request, **kwargs: Any) -> Response:
        response = super().send_request(request, **kwargs)

        # If the response status code is 401, it means that the token has expired.
        # Then we need to refresh the token and retry the request.
        if response.status_code == 401:
            self.authentication.refresh_token()
            response = super().send_request(request, **kwargs)

        return response
