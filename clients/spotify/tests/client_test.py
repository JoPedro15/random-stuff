import pytest

from clients.spotify.spotify_client.client import SpotifyClient


@pytest.mark.parametrize(
    "track, album, artist",
    [
        ("Open Car", "Deadwing", "Porcupine Tree"),
        ("Lazarus", "Deadwing", "Porcupine Tree"),
        ("Blackest Eyes", "In Absentia", "Porcupine Tree"),
        ("Arriving Somewhere but Not Here", "Deadwing", "Porcupine Tree"),
    ],
)
def test_client_search_multiple_tracks(track, album, artist):
    client = SpotifyClient()
    result = client.get_track(track_name=track, track_album=album, track_artist=artist)

    assert result is not None


def test_search_album_by_id():
    client = SpotifyClient()
    result = client.fetch_album("0w9RrU2alZeQ1BJwpvpFtP")

    assert result is not None
    assert "CLOSURE / CONTINUATION" in result["name"]
