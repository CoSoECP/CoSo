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
    birthDate = models.DateTimeField('date published')
    birthPlace = models.DateTimeField('date published')


class Election(models.Model):
    date = models.DateTimeField('date published')
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    candidates = models.ManyToManyField(
        Candidate,
        through='Result',
        through_fields=('election', 'candidate'),
    )


class Result(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    votingResult = models.DecimalField(max_digits=4,decimal_places=2)


class PollInstitute(models.Model):
    name = models.CharField(max_length=50)
    grade = models.DecimalField(max_digits=4,decimal_places=2)


class Poll(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    date = models.DateTimeField('date published')
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=4,decimal_places=2)
    weight = models.DecimalField(max_digits=4,decimal_places=2)
    pollInstitute = models.ForeignKey(PollInstitute, on_delete=models.CASCADE)


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
    year_in_school = models.CharField(
        max_length=2,
        choices=ORIENTATION_CHOICES,
        default=CENTER,
    )
    creationDate = models.DateTimeField('date published')
    parent = models.ForeignKey('Party', on_delete=models.CASCADE, blank = True, null = True)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    pass


class Position(models.Model):
    position = models.CharField(max_length=50)


class Role(models.Model):
    beginningDate = models.DateTimeField('date published')
    endDate = models.DateTimeField('date published', blank = True, null = True)
    election = models.ForeignKey(Election, on_delete=models.CASCADE, blank = True, null = True)
    positionType = models.ForeignKey(Position, on_delete=models.CASCADE, blank = True, null = True)


class DetailedResults(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    voteNumber = models.IntegerField(default=0)
