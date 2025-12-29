from client import SpotifyClient

client = SpotifyClient()
client.get_track(
    track_name="Open Car", track_album="Deadwing", track_artist="Porcupine tree"
)

client.fetch_album("0w9RrU2alZeQ1BJwpvpFtP")
