from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    isbn = models.CharField(max_length=255)
    sub_title = models.TextField()
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, related_name='books')
    authors = models.ManyToManyField(Author, related_name='books')
    published = models.PositiveSmallIntegerField(default=2020)
    size = models.DecimalField(max_digits=4, decimal_places=2)
    price = models.PositiveIntegerField(default=2000)
    link = models.CharField(max_length=255)
    image_link_arvan = models.CharField(default='1.jpg', max_length=255)
    image_link_scrap = models.CharField(max_length=255)
    description = models.TextField()
    file_link = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class ExtraInfo(models.Model):
    key = models.CharField(max_length=100)
    value = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.key } : {self.value}"
