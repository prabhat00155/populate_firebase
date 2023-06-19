import requests


def fetch(books):
  API_KEY = 'AIzaSyAf6HI9iU3jzVZBP9Jgf5cSiXRnmQ8O9Gk'
  book_list = []
  for book_name, locations in books.items():
    url = f'https://www.googleapis.com/books/v1/volumes?q={book_name.strip().replace(" ", "_")}&key={API_KEY}'
    response = requests.get(url)
    data = response.json()
    if 'items' not in data:
      url = f'https://www.googleapis.com/books/v1/volumes?q={book_name.strip()}&key={API_KEY}'
      response = requests.get(url)
      data = response.json()
    if 'items' in data:
      books = data['items']
      if books:
        book = books[0] 
        current = {}
        current['name'] = book['volumeInfo']['title']
        current['authors'] = book['volumeInfo']['authors'] if 'authors' in book['volumeInfo'] else ['Unknown author']
        current['publisher'] = book['volumeInfo'].get('publisher')
        current['publishedDate'] = book['volumeInfo'].get('publishedDate')
        current['pageCount'] = book['volumeInfo'].get('pageCount')
        current['categories'] = book['volumeInfo'].get('categories')
        current['thumbnail'] = book['volumeInfo'].get('imageLinks').get('thumbnail')
        current['language'] = book['volumeInfo'].get('language')
        current['description'] = book['volumeInfo'].get('description')
        current['locations'] = locations 
        book_list.append(current)
  return book_list
