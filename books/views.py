from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, ListAPIView, CreateAPIView
from rest_framework.decorators import permission_classes
from rest_framework import filters, status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from books.models import Book, Publisher, Genre
from books.serializers import BookSerializer, PublisherSerializer, GenreSerializer
from books.permissions import IsAdminOrReadOnly
from books.services import parse_book


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

# @permission_classes([IsAdminUser])
# class BookCreate(CreateAPIView):


class BookListByCategory(ListAPIView):
    serializer_class = BookSerializer
    def get_queryset(self):
        queryset = Book.objects.all()
        category = self.kwargs['category']
        queryset = queryset.filter(bookgenre__genre__slug=category).order_by('-quantity')
        return queryset

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