from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.validators import URLValidator
from django.db import models
from django.db.models import Avg, Count, Min, Max, StdDev, Sum
from django.template.defaultfilters import truncatechars

from libs.time import datetime_to_string

# Create your models here.

class Place(models.Model):
    country = models.TextField(max_length=50)
    region = models.TextField(max_length=50, blank=True, null=True)
    department = models.TextField(max_length=50, blank=True, null=True)
    county = models.TextField(max_length=50, blank=True, null=True)
    city = models.TextField(max_length=50, blank=True, null=True)

    def __str__(self):
        output = []
        for attr, value in self.__dict__.iteritems():
            if attr not in ["id", "_state"] and value:
                output.append(value)
        return str(output)

    def __unicode__(self):
        output = []
        for attr, value in self.__dict__.iteritems():
            if attr not in ["id", "_state"] and value:
                output.append(value)
        return ", ".join(output)


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


class Candidate(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    birth_date = models.DateTimeField(blank=True, null=True)
    birth_place = models.ForeignKey(Place, related_name="custom_birth_place", on_delete=models.CASCADE, blank=True, null=True)
    nationality = models.ForeignKey(Place, related_name="custom_nationality", on_delete=models.CASCADE, blank=True, null=True)
    image_url = models.TextField(validators=[URLValidator()], blank=True, null=True)
    party = models.ForeignKey(Party, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name + " " + self.surname

    def __unicode__(self):
        return self.name + " " + self.surname

    @property
    def image(self):
        return self.image_url

    @property
    def complete_name(self):
        return "%s %s" % (self.name, self.surname)


class Election(models.Model):
    name = models.CharField(max_length=50,blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    candidates = models.ManyToManyField(
        Candidate,
        through='Result',
        through_fields=('election', 'candidate'),
    )

    @property
    def print_name(self):
        if self.name == None:
            return ("Election du %s" % self.date)
        return "%s %s" % (self.name, self.date)


class Result(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    voting_result = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)


class TrendSource(models.Model):
    name = models.CharField(max_length=50)
    grade = models.DecimalField(blank=True, null=True, max_digits=4,decimal_places=2)

    def __str__(self):
        return self.name + " - " + ("grade : %s" % (self.grade))

    def __unicode__(self):
        return self.name + " - " + ("grade : %s" % (self.grade))


class Trend(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    date = models.DateTimeField(blank=True, null=True)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=10,decimal_places=3)
    weight = models.DecimalField(blank=True, null=True, max_digits=10,decimal_places=3)
    trend_source = models.ForeignKey(TrendSource, on_delete=models.CASCADE)

    def __unicode__(self):
        output = []
        for attr, value in self.__dict__.iteritems():
            if attr in ["date"]:
                output.append(datetime_to_string(value))
            elif attr in ["place", "election", "candidate", "score", "weight", "trend_source"]:
                output.append(str(value))
            elif attr not in ["id", "_state"] and value:
                output.append(str(value))
        return ", ".join(output)



class PoliticalFunction(models.Model):
    position = models.CharField(max_length=200)

    @property
    def short_description(self):
        return truncatechars(self.position, 100)

    def __str__(self):
        return self.position

    def __unicode__(self):
        return self.position


class Role(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, blank=True, null=True)
    beginning_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    election = models.ForeignKey(Election, on_delete=models.CASCADE, blank=True, null=True)
    position_type = models.ForeignKey(PoliticalFunction, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.position_type_id) + " " + str(self.candidate_id)

    def __unicode__(self):
        output = []
        for attr, value in self.__dict__.iteritems():
            if attr in ["beginning_date", "end_date"] and value:
                output.append(datetime_to_string(value))
            elif attr in ["candidate", "election", "position_type"]:
                output.append(str(value))
            elif attr not in ["id", "_state"] and value:
                output.append(value)
        return ", ".join(map(str, output))


class DetailedResults(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    vote_number = models.IntegerField(default=0)


class Statistics(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=4 ,decimal_places=3)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    def get_results(self):
        twitter = TrendSource.objects.get(name="Twitter")
        twitter_weight_sum = Trend.objects.filter(
            trend_source_id=twitter.id,
            date__gte=self.start_date,
            date__lte=self.end_date).aggregate(weight_sum=Sum("weight"))
        twitter_stats = Trend.objects.filter(
            trend_source_id=twitter.id,
            candidate_id=self.candidate.id,
            date__gte=self.start_date,
            date__lte=self.end_date).aggregate(average=Avg("score"), weight_sum=Sum("weight"), standard_deviation=StdDev("score"), min_value=Min("score"), max_value=StdDev("score"))
        google = TrendSource.objects.get(name="Google Trends")
        google_stats = Trend.objects.filter(
            trend_source_id=google.id,
            candidate_id=self.candidate.id,
            election_id=self.election.id,
            date__gte=self.start_date,
            date__lte=self.end_date).aggregate(average=Avg("score"), standard_deviation=StdDev("score"), min_value=Min("score"), max_value=StdDev("score"))
        return [twitter_weight_sum, twitter_stats, google_stats]
