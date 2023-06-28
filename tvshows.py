from tmdbv3api import TMDb
from tmdbv3api import TV
from firebase_admin import firestore
import firebase_admin


country_code = {
  'US': 'US',
  'UK': 'GB',
  'India': 'IN',
}

def fetch(tvshows):
  tmdb = TMDb()
  tmdb.api_key = '4a19dfe65c6b0684fcc5937ee00fd6d9'
  tmdb.language = 'en'
  #for debugging we have set it true 
  tmdb.debug = True
  tv_show = TV()
  WIDTH = 200
  URL_BASE = 'http://image.tmdb.org/t/p/w'
  PROVIDER_BASE = 'https://image.tmdb.org/t/p/original'
  tv_show_list = [] 
  for tv_show_name, locations in tvshows.items():
    current = {}
    details = tv_show.search(tv_show_name)
    if details:
      details = details[0]
    else:
      print(f'{tv_show_name} not found')
      continue
    current['name'] = details.name
    current['url'] = f'{URL_BASE}{WIDTH}/{details.poster_path}'
    current['overview'] = details.overview
    current['first_air_date'] = details.first_air_date
    current['origin_country'] = details.origin_country
    current['language'] = details.original_language
    current['locations'] = locations 

    current['buy'] = {} 
    current['rent'] = {} 
    current['providers'] = {}
    for location in locations:
      code = country_code.get(location)
      if code:
        providers = tv_show.watch_providers(details['id'])['results'].get(code)
        if providers:
          providers_buy = list(map(lambda x: {'provider': x['provider_name'], 'logo': f'{PROVIDER_BASE}/{x["logo_path"]}'}, providers.get('buy', {})))
          providers_rent = list(map(lambda x: {'provider': x['provider_name'], 'logo': f'{PROVIDER_BASE}/{x["logo_path"]}'}, providers.get('rent', {})))
          providers_others = list(map(lambda x: {'provider': x['provider_name'], 'logo': f'{PROVIDER_BASE}/{x["logo_path"]}'}, providers.get('flatrate', {})))
          current['buy'][location] = providers_buy
          current['rent'][location] = providers_rent
          current['providers'][location] = providers_others
  
    other_details = tv_show.details(details.get('id'))
    current['is_running'] = other_details.status == 'Returning Series'
    casts = other_details.credits.cast
    current['casts' ] = list(map(lambda x: {'name': x.get('name'), 'character': x.get('character'), 'photo': f'{PROVIDER_BASE}{x.get("profile_path")}'}, casts)) if casts else None 

    current['last_air_date'] = other_details.last_air_date 
    current['number_of_seasons'] = other_details.number_of_seasons
    current['number_of_episodes'] = other_details.number_of_episodes
    current['genres' ] = list(map(lambda x: x.get('name'), other_details.genres))

    tv_show_list.append(current)

  return tv_show_list
