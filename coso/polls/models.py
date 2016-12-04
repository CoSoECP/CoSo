from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Place(models.Model):
    country = models.TextField(max_length=50)
    region = models.TextField(max_length=50, blank=True, null=True)
    department = models.TextField(max_length=50, blank=True, null=True)
    county = models.TextField(max_length=50, blank=True, null=True)
    city = models.TextField(max_length=50, blank=True, null=True)