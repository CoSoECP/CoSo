import json
import urllib2
from bs4 import BeautifulSoup

from django.http import HttpResponse
from django.shortcuts import render

from polls.models import Election, Place, Candidate, Result, Trend, TrendSource

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
    _election, created = Election.objects.get_or_create(date=datetime.datetime(2016,12,22), place_id = _place.id)
    _candidate1, created = Candidate.objects.get_or_create(name="Valls", surname = "Manuel", birth_date=datetime.datetime(1968,12,05), birth_place_id= _place.id, nationality_id= _place.id)
    _candidate2, created = Candidate.objects.get_or_create(name="Peillon", surname = "Vincent", birth_date=datetime.datetime(1968,12,05), birth_place_id= _place.id, nationality_id= _place.id)
    _result1, created = Result.objects.get_or_create(election_id = _election.id, candidate_id = _candidate1.id)
    _result2, created = Result.objects.get_or_create(election_id = _election.id, candidate_id = _candidate2.id)
    


def analysis_from_google(request, election_id):
    #elections = Election.objects.all()
    elections = [Election.objects.get(id=election_id)]
    _twitter, created = TrendSource.objects.get_or_create(name = "Twitter")
    total = 0.00
    data=[]
    for election in elections:
        request_content = []
        liste_candidat = []
        candidats=election.candidates.all()
        for candidat in candidats:
            liste_candidat.append(candidat.surname + " " + candidat.name)
        vecteur_candidat=", ".join(liste_candidat)
        date=election.date
        mois = date.month
        annee=date.year
        #if date.month > 1:
        #    mois = date.month - 1
        #    annee=date.year
        #else:
        #    mois = 12
        #    annee=date.year - 1
        date_temp=[str(mois),str(annee)]
        date_format="/".join(date_temp)
        request_content.append(vecteur_candidat)
        request_content.append("FR")
        request_content.append(date_format)
        my_data = import_trends(request_content)
        for daily_date in my_data.index:
            for candidate in candidats:
                total = 0
                candidate_name =  candidate.surname + " " + candidate.name
                if (isinstance(my_data.loc[daily_date, candidate_name.lower()], (int, float, long))):
                    candidate_weight = round(float(my_data.loc[daily_date, candidate_name.lower()]),2)
                total = total + candidate_weight
            for candidate in candidats:
                candidate_name =  candidate.surname + " " + candidate.name
                if (total !=0 and str(total) != "nan"):
                    _trend, created = Trend.objects.get_or_create(place_id = election.place.id, date = pandas.to_datetime(daily_date), election_id = election.id, candidate_id = candidate.id, score = round(candidate_weight/total,2), weight = candidate_weight, trend_source_id = _twitter.id)
    return HttpResponse("Hello, we've done the Google Analysis")
