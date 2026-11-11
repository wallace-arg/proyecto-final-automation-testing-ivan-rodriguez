"""Cliente HTTP sencillo sobre requests con logging y medición de tiempo."""
import requests

from utils.logger import get_logger

log = get_logger(__name__)


class ApiClient:
    def __init__(self, base_url: str, timeout: int = 10):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json; charset=UTF-8"})

    def _request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        log.info("%s %s", method.upper(), url)
        response = self.session.request(method, url, timeout=self.timeout, **kwargs)
        log.info(
            "Respuesta: %s en %.3f s",
            response.status_code,
            response.elapsed.total_seconds(),
        )
        return response

    def get(self, endpoint: str, **kwargs) -> requests.Response:
        return self._request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, payload: dict, **kwargs) -> requests.Response:
        return self._request("POST", endpoint, json=payload, **kwargs)

    def put(self, endpoint: str, payload: dict, **kwargs) -> requests.Response:
        return self._request("PUT", endpoint, json=payload, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        return self._request("DELETE", endpoint, **kwargs)
