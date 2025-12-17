from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.decorators import permission_classes
from books.models import Book
from books.serializers import BookSerializer
from books.permissions import IsAdminOrReadOnly

@permission_classes([IsAdminOrReadOnly])
class BookList(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

@permission_classes([IsAdminOrReadOnly])
class BookDetails(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


