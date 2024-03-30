import requests

class ChatterRequestor:
    def __init__(self, key: str, baseUrl: str):
        self.key = key
        self.baseUrl = baseUrl

    def _getHeaders(self):
        return {
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
    
    def get(self, path: str, params: dict = {}):
        response = requests.get(f"{self.baseUrl}{path}", headers=self._getHeaders(), params=params)
        self._checkResponse(response)
        return response.json()['data']
    
    def post(self, path: str, data: dict = {}):
        response = requests.post(f"{self.baseUrl}{path}", headers=self._getHeaders(), json=data)
        self._checkResponse(response)
        return response.json()['data']
    
    def put(self, path: str, data: dict = {}):
        response = requests.put(f"{self.baseUrl}{path}", headers=self._getHeaders(), json=data)
        self._checkResponse(response)
        return response.json()['data']
    
    def patch(self, path: str, data: dict = {}):
        response = requests.patch(f"{self.baseUrl}{path}", headers=self._getHeaders(), json=data)
        self._checkResponse(response)
        return response.json()['data']
    
    def delete(self, path: str):
        response = requests.delete(f"{self.baseUrl}{path}", headers=self._getHeaders())
        self._checkResponse(response)
        return response.json()['data']
    
    def _checkResponse(self, response):
        if response.status_code >= 400:
            raise ValueError(f"Request failed with status code {response.status_code}: {response.text}")

