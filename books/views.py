from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, ListAPIView
from rest_framework.decorators import permission_classes
from rest_framework import filters
from books.models import Book, Publisher, Genre
from books.serializers import BookSerializer, PublisherSerializer, GenreSerializer
from books.permissions import IsAdminOrReadOnly

@permission_classes([IsAdminOrReadOnly])
class BookList(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    # def get_queryset(self):
    #     queryset = Book.objects.all()
    #     category = self.request.query_params.get('category')
    #     if category is not None:
    #         queryset = queryset.filter(bookgenre__genre__name=category.capitalize())
    #     return queryset


class BookListByCategory(ListAPIView):
    serializer_class = BookSerializer
    def get_queryset(self):
        queryset = Book.objects.all()
        category = self.kwargs['category']
        queryset = queryset.filter(bookgenre__genre__slug=category)
        return queryset


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