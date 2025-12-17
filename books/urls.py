from django.urls import path
from books import views
urlpatterns = [
    path("books/", views.BookList.as_view(), name="books"),
    path("books/<int:pk>/", views.BookDetails.as_view(), name="book_details"),

]