from autoslug import AutoSlugField
from django.db import models
from django.utils.text import slugify


class Author(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)

class Collection(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)

class Genre(models.Model):
    name = models.CharField(max_length=30, null=False, blank=False)
    slug = AutoSlugField(populate_from='name')

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.name)
    #
    #     super(Genre, self).save(*args, **kwargs)

class Publisher(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(max_length=1500, null=False)
    logo = models.TextField(max_length=500, null=False, blank=True)

class Book(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(max_length=1500, null=False)
    price = models.IntegerField(null=False, blank=False)
    cover = models.TextField(max_length=500, null=False)
    publisher = models.ForeignKey(Publisher, on_delete=models.PROTECT)
    pages = models.PositiveIntegerField()
    cover_type = models.CharField(max_length=50, null=False, blank=False)
    language = models.CharField(max_length=50, null=False, blank=False)
    isbn = models.CharField(max_length=13, unique=True)
    quantity = models.PositiveIntegerField()
    discount_price = models.IntegerField(null=True, blank=True)

class BookAuthor(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)


class BookGenre(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)


class BookCollection(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)