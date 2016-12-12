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
<<<<<<< HEAD
    birth_date = models.DateTimeField(blank=True, null=True)
    birth_place = models.ForeignKey(Place, on_delete=models.CASCADE, blank=True, null=True)


class Election(models.Model):
    date = models.DateTimeField(blank=True, null=True)
=======
    birthDate = models.DateTimeField('date published')
    birthPlace = models.DateTimeField('date published')


class Election(models.Model):
    date = models.DateTimeField('date published')
>>>>>>> 8ce7dd3421018eff5f999154540696d4219b2760
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    candidates = models.ManyToManyField(
        Candidate,
        through='Result',
        through_fields=('election', 'candidate'),
    )


class Result(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
<<<<<<< HEAD
    voting_result = models.DecimalField(max_digits=4, decimal_places=2)
=======
    votingResult = models.DecimalField(max_digits=4,decimal_places=2)
>>>>>>> 8ce7dd3421018eff5f999154540696d4219b2760


class PollInstitute(models.Model):
    name = models.CharField(max_length=50)
    grade = models.DecimalField(max_digits=4,decimal_places=2)


class Poll(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
<<<<<<< HEAD
    date = models.DateTimeField(blank=True, null=True)
=======
    date = models.DateTimeField('date published')
>>>>>>> 8ce7dd3421018eff5f999154540696d4219b2760
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=4,decimal_places=2)
    weight = models.DecimalField(max_digits=4,decimal_places=2)
<<<<<<< HEAD
    poll_institute = models.ForeignKey(PollInstitute, on_delete=models.CASCADE)
=======
    pollInstitute = models.ForeignKey(PollInstitute, on_delete=models.CASCADE)
>>>>>>> 8ce7dd3421018eff5f999154540696d4219b2760


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
<<<<<<< HEAD
    political_orientation = models.CharField(
=======
    year_in_school = models.CharField(
>>>>>>> 8ce7dd3421018eff5f999154540696d4219b2760
        max_length=2,
        choices=ORIENTATION_CHOICES,
        default=CENTER,
    )
<<<<<<< HEAD
    creationDate = models.DateTimeField(blank=True, null=True)
=======
    creationDate = models.DateTimeField('date published')
>>>>>>> 8ce7dd3421018eff5f999154540696d4219b2760
    parent = models.ForeignKey('Party', on_delete=models.CASCADE, blank = True, null = True)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    pass


<<<<<<< HEAD
class PoliticalFunction(models.Model):
=======
class Position(models.Model):
>>>>>>> 8ce7dd3421018eff5f999154540696d4219b2760
    position = models.CharField(max_length=50)


class Role(models.Model):
<<<<<<< HEAD
    beginning_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank = True, null=True)
    election = models.ForeignKey(Election, on_delete=models.CASCADE, blank=True, null=True)
    position_type = models.ForeignKey(PoliticalFunction, on_delete=models.CASCADE, blank=True, null=True)
=======
    beginningDate = models.DateTimeField('date published')
    endDate = models.DateTimeField('date published', blank = True, null = True)
    election = models.ForeignKey(Election, on_delete=models.CASCADE, blank = True, null = True)
    positionType = models.ForeignKey(Position, on_delete=models.CASCADE, blank = True, null = True)
>>>>>>> 8ce7dd3421018eff5f999154540696d4219b2760


class DetailedResults(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
<<<<<<< HEAD
    vote_number = models.IntegerField(default=0)
=======
    voteNumber = models.IntegerField(default=0)
>>>>>>> 8ce7dd3421018eff5f999154540696d4219b2760
