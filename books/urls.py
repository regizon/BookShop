from django.urls import path
from books import views
urlpatterns = [
    path("", views.BookList.as_view(), name="books"),
    path("<int:pk>/", views.BookDetails.as_view(), name="book_details"),

]