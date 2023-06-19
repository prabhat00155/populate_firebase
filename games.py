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
        current['ratings_count'] = game['ratings_count']
        current['esrb_rating'] = game['esrb_rating']['name'] if game['esrb_rating'] else None
        current['genres'] = list(map(lambda x: x['name'], game['genres']))
        current['locations'] = locations 
        game_list.append(current)
  return game_list
