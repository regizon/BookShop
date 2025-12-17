from rest_framework import serializers

from books.models import Book, Genre, BookGenre, Author, BookAuthor


class BookSerializer(serializers.ModelSerializer,):
    genres = serializers.ListField(required=True, child=serializers.IntegerField(), write_only=True)
    authors = serializers.ListField(required=True, child=serializers.CharField(), write_only=True)
    author_read = serializers.SerializerMethodField()
    genres_read = serializers.SerializerMethodField()
    class Meta:
        model = Book
        fields= ['author_read', 'id', 'title', 'description', 'price', 'pub_date', 'genres', 'genres_read', 'authors']

    def get_genres_read(self, obj):
        book_genres = BookGenre.objects.filter(book=obj)
        genres = book_genres.values_list('genre', flat=True)
        return genres

    def get_author_read(self, obj):
        authors = []
        book_authors = BookAuthor.objects.filter(book=obj)
        for author in book_authors:
            authors.append(author.author.name)
        print(authors)
        return authors

    def create(self, validated_data):
        genres = validated_data.pop('genres')
        authors = validated_data.pop('authors')
        book = Book.objects.create(**validated_data)

        for genre in genres:
            if not Genre.objects.filter(id=genre).exists():
                book.delete()
                raise serializers.ValidationError('Genre does not exist')

            genre = Genre.objects.get(id=genre)
            BookGenre.objects.create(book=book, genre=genre)

        for author_name in authors:
            author = Author.objects.get_or_create(name=author_name)[0]
            BookAuthor.objects.create(book=book, author=author)

        return book