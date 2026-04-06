from datetime import datetime, timezone

import requests


class MovieGluError(Exception):
    pass


class MovieGluClient:
    def __init__(self, settings):
        self.settings = settings

    def _headers(self):
        return {
            "client": self.settings.movieglu_client,
            "x-api-key": self.settings.movieglu_api_key,
            "authorization": self.settings.movieglu_authorization,
            "territory": self.settings.movieglu_territory,
            "api-version": self.settings.movieglu_api_version,
            "geolocation": self.settings.movieglu_geolocation,
            "device-datetime": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3],
            "accept": "application/json",
        }

    def _request(self, path, params):
        base_url = self.settings.movieglu_api_base_url.rstrip("/")
        url = f"{base_url}/{path.lstrip('/')}"

        response = requests.get(url, params=params, headers=self._headers(), timeout=20)
        mg_message = response.headers.get("MG-message")

        if response.status_code == 204:
            detail = mg_message or "No content was returned for this request."
            raise MovieGluError(f"MovieGlu returned no content (204). {detail}")

        if not response.ok:
            raise MovieGluError(
                f"MovieGlu request failed ({response.status_code} {response.reason}). "
                f"MG-message: {mg_message or 'none'}. Body: {response.text}"
            )

        if not response.content.strip():
            detail = mg_message or "The response body was empty."
            raise MovieGluError(f"MovieGlu returned an empty response body. {detail}")

        try:
            return response.json()
        except ValueError as error:
            content_type = response.headers.get("Content-Type", "unknown")
            snippet = response.text[:300]
            raise MovieGluError(
                f"MovieGlu returned a non-JSON response. "
                f"Content-Type: {content_type}. MG-message: {mg_message or 'none'}. "
                f"Body snippet: {snippet}"
            ) from error

    def search_cinemas(self, query, limit=5):
        return self._request("cinemaLiveSearch/", {"query": query, "n": limit})

    def get_cinema_showtimes(self, cinema_id, show_date, sort="alphabetical"):
        return self._request(
            "cinemaShowTimes/",
            {"cinema_id": cinema_id, "date": show_date, "sort": sort},
        )

    def get_films_now_showing(self, limit=10):
        return self._request("filmsNowShowing/", {"n": limit})
