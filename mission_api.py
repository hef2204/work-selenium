"""
This module provides an interface to interact with the Mission API,
including domain-specific classes for Maps, Customers, and Missions.
"""

import json
import os
from typing import Optional

import requests


class MissionAPI:
    """
    Base class for interacting with the Mission API.
    Provides methods for authentication and making HTTP requests.
    """

    def __init__(self):
        self.base_url: str = os.getenv('MISSION_API_URL')
        self._token: Optional[str] = None

    def __get_token(self):
        """
        Retrieves and sets the authentication token using Firebase credentials.
        Raises a ValueError if authentication fails.
        """
        fb_token = os.getenv("FIREBASE_TOKEN")
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={fb_token}"
        headers = {"Content-Type": "application/json"}
        body = {
            "email": os.getenv("VALID_EMAIL"),
            "password": os.getenv("VALID_PASSWORD"),
            "returnSecureToken": True
        }

        response = requests.post(url, headers=headers, data=json.dumps(body), timeout=10)

        if response.status_code == 200:
            res_json = response.json()
            self._token = res_json["idToken"]
        else:
            raise ValueError(f"Error: {response.status_code}, {response.text}")

    def token(self) -> str:
        """
        Returns the authentication token. Retrieves a new token if not already set.
        """
        if self._token is None:
            self.__get_token()
        return self._token

    def _get_headers(self) -> dict:
        """
        Returns headers with the authorization token for making requests.
        """
        bearer_token = self.token()
        return {
            "Accept": "application/json",
            "Authorization": f"Bearer {bearer_token}",
        }

    def http_delete(self, path: str) -> requests.Response:
        """
        Makes an HTTP DELETE request to the specified path.
        """
        return requests.delete(f"{self.base_url}/{path}", headers=self._get_headers(), timeout=10)

    def http_get(self, path: str) -> requests.Response:
        """
        Makes an HTTP GET request to the specified path.
        """
        return requests.get(f"{self.base_url}/{path}", headers=self._get_headers(), timeout=10)


class MissionAPIDomainMap(MissionAPI):
    """
    Class for interacting with the Maps domain of the Mission API.
    """

    def __init__(self):
        super().__init__()
        self.base_url_domain = "maps"

    def delete_map(self, map_id: int) -> bool:
        """
        Deletes a map by its ID.
        """
        response = self.http_delete(f"{self.base_url_domain}/{map_id}")
        if not response.status_code == 204:
            raise ValueError(f"Error: {response.status_code}, {response.text}")
        return True

    def get_map(self, map_id: int) -> dict:
        """
        Retrieves a map by its ID.
        """
        response = self.http_get(f"{self.base_url_domain}/{map_id}")
        if not response.status_code == 200:
            raise ValueError(f"Error: {response.status_code}, {response.text}")
        return response.json()


class MissionAPIDomainCustomer(MissionAPI):
    """
    Class for interacting with the Customer domain of the Mission API.
    """

    def __init__(self):
        super().__init__()
        self.base_url_domain = "customer"

    def delete_customer(self, customer_id: str) -> bool:
        """
        Deletes a customer by their ID.
        """
        response = self.http_delete(f"{self.base_url_domain}/{customer_id}")
        if not response.status_code == 204:
            raise ValueError(f"Error: {response.status_code}, {response.text}")
        return True

    def get_customer(self, customer_id: str) -> dict:
        """
        Retrieves a customer by their ID.
        """
        response = self.http_get(f"{self.base_url_domain}/{customer_id}")
        if not response.status_code == 200:
            raise ValueError(f"Error: {response.status_code}, {response.text}")
        return response.json()


class MissionAPIDomainMission(MissionAPI):
    """
    Class for interacting with the Mission Templates domain of the Mission API.
    """

    def __init__(self):
        super().__init__()
        self.base_url_domain = "mission_templates"

    def delete_mission(self, mission_template_id: int) -> bool:
        """
        Deletes a mission template by its ID.
        """
        response = self.http_delete(f"{self.base_url_domain}/{mission_template_id}")
        if not response.status_code == 200:
            raise ValueError(f"Error: {response.status_code}, {response.text}")
        return True

    def get_mission(self, mission_template_id: int) -> dict:
        """
        Retrieves a mission template by its ID.
        """
        response = self.http_get(f"{self.base_url_domain}/{mission_template_id}")
        if not response.status_code == 200:
            raise ValueError(f"Error: {response.status_code}, {response.text}")
        return response.json()
