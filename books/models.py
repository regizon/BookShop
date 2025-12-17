from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(max_length=500, null=False)
    price = models.FloatField(null=False)
    pub_date = models.DateTimeField('date published')

class Author(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)


class Genre(models.Model):
    name = models.CharField(max_length=30, null=False, blank=False)

class BookAuthor(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

class BookGenre(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
