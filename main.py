from collections import defaultdict
import importlib

from firebase_admin import firestore
import firebase_admin

import scrape_google


def populate_firebase(data, category):
  db = firestore.client()
  for d in data:
    db.collection(category).document(d['name']).set(d)


locations = [
  'US',
  'UK',
  'India',
  'World',
]
categories = [
  'movies',
  'tv shows',
  'books',
  'apps',
  'games',
  'songs',
]
use_scraping = True 
data_dir = 'data'


def main():
  app = firebase_admin.initialize_app()
  for category in categories:
    try:
      module = importlib.import_module(category.replace(' ', ''))
    except ModuleNotFoundError:
      print(f'{category}.py not present')
    item_and_location = defaultdict(list)
    for location in locations:
      print(f'Processing {category} for {location}')
      items_list = scrape_google.trending(category, location) if use_scraping else []
      if not items_list:
        fname = f'{data_dir}/{category.replace(" ", "")}_{location.lower()}.txt'
        try:
          with open(fname) as file:
            data = file.read()
          items_list = data.strip().split('\n')
        except FileNotFoundError:
          print(f'File not found: {fname}')
      for item in items_list:
        item_and_location[item].append(location)
    item_list = module.fetch(item_and_location)
    populate_firebase(item_list, category)


if __name__ == '__main__':
  main()
