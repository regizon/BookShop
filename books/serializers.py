import logging

from rest_framework import serializers

from books.models import Book, Genre, BookGenre, Author, BookAuthor, Publisher, BookCollection, Collection

logger = logging.getLogger(__name__)


class BookSerializer(serializers.ModelSerializer,):
    genres = serializers.ListField(required=True, child=serializers.IntegerField(), write_only=True)
    authors = serializers.ListField(required=True, child=serializers.CharField(), write_only=True)
    publisher = serializers.CharField(write_only=True)
    publisher_read = serializers.SerializerMethodField()
    author_read = serializers.SerializerMethodField()
    genres_read = serializers.SerializerMethodField()

    def validate_language(self, value):
        return value.capitalize()

    def validate_cover_type(self, value):
        return value.capitalize()

    class Meta:
        model = Book
        fields= ['author_read', 'id', 'title', 'description', 'price', 'discount_price', 'genres', 'genres_read',
                 'authors', 'cover', 'publisher', 'publisher_read', 'pages', 'cover_type', 'language', 'isbn', 'quantity']


    def get_publisher_read(self, obj):
        return obj.publisher.name

    def get_genres_read(self, obj):
        genre_ids = BookGenre.objects.values_list('genre', flat=True).filter(book=obj)
        genres = []
        for id in genre_ids:
            genre = Genre.objects.get(id=id).name
            genres.append(genre)
        return genres

    def get_author_read(self, obj):
        authors = []
        book_authors = BookAuthor.objects.filter(book=obj)
        for author in book_authors:
            authors.append(author.author.name)
        return authors

    def _sync_akcii_collection(self, book):
        if book.discount_price is not None:
            akcii, _ = Collection.objects.get_or_create(name='Акції')
            BookCollection.objects.get_or_create(book=book, collection=akcii)
        else:
            akcii = Collection.objects.filter(name='Акції').first()
            if akcii is not None:
                BookCollection.objects.filter(book=book, collection=akcii).delete()

    def update(self, instance, validated_data):
        genres = validated_data.pop('genres', None)
        authors = validated_data.pop('authors', None)
        publisher_name = validated_data.pop('publisher', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if publisher_name is not None:
            publisher = Publisher.objects.get_or_create(name=publisher_name)[0]
            instance.publisher = publisher

        instance.save()

        if authors is not None:
            BookAuthor.objects.filter(book=instance).delete()
            for author_name in authors:
                author = Author.objects.get_or_create(name=author_name)[0]
                BookAuthor.objects.create(book=instance, author=author)

        if genres is not None:
            BookGenre.objects.filter(book=instance).delete()
            for genre_id in genres:
                if not Genre.objects.filter(id=genre_id).exists():
                    raise serializers.ValidationError('Genre does not exist')
                genre = Genre.objects.get(id=genre_id)
                BookGenre.objects.create(book=instance, genre=genre)

        self._sync_akcii_collection(instance)

        return instance

    def create(self, validated_data):
        genres = validated_data.pop('genres')
        authors = validated_data.pop('authors')
        publisher_name = validated_data.pop('publisher')
        publisher = Publisher.objects.get_or_create(name=publisher_name)[0]
        book = Book.objects.create(**validated_data, publisher=publisher)

        for genre in genres:
            if not Genre.objects.filter(id=genre).exists():
                book.delete()
                raise serializers.ValidationError('Genre does not exist')

            genre = Genre.objects.get(id=genre)
            BookGenre.objects.create(book=book, genre=genre)

        for author_name in authors:
            author = Author.objects.get_or_create(name=author_name)[0]
            BookAuthor.objects.create(book=book, author=author)

        self._sync_akcii_collection(book)

        return book

class BookPreviewSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['title', 'cover', 'author']

    def get_author(self, obj):
        authors = []
        book_authors = BookAuthor.objects.filter(book=obj)
        for author in book_authors:
            authors.append(author.author.name)
        return authors

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = '__all__'

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name', 'slug']

class BookCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCollection
        fields = ['book', 'collection']

class CollectionSerializer(serializers.ModelSerializer):
    books = serializers.SerializerMethodField()

    def get_books(self, obj):
        book_collections = obj.bookcollection_set.all()
        books = [bc.book for bc in book_collections]
        return BookSerializer(books, many=True).data

    class Meta:
        model = Collection
        fields = ['id', 'name', 'slug', 'books']
