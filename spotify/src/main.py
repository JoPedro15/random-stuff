from client import SpotifyClient

client = SpotifyClient()
client.search_for_track(
    track_name="Open Car", track_album="Deadwing", track_artist="Porcupine tree"
)

client.search_for_album_by_id("0w9RrU2alZeQ1BJwpvpFtP")
