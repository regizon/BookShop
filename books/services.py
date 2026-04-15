import requests


class Book:
    def __init__(self, title, description, authors, page_count):
        self.title = title
        self.description = description
        self.author = authors
        self.page_count = page_count


def parse_book(title):
    api_url = f'https://www.googleapis.com/books/v1/volumes?q={title}&key=AIzaSyCtp3Yer6bXA83ZoM3lIOPUFJYdOoYufyE'
    response = requests.get(api_url)
    if 'items' in response.json().keys():
        for item in response.json()['items']:
            info = item['volumeInfo']
            if 'description' in info.keys():
                print(info['description'])
            # if info['description'] is not None and info['pageCount'] is not None and info['imageLinks'] is not None:
            #     book = Book(info['title'], info['description'], info['authors'], info['pageCount'])
            #     print(book)
            #     break
    else:
        print("error")