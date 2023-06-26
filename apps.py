import requests


def fetch(apps):
  app_list = []
  for app_name, locations in apps.items():
    response = requests.get(f"https://itunes.apple.com/search?term={app_name}&entity=software")
    data = response.json()

    # Access the desired information
    if data['resultCount'] > 0:
        current = {}
        app = data['results'][0]
        current['name'] = app['trackName']
        current['publisher'] = app['artistName']
        current['genres'] = app['genres']
        current['description'] = app['description']
        current['app_url'] = app['trackViewUrl']
        current['image_url'] = app['artworkUrl512']
        current['contentAdvisoryRating'] = app['contentAdvisoryRating']
        current['app_rating'] = app['averageUserRating']
        current['app_reviews'] = app['userRatingCount']
        current['locations'] = locations
        app_list.append(current)
  return app_list


