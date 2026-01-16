from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.decorators import permission_classes
from books.models import Book, Publisher, Genre
from books.serializers import BookSerializer, PublisherSerializer, GenreSerializer
from books.permissions import IsAdminOrReadOnly

@permission_classes([IsAdminOrReadOnly])
class BookList(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

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