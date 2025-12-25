from __future__ import annotations

from typing import Any, Dict, List


def parse_multiple_tracks(response):
    # Extract the list of tracks
    tracks = response.get("tracks", [])

    # Handle each track safely
    for i, track in enumerate(tracks, start=1):
        if track is None:
            print(f"{i}. ⚠️ Track unavailable or invalid")
            continue

        # Extract key data
        song_name = track.get("name", "Unknown")
        album_name = track.get("album", {}).get("name", "Unknown Album")
        artists = ", ".join(a["name"] for a in track.get("artists", []))

        # Print in a readable format
        print(f"{i}. 🎵 {song_name} — {artists} 💿 {album_name}")


def format_spotify_album(album_obj: Dict[str, Any]) -> str:
    """
    Accepts either:
      - a Spotify album dict (like the one you pasted), or
      - a search/browse result with {"albums": {"items": [ ... ]}}
    and returns a pretty, line-by-line string with album, artist, year, and tracks.
    """
    # If it's a search-style payload, grab the first album item
    if "albums" in album_obj and isinstance(album_obj["albums"], dict):
        items = album_obj["albums"].get("items", [])
        if not items:
            return "No albums found."
        album = items[0]
    else:
        album = album_obj

    album_name = album.get("name", "")
    release_date = album.get("release_date", "")
    year = release_date[:4] if release_date else ""
    artists = album.get("artists", [])
    artist_name = artists[0].get("name", "") if artists else ""

    # Tracks
    tracks_block = album.get("tracks", {}) or {}
    tracks_items: List[Dict[str, Any]] = tracks_block.get("items", []) or []

    # Ensure ordered by track_number if present
    tracks_items.sort(key=lambda t: t.get("track_number", 0))

    track_names = [t.get("name", "") for t in tracks_items]
    width = max(2, len(str(len(track_names))))  # zero-pad width (e.g., 01..14)

    lines = [
        f"Album : {album_name} ({year})",
        f"Artist: {artist_name}",
        "Tracks:",
    ]
    for i, name in enumerate(track_names, 1):
        lines.append(f"  {i:0{width}d}. {name}")

    return "\n".join(lines)
