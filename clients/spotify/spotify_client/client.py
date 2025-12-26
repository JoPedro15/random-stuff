"""
CLI for Spotify client
"""

# stdlib
import os
from typing import Any, Dict, Optional

# third-party
import requests
from dotenv import load_dotenv

# first-party
from common.python.logging_utils import setup
from .utils import format_spotify_album


class SpotifyClient:
    """
    A small wrapper around the Spotify Web API using the Client Credentials flow.

    Responsibilities:
      - Manage auth.py token (fetch + cache until expiry).
      - Provide typed, testable methods for common actions:
          * search_track(...)
          * get_track(...)
          * get_album_by_id(...)
          * get_multiple_tracks(...)

    Notes:
      - Expects the following environment variables:
          SPOTIFY_CLIENT_ID
          SPOTIFY_CLIENT_SECRET
          SPOTIFY_AUTH_URL
          SPOTIFY_ENDPOINT
      - Uses only application-level auth.py (no user scopes).
    """

    def __init__(
            self,
            client_id: Optional[str] = None,
            client_secret: Optional[str] = None,
            auth_url: Optional[str] = None,
            api_base_url: Optional[str] = None,
            logger_name: str = "spotify.client",
    ) -> None:
        """
        Initialize the Spotify client with credentials and endpoints.

        If parameters are not provided explicitly, values are read from the environment
        (via .env): SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_AUTH_URL, SPOTIFY_ENDPOINT.

        Raises:
            SystemError: If any required credential or URL is missing.
        """
        load_dotenv()

        self.client_id = client_id or os.getenv("SPOTIFY_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("SPOTIFY_CLIENT_SECRET")
        self.auth_url = auth_url or os.getenv("SPOTIFY_AUTH_URL")
        self.api_base_url = api_base_url or os.getenv("SPOTIFY_ENDPOINT")
        self.timeout: int = 10  # Seconds

        self.logger = setup(name=logger_name)

        if not self.client_id or not self.client_secret or not self.auth_url:
            raise SystemError("Missing Spotify credentials or auth.py URL in environment.")

        # Token cache
        self._access_token: Optional[str] = None
        self._token_expires_at: float = 0.0

    def get_access_token(self) -> str:
        """
        Obtain a fresh access token using the Client Credentials flow.

        Returns:
            str: A Spotify API access token.

        Raises:
            SystemExit: If the token request fails.
        """
        self.logger.info("Getting access token...")

        auth_response = requests.post(
            self.auth_url,
            data={
                "grant_type": "client_credentials",
            },
            auth=(self.client_id, self.client_secret),
            timeout=10,
        )

        if auth_response.status_code != 200:
            raise SystemExit(f"❌ Failed to get token: {auth_response.text}")

        token = auth_response.json()["access_token"]
        self.logger.info("✅ Access token received!")

        return token

    def _auth_headers(self) -> Dict[str, Any]:
        """
        Build Authorization headers for subsequent API requests.

        Notes:
            Internal helper (underscore indicates non-public API surface).
        """
        token = self.get_access_token()
        return {"Authorization": f"Bearer {token}"}

    def get_track(self, track_name: str, track_artist: str, track_album: str) -> dict:
        """
        Search for a Spotify track and retrieve detailed information.

        Args:
            track_name (str): The name of the track to search for.
            track_artist (str): The artist associated with the track.
            track_album (str): The album where the track appears.

        Returns:
            dict: Full JSON response of the matched track from the Spotify API.

        Raises:
            SystemExit: If the API call fails or no result is found.
        """
        headers = self._auth_headers()

        track_query = f"track:{track_name} artist:{track_artist} album:{track_album}"
        search_item = requests.get(
            f"{self.api_base_url}/search",
            headers=headers,
            params={
                "q": track_query,
                "type": "track",
                "limit": 1,
            },
            timeout=10,
        )

        if search_item.status_code != 200:
            raise SystemExit(f"❌ API call failed: {search_item.text}")
        result = search_item.json()["tracks"]["items"]

        if len(result) == 0:
            raise SystemExit("❌ No results found with the provided query.")

        target_track_id = result[0]["id"]

        # Get Track Info
        track_request = requests.get(
            f"{self.api_base_url}/tracks/{target_track_id}",
            headers=headers,
            timeout=self.timeout,
        )

        if track_request.status_code != 200:
            raise SystemExit(f"❌ API call failed: {track_request.text}")

        track = track_request.json()

        print(f"🎵 Track: {track['name']}")
        print(f"👤 Artist: {track['artists'][0]['name']}")
        print(f"💿 Album: {track['album']['name']}")
        print(f"📅 Release date: {track['album']['release_date']}")
        print(f"⏱️ Duration: {track['duration_ms'] / 1000:.0f}s")
        print(f"⏱️ ID: {track['id']}")
        return track

    def fetch_album(self, album_id: str) -> Dict[str, Any]:
        """
        Fetch detailed album information from Spotify by its unique ID.

        Args:
            album_id (str): The Spotify album ID.

        Returns:
            dict: Full JSON response containing album metadata and track list.

        Raises:
            SystemExit: If the API call fails.
        """
        headers = self._auth_headers()

        search_album = requests.get(
            f"{self.api_base_url}/albums/{album_id}", headers=headers, timeout=self.timeout
        )

        if search_album.status_code != 200:
            raise SystemExit(f"❌ API call failed: {search_album.text}")

        results = search_album.json()
        album_data = format_spotify_album(results)
        print(album_data)
        return results
