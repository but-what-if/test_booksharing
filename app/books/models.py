from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    date_of_birth = models.CharField(max_length=64)
    date_of_death = models.CharField(max_length=64)
    country = models.CharField(max_length=128)
    gender = models.CharField(max_length=32)
    language = models.CharField(max_length=64)


class Category(models.Model):
    name = models.CharField(max_length=128)


class Book(models.Model):
    title = models.CharField(max_length=128)
    publish_year = models.PositiveIntegerField()
    review = models.CharField(max_length=512)
    condition = models.PositiveSmallIntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                               null=True, default=None)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE,
                             null=True, default=None)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL,
                               null=True, default=None)


class Log(models.Model):
    path = models.CharField(max_length=500)
    method = models.CharField(max_length=32)
    time = models.PositiveIntegerField()
