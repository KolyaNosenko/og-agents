import requests
from requests import Response

from og_agents.common.http_client.http_client import HttpClient

class RequestsHttpClient(HttpClient):
    def get(self, url, params=None, **kwargs) -> Response:
        response = requests.get(url, params=params, **kwargs)
        response.raise_for_status()
        return response

    def post(self, url: str, data=None, json=None, **kwargs) -> Response:
        response = requests.post(url, data=data, json=json, **kwargs)
        response.raise_for_status()
        return response

    def put(self, url, data=None, **kwargs) -> Response:
        response = requests.put(url, data=data, **kwargs)
        response.raise_for_status()
        return response

    def patch(self, url, data=None, **kwargs) -> Response:
        response = requests.patch(url, data=data, **kwargs)
        response.raise_for_status()
        return response

    def delete(self, url, **kwargs) -> Response:
        response = requests.delete(url, **kwargs)
        response.raise_for_status()
        return response
