from django.urls import path
from books import views
urlpatterns = [
    path("", views.BookList.as_view(), name="books"),
    path("collections/", views.BookCollectionList.as_view(), name="collections"),
    path('collections/<int:pk>/', views.CollectionDetail.as_view(), name="collection_detail"),
    path('collections/book-collections/', views.BookCollectionPairsList.as_view(), name="collection_pairs"),
    path("category/<slug:category>/filters/", views.BookCategoryFilters.as_view(), name="category_filters"),
    path("category/<slug:category>/", views.BookListByCategory.as_view(), name="category"),
    path("parse/", views.BookParser.as_view(), name="parse"),
    path("<int:pk>/", views.BookDetails.as_view(), name="book_details"),
    path("publishers/", views.PublisherList.as_view(), name="publishers"),
    path("publishers/<int:pk>/", views.PublisherDetails.as_view(), name="publisher_details"),
    path("genres/", views.GenreList.as_view(), name="genres"),
]