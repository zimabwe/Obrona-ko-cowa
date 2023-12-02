from django.db import models


GENERE = (
    (-1, "not defined"),
    (0, "rock"),
    (1, "metal"),
    (2, "pop"),
    (3, "hiphop"),
    (4,"electronic"),
    (5, "regge"),
    (6, "other")
)

ARTICLE_STATUSES = (
    (0, 'in progres'),
    (1, 'waitnig for approval'),
    (2, 'published')
)

SCORE = (
    (0, ' '),
    (1, '*'),
    (2, '**'),
    (3, '***'),
    (4, '****'),
    (5, '*****')
)
# Create your models here.
class Band(models.Model):
    name = models.CharField(max_length=64)
    year = models.IntegerField(null=True)
    still_active = models.BooleanField(default=True)
    genere = models.IntegerField(choices=GENERE, default=-1)


class Category(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(null=True)



class Article(models.Model):
    title = models.CharField(max_length=128)
    author = models.CharField(max_length=64, null=True)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=ARTICLE_STATUSES)
    published_date_start = models.DateTimeField(null=True)
    published_date_end = models.DateTimeField(null=True)
    category = models.ManyToManyField(Category)

class Album(models.Model):
    title = models.CharField(max_length=128)
    year_of_emmision = models.DateField
    score = models.IntegerField(choices=SCORE)
    band = models.ForeignKey(Band, on_delete=models.CASCADE, null=True)

class Song(models.Model):
    title = models.CharField(max_length=128)
    duration = models.TimeField(null= True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)

class Person(models.Model):
    name = models.CharField(max_length=128)

class Position(models.Model):
    position_name= models.CharField(max_length=128)
    salary = models.DecimalField(max_digits=8, decimal_places=2)
    person = models.OneToOneField(Person, on_delete=models.CASCADE)