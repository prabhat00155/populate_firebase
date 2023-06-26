import requests


def fetch(games):
  API_KEY = '8ea693465c6e400198bf22459477976d'
  game_list = []
  for game_name, locations in games.items():
    url = f"https://api.rawg.io/api/games"
    params = {
        "key": API_KEY,
        "search": game_name,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200: 
      data = response.json()
      results = data.get("results", [])
      if results:
        game = results[0] 
        current = {}
        current['name'] = game['name']
        current['platforms'] = list(map(lambda x: x['platform']['name'], game['platforms']))
        current['background_image'] = game['background_image']
        current['metacritic'] = game['metacritic']
        current['rating'] = game['rating']
        current['released'] = game['released']
        current['playtime'] = game['playtime']
        current['ratings_count'] = game['ratings_count']
        current['esrb_rating'] = game['esrb_rating']['name'] if game['esrb_rating'] else None
        current['genres'] = list(map(lambda x: x['name'], game['genres']))
        current['locations'] = locations 
        game_id = game['id']
        current['description'] = ''
        current['website'] = ''
        current['reddit_url'] = ''
        current['metacritic_url'] = ''

        url = f"https://api.rawg.io/api/games/{game_id}"
        params = { 'key': API_KEY }
        response = requests.get(url, params=params)
        if response.status_code == 200:
          data = response.json()
          if data:
            current['description'] = data['description']
            current['website'] = data['website']
            current['reddit_url'] = data['reddit_url']
            current['metacritic_url'] = data['metacritic_url']

        game_list.append(current)
  return game_list
