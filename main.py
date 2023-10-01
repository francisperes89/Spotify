from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth


#SCRAPING BILLBOARD 100
date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
URL = "https://www.billboard.com/charts/hot-100/"
new_URL = URL + date.strip()
response = requests.get(new_URL)
web_html = response.text
soup = BeautifulSoup(web_html, "html.parser")

tracks_title = soup.select("li ul li h3")
tracks_list = [track.getText().strip() for track in tracks_title]

artist = soup.find_all(name="span", class_="u-max-width-330")
artist_names = [name.getText().strip() for name in artist]
song_and_artist = dict(zip(tracks_list, artist_names))
print(song_and_artist)


#SPOTIFY AUTHENTICATION
OAUTH_AUTHORIZE_URL = "https://accounts.spotify.com/authorize"
OAUTH_TOKEN_URL = "https://accounts.spotify.com/api/token"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id="YOUR CLIENT ID",
        client_secret="YOUR CLIENT SECRET",
        show_dialog=True,
        cache_path="token.txt",
        username="Francis Oliveira",
    )
)
user_id = sp.current_user()["id"]

#SEARCH SPOTIFY FOR SONGS BY TITLE AND ARTIST
song_uris = []
for (song, artist) in song_and_artist.items():
    try:
        result = sp.search(q=f"track:{song} artist:{artist}", type="track")
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except:
        pass

print(f"Number of songs found: {len(song_uris)}")

#CREATING A NEW PLAYLIST ON SPOTIFY
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False,)

#ADDING SONGS FOUND INTO NEW PLAYLIST
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
print(f"New playlist '{date} Billboard 100' successfully created on Spotify!")
