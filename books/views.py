from django.db.models import Prefetch, Case, When, IntegerField, Min, Max
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, ListAPIView, CreateAPIView
from rest_framework.decorators import permission_classes
from rest_framework import filters, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from books.models import Book, Publisher, Genre, BookCollection, Collection, Author
from books.serializers import BookSerializer, PublisherSerializer, GenreSerializer, BookCollectionSerializer, \
    CollectionSerializer
from books.permissions import IsAdminOrReadOnly
from books.services import parse_book


@permission_classes([IsAdminOrReadOnly])
class BookList(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']


@permission_classes([IsAdminOrReadOnly])
class BookCollectionPairsList(ListCreateAPIView):
    queryset = BookCollection.objects.all()
    serializer_class = BookCollectionSerializer

    def delete(self, request):
        book_id = request.data.get('book')
        collection_id = request.data.get('collection')
        if collection_id and book_id:
            deleted_count, _ = BookCollection.objects.filter(book_id=book_id, collection_id=collection_id).delete()

            if deleted_count:
                return Response({"message": "Book was deleted successfully"}, status=status.HTTP_200_OK)

            return Response({'message': "Book wasn't found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({'message': 'Both book_id and collection_id are required'}, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([IsAdminOrReadOnly])
class CollectionDetail(RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.name == 'Акції':
            return Response(
                {'message': "Collection 'Акції' cannot be deleted because it is used for discounted books."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().destroy(request, *args, **kwargs)


@permission_classes([IsAdminOrReadOnly])
class BookCollectionList(ListCreateAPIView):
    queryset = Collection.objects.prefetch_related(
        Prefetch(
            'bookcollection_set',
            queryset=BookCollection.objects.select_related('book').annotate(
                in_stock=Case(
                    When(book__quantity=0, then=1),
                    default=0,
                    output_field=IntegerField()
                )
            ).order_by('in_stock')
        )
    )

    serializer_class = CollectionSerializer


class CategoryPagePagination(PageNumberPagination):
    page_size = 10


class BookListByCategory(ListAPIView):
    serializer_class = BookSerializer
    pagination_class = CategoryPagePagination

    def get_queryset(self):
        queryset = Book.objects.filter(bookgenre__genre__slug=self.kwargs['category'])

        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        if min_price is not None:
            queryset = queryset.filter(price__gte=min_price)
        if max_price is not None:
            queryset = queryset.filter(price__lte=max_price)

        authors = self.request.query_params.getlist('authors')
        if authors:
            queryset = queryset.filter(bookauthor__author__name__in=authors)

        languages = self.request.query_params.getlist('language')
        if languages:
            queryset = queryset.filter(language__in=languages)

        cover_types = self.request.query_params.getlist('cover_type')
        if cover_types:
            queryset = queryset.filter(cover_type__in=cover_types)

        return queryset.distinct().order_by('-quantity')


class BookCategoryFilters(APIView):
    def get(self, request, category):
        base_qs = Book.objects.filter(bookgenre__genre__slug=category)
        genre = Genre.objects.filter(slug=category).first()

        authors = list(
            Author.objects.filter(bookauthor__book__in=base_qs)
            .values_list('name', flat=True)
            .distinct()
        )
        languages = list(base_qs.values_list('language', flat=True).distinct())
        cover_types = list(base_qs.values_list('cover_type', flat=True).distinct())
        prices = base_qs.aggregate(min_price=Min('price'), max_price=Max('price'))

        return Response({
            'genre_name': genre.name if genre else category,
            'authors': authors,
            'languages': languages,
            'cover_types': cover_types,
            'min_price': prices['min_price'] or 0,
            'max_price': prices['max_price'] or 0,
        })

class BookListByCollection(ListAPIView):
    serializer_class = BookSerializer
    pagination_class = CategoryPagePagination

    def get_queryset(self):
        queryset = Book.objects.filter(bookcollection__collection__slug=self.kwargs['slug'])

        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        if min_price is not None:
            queryset = queryset.filter(price__gte=min_price)
        if max_price is not None:
            queryset = queryset.filter(price__lte=max_price)

        authors = self.request.query_params.getlist('authors')
        if authors:
            queryset = queryset.filter(bookauthor__author__name__in=authors)

        languages = self.request.query_params.getlist('language')
        if languages:
            queryset = queryset.filter(language__in=languages)

        cover_types = self.request.query_params.getlist('cover_type')
        if cover_types:
            queryset = queryset.filter(cover_type__in=cover_types)

        return queryset.distinct().order_by('-quantity')


class CollectionFilters(APIView):
    def get(self, request, slug):
        base_qs = Book.objects.filter(bookcollection__collection__slug=slug)
        collection = Collection.objects.filter(slug=slug).first()

        authors = list(
            Author.objects.filter(bookauthor__book__in=base_qs)
            .values_list('name', flat=True)
            .distinct()
        )
        languages = list(base_qs.values_list('language', flat=True).distinct())
        cover_types = list(base_qs.values_list('cover_type', flat=True).distinct())
        prices = base_qs.aggregate(min_price=Min('price'), max_price=Max('price'))

        return Response({
            'collection_name': collection.name if collection else slug,
            'authors': authors,
            'languages': languages,
            'cover_types': cover_types,
            'min_price': prices['min_price'] or 0,
            'max_price': prices['max_price'] or 0,
        })


@permission_classes([IsAdminUser])
class BookParser(APIView):
    def get(self, request):
        author = request.query_params.get('author', None)
        title = request.query_params.get('title', None)
        publisher = request.query_params.get('publisher', None)
        if title:
            book_info = parse_book(title, author, publisher)
            if book_info:
                return Response({"message": book_info}, status=status.HTTP_200_OK)
            return Response({"message": "Book wasn't found or something went wrong with Books API"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "author and title are required"}, status=status.HTTP_400_BAD_REQUEST)
@permission_classes([IsAdminOrReadOnly])
class BookDetails(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

@permission_classes([IsAdminOrReadOnly])
class PublisherList(ListCreateAPIView):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer

@permission_classes([IsAdminOrReadOnly])
class PublisherDetails(RetrieveUpdateDestroyAPIView):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer


@permission_classes([IsAdminOrReadOnly])
class GenreList(ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer