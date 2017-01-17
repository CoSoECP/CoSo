import json
import urllib2
from bs4 import BeautifulSoup

from django.http import HttpResponse
from django.shortcuts import render

from polls.models import Election, Place, Candidate, Result

import datetime

from pytrends.request import TrendReq
import pandas

google_username = "cosoecp@gmail.com"
google_password = "cosoecp2017"
path = ""

def sondage_2012(request):
    wiki = "http://www.sondages-en-france.fr/sondages/Elections/Pr%C3%A9sidentielles%202012"
    page = urllib2.urlopen(wiki)
    soup = BeautifulSoup(page)
    right_table = soup.find("table",class_="summaryTable")
    data = [[]]

    for row in right_table.findAll("tr"):
        cells=row.findAll("td")
        if len(cells) == 14:
            for i in range(len(data)):
                data[i].append(cells[i].get_text())
    return HttpResponse("Hello, we've done the scrapping")


def import_trends(request_content):

    vecteur = request_content[0]
    pays = request_content[1]
    date = request_content[2]

    # connect to Google
    pytrend = TrendReq(google_username, google_password, custom_useragent='My Coso Script')


    trend_payload = {'q': vecteur, 'hl': 'fr-FR', 'geo': pays,'date': date + ' 2m'}

    # trend
    trend = pytrend.trend(trend_payload)
    df = pytrend.trend(trend_payload, return_type='dataframe')
    return(df)



def new_election():
    _place, created = Place.objects.get_or_create(country="France")
    _election, created = Election.objects.get_or_create(date=datetime.datetime(2016,12,05), place_id = _place.id)
    _candidate1, created = Candidate.objects.get_or_create(name="Valls", surname = "Manuel", birth_date=datetime.datetime(1968,12,05), birth_place_id= _place.id, nationality="French")
    _candidate2, created = Candidate.objects.get_or_create(name="Peillon", surname = "Vincent", birth_date=datetime.datetime(1968,12,05), birth_place_id= _place.id, nationality="French")
    _result1, created = Result.objects.get_or_create(election_id = _election.id, candidate_id = _candidate1.id)
    _result2, created = Result.objects.get_or_create(election_id = _election.id, candidate_id = _candidate2.id)


def analysis_from_google(request):
    new_election()
    data=[]
    elections = Election.object.all()
    for election in elections:
        request_content = []
        liste_candidat = []
        candidats=election.candidates
        for candidat in candidats:
            liste_candidat.append(candidat)
        vecteur_candidat=", ".join(liste_candidat)
        date=election.date
        annee=date.year
        mois=date.month
        date_temp=[mois,annee]
        date_format="/".join(date_temp)
        request_content.append(vecteur_candidat)
        request_content.append("FR")
        request_content.append(date_format)
        data.append(import_trends(request_content))
    print(data)
    return HttpResponse("Hello, we've done the Google Analysis")

