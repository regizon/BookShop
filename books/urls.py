from django.urls import path
from books import views
urlpatterns = [
    path("", views.BookList.as_view(), name="books"),
    path("category/<slug:category>/", views.BookListByCategory.as_view(), name="category"),
    path("<int:pk>/", views.BookDetails.as_view(), name="book_details"),
    path("publishers/", views.PublisherList.as_view(), name="publishers"),
    path("publishers/<int:pk>/", views.PublisherDetails.as_view(), name="publisher_details"),
    path("genres/", views.GenreList.as_view(), name="genres"),
]