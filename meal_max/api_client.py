import requests
import os

class CalorieNinjasAPIClient:
    def __init__(self, api_key: str):
        """
        Initializes the API client with the given API key.
        """
        self.api_url = 'https://api.calorieninjas.com/v1'
        self.headers = {'X-Api-Key': api_key}

    def get_nutrition(self, query: str):
        """
        Makes a GET request to fetch nutritional information for a given query.

        Args:
            query (str): The food or ingredient query string.

        Returns:
            dict: JSON response with nutritional data or error information.
        """
        url = f"{self.api_url}/nutrition?query={query}"
        response = requests.get(url, headers=self.headers)
        return self._handle_response(response)

    def _handle_response(self, response: requests.Response) -> dict:
        """
        Handles API responses and errors.

        Args:
            response (requests.Response): The response object from the API call.

        Returns:
            dict: The parsed JSON response or an error message.
        """
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "error": response.status_code,
                "message": response.text
            }
