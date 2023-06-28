import requests

from tmdbv3api import TMDb
from tmdbv3api import Movie


country_code = {
  'US': 'US',
  'UK': 'GB',
  'India': 'IN',
}


def fetch(movies):
  tmdb = TMDb()
  tmdb.api_key = '4a19dfe65c6b0684fcc5937ee00fd6d9'
  tmdb.language = 'en'
  #for debugging we have set it true 
  tmdb.debug = True
  movie = Movie()
  WIDTH = 200
  URL_BASE = 'http://image.tmdb.org/t/p/w'
  PROVIDER_BASE = 'https://image.tmdb.org/t/p/original'
  movie_list = [] 
  for movie_name, locations in movies.items():
    current = {}
    details = movie.search(movie_name)
    if details:
      details = details[0]
    else:
      print(f'{movie_name} not found')
      continue
    current['name'] = details.title
    current['url'] = f'{URL_BASE}{WIDTH}/{details.poster_path}'
    current['overview'] = details.overview
    current['release_date'] = details.release_date
    current['vote_average'] = details.vote_average
    current['vote_count'] = details.vote_count
    current['locations'] = locations
    current['language'] = details.original_language

    current['buy'] = {} 
    current['rent'] = {} 
    current['providers'] = {}
    for location in locations:
      code = country_code.get(location)
      if code:
        providers = movie.watch_providers(details['id'])['results'].get(code)
        if providers:
          providers_buy = list(map(lambda x: {'provider': x['provider_name'], 'logo': f'{PROVIDER_BASE}/{x["logo_path"]}'}, providers.get('buy', {})))
          providers_rent = list(map(lambda x: {'provider': x['provider_name'], 'logo': f'{PROVIDER_BASE}/{x["logo_path"]}'}, providers.get('rent', {})))
          providers_others = list(map(lambda x: {'provider': x['provider_name'], 'logo': f'{PROVIDER_BASE}/{x["logo_path"]}'}, providers.get('flatrate', {})))
          current['buy'][location] = providers_buy
          current['rent'][location] = providers_rent
          current['providers'][location] = providers_others
  
    other_details = movie.details(details.get('id'))
    casts = other_details.casts.cast
    current['casts' ] = list(map(lambda x: {'name': x.get('name'), 'character': x.get('character'), 'photo': f'{PROVIDER_BASE}{x.get("profile_path")}'}, casts)) if casts else None 
    current['genres' ] = list(map(lambda x: x.get('name'), other_details.genres))

    # Fetch trailer URL
    url = f"https://api.themoviedb.org/3/movie/{details.get('id')}/videos"
    params = {
        "api_key": tmdb.api_key,
    }
    response = requests.get(url, params=params)
    trailer_url = None
    if response.status_code == 200:
        data = response.json()
        results = data.get("results", [])

        # Find the trailer URL
        for result in results:
            if result.get("type") == "Trailer":
                trailer_url = f"https://www.youtube.com/watch?v={result.get('key')}"
                break

        if not trailer_url:
            print(f"No trailer found for the movie: {movie_name}")
    current['trailer_url'] = trailer_url

    movie_list.append(current)

  return movie_list
