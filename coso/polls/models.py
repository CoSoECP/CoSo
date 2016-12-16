from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Place(models.Model):
    country = models.TextField(max_length=50)
    region = models.TextField(max_length=50, blank=True, null=True)
    department = models.TextField(max_length=50, blank=True, null=True)
    county = models.TextField(max_length=50, blank=True, null=True)
    city = models.TextField(max_length=50, blank=True, null=True)


class Candidate(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    birth_date = models.DateTimeField(blank=True, null=True)
    birth_place = models.ForeignKey(Place, on_delete=models.CASCADE, blank=True, null=True)


class Election(models.Model):
    date = models.DateTimeField(blank=True, null=True)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    candidates = models.ManyToManyField(
        Candidate,
        through='Result',
        through_fields=('election', 'candidate'),
    )


class Result(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    voting_result = models.DecimalField(max_digits=4, decimal_places=2)


class PollInstitute(models.Model):
    name = models.CharField(max_length=50)
    grade = models.DecimalField(max_digits=4,decimal_places=2)


class Poll(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    date = models.DateTimeField(blank=True, null=True)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=4,decimal_places=2)
    weight = models.DecimalField(max_digits=4,decimal_places=2)
    poll_institute = models.ForeignKey(PollInstitute, on_delete=models.CASCADE)


class Party(models.Model):
    name = models.CharField(max_length=50)
    FARLEFT = 'FL'
    LEFT = 'LE'
    CENTER = 'CE'
    RIGHT = 'RI'
    FARRIGHT = 'FR'
    ORIENTATION_CHOICES = (
        (FARLEFT, 'FarLeft'),
        (LEFT, 'Left'),
        (CENTER, 'Center'),
        (RIGHT, 'Right'),
        (FARRIGHT, 'FarRight'),
    )
    political_orientation = models.CharField(
        max_length=2,
        choices=ORIENTATION_CHOICES,
        default=CENTER,
    )
    creation_date = models.DateTimeField(blank=True, null=True)
    parent = models.ForeignKey('Party', on_delete=models.CASCADE, blank = True, null = True)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    pass


class PoliticalFunction(models.Model):
    position = models.CharField(max_length=50)


class Role(models.Model):
    beginning_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank = True, null=True)
    election = models.ForeignKey(Election, on_delete=models.CASCADE, blank=True, null=True)
    position_type = models.ForeignKey(PoliticalFunction, on_delete=models.CASCADE, blank=True, null=True)


class DetailedResults(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    vote_number = models.IntegerField(default=0)
