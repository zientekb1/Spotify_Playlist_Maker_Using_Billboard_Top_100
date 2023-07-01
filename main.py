import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
from bs4 import BeautifulSoup

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}")
print(response.raise_for_status())
billboard_webpage = response.text
soup = BeautifulSoup(billboard_webpage, "html.parser")
songs_web_scrape = soup.select("div ul li ul li h3")
song_names = [song.getText().strip() for song in songs_web_scrape]
print(song_names)
sp = spotipy.Spotify(
    oauth_manager=SpotifyOAuth(
        client_id='',   # spotify developer mode client id
        client_secret='',   # spotify developer mode client_secret id
        redirect_uri='https://example.com',
        scope='playlist-modify-public',
        cache_path='token.txt',
        show_dialog=True,
        username=''     # username to spotify account
    )
)
user_id = sp.current_user()["id"]

song_uris = []
for song in song_names:
    try:
        result = sp.search(q=f"track:{song}", type="track")
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except:
        pass
print(f"number of songs found: {len(song_uris)}")
playlist = sp.user_playlist_create(
    user=user_id,
    name=f'Billboard Top 100 from {date}',
    public=True,
    collaborative=False,
)
sp.playlist_add_items(
    playlist_id=playlist["id"],
    items=song_uris,
)
print("playlist has been created")
