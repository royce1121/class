from django.db import models

# Create your models here.
class Person(models.Model):
    First_name = models.CharField(max_length=30)
    Last_name = models.CharField(max_length=30)
    contact = models.CharField(max_length=11)
    address = models.CharField(max_length=100, blank=True)
    author = models.CharField(max_length=30)

class Person1(models.Model):
    First_name = models.CharField(max_length=30)
    Last_name = models.CharField(max_length=30)
    contact = models.CharField(max_length=11)
    address = models.CharField(max_length=100, blank=True)