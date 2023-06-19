import requests


def fetch(songs):
  song_list = []
  url = f"https://accounts.spotify.com/api/token"
  headers = {"Content-Type": "application/x-www-form-urlencoded"}
  data = {
    "grant_type": "client_credentials",
    "client_id": "33695283c4754fd4bb090d903a8f6196",
    "client_secret": "60e7f5cd0ef842a59b1a755904c2a0ab"
  }
  res = requests.post(url, headers=headers, data=data)
  if res.status_code == 200:
    data = res.json()
    access_token = data['access_token']
    for song_name, locations in songs.items():
      url = f"https://api.spotify.com/v1/search"
      params = {
          "q": song_name,
          "type": "track",
          "limit": 1
      }
      headers = {
        "Authorization": f"Bearer {access_token}"
      }
      response = requests.get(url, headers=headers, params=params)
      if response.status_code == 200: 
        data = response.json()
        tracks = data.get('tracks')
        track = tracks.get('items') if tracks else None
        if track:
          song = track[0] 
          current = {}
          current['name'] = song['name']
          current['duration_ms'] = song['duration_ms'] 
          current['preview_url'] = song['preview_url'] 
          current['artists'] = list(map(lambda x: x.get('name'), song['artists']))
          current['album_name'] = song['album']['name']
          current['release_date'] = song['album']['release_date']
          current['image_url'] = song['album']['images'][0]['url']
          current['locations'] = locations 

          artist_id = song.get("artists")[0].get("id")
          artist_url = f"https://api.spotify.com/v1/artists/{artist_id}"
          artist_response = requests.get(artist_url, headers=headers)
          if artist_response.status_code == 200:
            artist_data = artist_response.json()
            current['genres'] = artist_data.get("genres", [])

          song_list.append(current)
    return song_list
