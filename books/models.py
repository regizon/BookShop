from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)


class Genre(models.Model):
    name = models.CharField(max_length=30, null=False, blank=False)

class Publisher(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(max_length=1500, null=False)
    logo = models.TextField(max_length=500, null=False, blank=True)

class Book(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(max_length=1500, null=False)
    price = models.IntegerField(null=False, blank=False)
    cover = models.TextField(max_length=500, null=False)
    pub_date = models.DateTimeField('date published')
    publisher = models.ForeignKey(Publisher, on_delete=models.PROTECT)
    pages = models.PositiveIntegerField()
    cover_type = models.CharField(max_length=50, null=False, blank=False)
    language = models.CharField(max_length=50, null=False, blank=False)
    isbn = models.CharField(max_length=13, unique=True)

class BookAuthor(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)


class BookGenre(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)