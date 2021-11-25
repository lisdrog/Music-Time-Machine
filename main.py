import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup

spoty_id = SPOTY_ID
spoty_secret = SPOTY_SECRET
date = input("Введите дату в формате: ГГГ-ММ-ДД\n")

url = "https://www.billboard.com/charts/hot-100/" + date

response = requests.get(url)
website_html = response.text

soup = BeautifulSoup(website_html, "html.parser")
results_aut = soup.find_all(name="h3", id="title-of-a-story")

songs = [autor.getText() for autor in results_aut[3:33]]
titles = [song.strip(song[0:1]) for song in songs]
print(titles)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=spoty_id,
                                               client_secret=spoty_secret,
                                               redirect_uri="http://example.com",
                                               scope="playlist-modify-private",
                                               show_dialog=True,
                                               cache_path="token.txt"
                                               ))
user_id = sp.current_user()["id"]

song_uris = []
year = date.split("-")[0]

for song in songs:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} нет в Spotify. Пропустить.")

id_play = sp.user_playlist_create(user=user_id, name=date, public=False)
sp.user_playlist_add_tracks(user=user_id, playlist_id=id_play["id"], tracks=song_uris)
