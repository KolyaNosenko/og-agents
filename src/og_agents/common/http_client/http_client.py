from abc import ABC, abstractmethod

class HttpClient(ABC):
    @abstractmethod
    def get(self, url: str):
        pass

    @abstractmethod
    def post(self, url: str, data=None, json=None, **kwargs):
        pass

    @abstractmethod
    def put(self, url, data=None, **kwargs):
        pass

    @abstractmethod
    def patch(self, url, data=None, **kwargs):
        pass

    @abstractmethod
    def delete(self, url, **kwargs):
        pass
