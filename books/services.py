import requests


class Book:
    def __init__(self, title, description, authors, page_count):
        self.title = title
        self.description = description
        self.author = authors
        self.page_count = page_count


def parse_book(title, author, publisher):
    if publisher:
        api_url = f'https://www.googleapis.com/books/v1/volumes?q={title}&author={author}&inpublisher={publisher}&key=AIzaSyCtp3Yer6bXA83ZoM3lIOPUFJYdOoYufyE'
    else:
        api_url = f'https://www.googleapis.com/books/v1/volumes?q={title}&author={author}&key=AIzaSyCtp3Yer6bXA83ZoM3lIOPUFJYdOoYufyE'
    response = requests.get(api_url)
    best_choice = None
    if 'items' in response.json().keys():
        for item in response.json()['items']:
            info = item['volumeInfo']
            if 'description' in info.keys() and 'pageCount' in info.keys() and 'imageLinks' in info.keys() and 'publisher' in info.keys():
                best_choice = info
                break
    else:
        print("error")

    return best_choice