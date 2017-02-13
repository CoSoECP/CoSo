# -*- coding: UTF-8 -*-
from coso.settings import WIKIPEDIA_BASE_API_URL, API_KEYS, GOOGLE_USERNAME, GOOGLE_PASSWORD
from polls.models import Candidate, Place, PoliticalFunction, Role, Trend, Election, Result, TrendSource

from libs.time import to_datetime
from libs import got

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseNotFound
from django.http import HttpResponse

from bs4 import BeautifulSoup
from datetime import datetime, time, timedelta
from json import load
from pytrends.request import TrendReq
from repustate import Client
from threading import Thread

import json
import logging
import os
import pandas
import requests
import sys
import tweepy
import urllib2

path = ""

@require_http_methods(["GET"])
def french_candidates(request):
    # Only GET request will go that far
    json_data = open('./static/french_politicians.json')
    raw_data = json.load(json_data)
    for raw_candidate in raw_data:
        candidate = Candidate.objects.get_or_create(
            name=raw_candidate["first_name"],
            surname=raw_candidate["last_name"]
        )
    json_data.close()
    return HttpResponse("Candidates import worked well")


@require_http_methods(["GET"])
def french_elections(request):
    # Only GET request will go that far
    _place, created = Place.objects.get_or_create(country="France", city="Paris")
    json_data = open('./static/french_elections.json')
    raw_data = json.load(json_data)
    for raw_election in raw_data:
        _election, created = Election.objects.get_or_create(
            date = datetime(int(raw_election["annee"]), int(raw_election["mois"]), int(raw_election["jour"])),
            place_id=_place.id,
            name = raw_election["election"]
        )
        for raw_candidate in raw_election["resultats"]:
            _candidate, created = Candidate.objects.get_or_create(
                name=raw_candidate["name"],
                surname=raw_candidate["surname"]
            )
            _result, created = Result.objects.get_or_create(
            election_id = _election.id,
            voting_result = raw_candidate["score"],
            candidate_id = _candidate.id
            )
    json_data.close()
    return HttpResponse("Elections and results import worked well")

@require_http_methods(["GET"])
def from_wikipedia(request):
    """
	This method will get some information for each candidate in the DB from wikipedia
	"""
    candidates = Candidate.objects.all()
    for candidate in candidates:
        url = WIKIPEDIA_BASE_API_URL
        url += candidate.name.replace(" ", "%20") + "%20"
        url += candidate.surname.replace(" ", "%20")
        response = requests.get(url)
        if response.status_code == 200:
            text = response.json()
            page_id = text["query"]["pages"].keys()[0]
            if page_id != "-1":
                text = text["query"]["pages"][page_id]["revisions"][0]["*"]
                starting_index = text.index("|name") if "|name" in text else text.index("birth_date")
                text = text[starting_index + 1:]
                # text.replace("=", "")
                data = text.split("\n|")
                data = clean_data(data)
                process_wikipedia_data(candidate, data)
        else:
            logging.warning("Wikipedia info import for %s %s did not work"
                            % (candidate.name, candidate.surname))
    return HttpResponse("Working on it")


def clean_data(data):
    cleaned_data = {}
    for element in data:
        element = element.split()
        starting_point = element.index("=") if "=" in element else 1
        ending_point = element.index("\'\'\'") if "\'\'\'" in element else len(element)
        value = " ".join(element[starting_point:ending_point])
        value = value.replace("[", "")
        value = value.replace("]", "")
        value = value.replace("{", "")
        value = value.replace("}", "")
        cleaned_data[element[0]] = value
    return cleaned_data


def process_birth_date(str_date):
    # birth date and age|1954|8|12|df=y
    start = str_date.index("|")
    end = str_date.rindex("|")
    date = str_date[start + 1:end]
    date = date.split("|")
    return datetime.date(int(date[0]), int(date[1]), int(date[2]))


def process_wikipedia_data(candidate, data):
    if not candidate.birth_date and "birth_date" in data.keys():
        try:
            birth_date = process_birth_date(data["birth_date"])
            candidate.birth_date = birth_date
        except ValueError:
            logging.warning("Value error on birth date")
    if not candidate.birth_place and "birth_place" in data.keys():
        birth_place = data["birth_place"].split(",")
        place, created = Place.objects.get_or_create(country=" ".join(birth_place[1:]), city=birth_place[0])
        candidate.birth_place_id = place.id
    if not candidate.nationality and "nationality" in data.keys():
        place, created = Place.objects.get_or_create(country=data["nationality"])
        candidate.place_id = place.id
    candidate.save()
    # Save all the different roles for one candidate
    roles = 0
    while roles == 0 or "office%s" % (roles) in data.keys():
        if roles == 0 and "office" in data.keys() or roles > 0:
            position = data["office%s" % (roles)] if roles > 0 else data["office"]
            if len(position) > 200:
                position = position[:200]
            political_function, created = PoliticalFunction.objects.get_or_create(position=position)
            # Beginning date
            beginning_date = None
            if roles == 0 and "term_start" in data.keys() or roles > 0 and ("term_start%s" % (roles)) in data.keys():
                field = "term_start%s" % (roles) if roles > 0 else "term_start"
                start = data[field]
                start = start.replace("=", "")
                start = start.lstrip()
                try:
                    beginning_date = to_datetime(start)
                except ValueError:
                    beginning_date = None
            # Ending date
            end_date = None
            if roles == 0 and "term_end" in data.keys() or roles > 0 and ("term_end%s" % (roles)) in data.keys():
                field = "term_end%s" % (roles) if roles > 0 else "term_end"
                end = data[field]
                end = end.replace("=", "")
                end = end.lstrip()
                logging.warning(end)
                try:
                    end_date = to_datetime(end)
                except ValueError:
                    end_date = None
            role, created = Role.objects.get_or_create(beginning_date=beginning_date, end_date=end_date,
                                                       position_type_id=political_function.id,
                                                       candidate_id=candidate.id)
        roles += 1

"""
Code used to import data from sondage en france
"""

@require_http_methods(['GET'])
def sondage_2012(request):
    wiki = "http://www.sondages-en-france.fr/sondages/Elections/Pr%C3%A9sidentielles%202012"
    page = urllib2.urlopen(wiki)
    soup = BeautifulSoup(page)
    right_table = soup.find("table", class_= "summaryTable")
    data = [[0 for x in range(14)] for y in range(12)]
    k = 0
    for row in right_table.findAll("tr"):
        cells = row.findAll("td")
        if len(cells) == 14:
            for i in range(14):
                data[k][i] = cells[i].get_text()
            k += 1
        if k > 11:
            break
    return HttpResponse("Hello, we've done the scrapping for 2012")


@require_http_methods(['GET'])
def sondage_2007(request):
    wiki = "https://fr.wikipedia.org/wiki/%C3%89lection_pr%C3%A9sidentielle_fran%C3%A7aise_de_2007"
    page = urllib2.urlopen(wiki)
    soup = BeautifulSoup(page)

    right_table = soup.find("table", class_="wikitable centre", style="text-align:center; font-size:95%;line-height:14px;")
    data = [[0 for x in range(6)] for y in range(17)]
    k = 1
    data[0][0] = "Institution"
    data[0][1] = "Date"
    data[0][2] = "Sarkozy"
    data[0][3] = "Royal"
    data[0][4] = "Bayrou"
    data[0][5] = "Le Pen"
    d = {"Sarkozy": 2, "Royal": 3, "Bayrou": 4, "Le Pen": 5}
    for row in right_table.findAll("tr"):
        cells = row.findAll("td")
        if len(cells) == 5:
            data[k][0] = cells[0].get_text()
            data[k][1] = cells[1].get_text()
            for b_tag in cells[4].findAll("b"):
                if b_tag.get_text() in d:
                    data[k][d[b_tag.get_text()]] = b_tag.findNext("b").get_text()
            for a_tag in cells[4].findAll("a", recursive=False):
                if a_tag.get_text() in d:
                    data[k][d[a_tag.get_text()]] = a_tag.next_sibling.replace(" | ", "").replace(" ", "")
            k += 1
    return HttpResponse("Hello, we've done the scrapping for 2007")

@require_http_methods(['GET'])
def sondage_2002(request):
    wiki = "http://www.france-politique.fr/sondages-electoraux-presidentielle-2002.htm"
    page = urllib2.urlopen(wiki)
    soup = BeautifulSoup(page)
    dataset = []
    for table in soup.findAll("table"):
        t = Thread(target= scrap_table, args=(table,dataset))
        t.start()
    return HttpResponse("Hello, we've done the scraping for 2002")

def scrap_table(table,dataset):
    r = table.find("tr")
    l = len(r.findAll("td"))
    data = [[0 for x in range(l)] for y in range(17)]
    k = 0
    for row in table.findAll("tr"):
        cells = row.findAll("td")
        if len(cells) == l:
            for i in range(l):
                data[k][i] = cells[i].get_text().replace("\n      ", "")
            k += 1
        if k > 16:
            break
    dataset.append(data)
    return dataset


"""
Code used to import data from Twitter
"""
non_usable_keys=[]

def get_trends(request):
    start_date = "2017-01-18"
    end_date = "2017-01-19"
    tag = "PrimaireGauche"
    election_id = 6
    get_twitter_trends(request, start_date, end_date, tag, election_id)
    return HttpResponse("It worked thanks !")


def get_twitter_trends(request, election_id, start_date, end_date, tag):
    try:
        election = Election.objects.get(id=election_id)
    except Election.DoesNotExist:
        return HttpResponseNotFound("Candidate not found")
    start = datetime.strptime(start_date, '%Y_%m_%d')
    end = datetime.strptime(end_date, '%Y_%m_%d')
    user_token = 0
    while start < end:
        save_to_database(start, tag, election)
        start += timedelta(1)


def replace_api_key(not_working_api_key):
    if not_working_api_key != '':
        non_usable_keys.append(not_working_api_key)

    for key in API_KEYS:
        if key in non_usable_keys:
            pass
        else:
            return key


def get_tweets_by_day_from_got(date, tag):
    next_date = date + timedelta(days=1)
    day = date.strftime('%Y-%m-%d')
    next_day = next_date.strftime('%Y-%m-%d')
    tweetCriteria = got.manager.TweetCriteria().setQuerySearch(tag).setSince(day).setUntil(next_day)
    tweets = got.manager.TweetManager.getTweets(tweetCriteria)
    return tweets


def filter_tweets_by_day_from_got(tweets, date, election):
    api_key = replace_api_key('')
    filtered_list = []
    for tweet in tweets:
        text = tweet.text
        for candidate in election.candidates.all():
            # On parcourt l'ensemble des candidats associés à l'objet election
            if text.find(candidate.surname) != -1:
                filtered_tweet = (date, text, candidate, get_score(text, api_key))
                filtered_list.append(filtered_tweet)
    return filtered_list


def get_score(text, api_key):
    client = Client(api_key=api_key, version='v3')
    text = text.encode("utf-8")
    sentiment = client.sentiment(text, lang='fr')

    if sentiment['status'] == 'OK':
        return sentiment['score']
    else:
        get_score(text, replace_api_key(api_key))


def aggregate_by_day(filtered_list, day, election):
    result = {}
    final_result = []
    for tweet in filtered_list:
        add_value(result, tweet[2], tweet[3])

    place, created = Place.objects.get_or_create(country = 'France', city="Paris")
    twitter, twitter_created = TrendSource.objects.get_or_create(name="Twitter")
    index = 0
    for candidate in result:
        trend = Trend(
            place_id = place.id,
            date = day,
            election_id = election.id,
            candidate_id = candidate.id,
            score = round(result[candidate]['score'] / result[candidate]['weight'], 2),
            weight = round(result[candidate]['weight'], 2),
            trend_source_id = twitter.id

        )
        trend.save()

def add_value(dictionary, candidate, score):
    if candidate not in dictionary:
        dictionary[candidate] = {
            'score': float(score),
            'weight': 1
        }
    else:
        dictionary[candidate]['score'] += float(score)
        dictionary[candidate]['weight'] += 1


def save_to_database(day, tag, election):
    """
    ::param day: datetime
    """
    tweets = get_tweets_by_day_from_got(day, tag)
    filtered_list = filter_tweets_by_day_from_got(tweets, day, election)

    aggregate_by_day(filtered_list, day, election)

"""
Code used to import data from Google Trends
"""
def import_trends(request_content):

    vecteur = request_content[0]
    pays = request_content[1]
    date = request_content[2]

    # connect to Google
    pytrend = TrendReq(GOOGLE_USERNAME, GOOGLE_PASSWORD, custom_useragent='My Coso Script')


    trend_payload = {'q': vecteur, 'hl': 'fr-FR', 'geo': pays,'date': date + ' 2m'}

    # trend
    trend = pytrend.trend(trend_payload)
    df = pytrend.trend(trend_payload, return_type='dataframe')
    return(df)


def analysis_from_google(request, election_id):
    elections = [Election.objects.get(id=election_id)]
    _google_trends, created = TrendSource.objects.get_or_create(name = "Google Trends")
    total = 0.00
    data=[]
    for election in elections:
        request_content = []
        liste_candidat = []
        candidats=election.candidates.order_by('result')
        for candidat in candidats[:5]:
            liste_candidat.append(candidat.surname + " " + candidat.name)
        vecteur_candidat=", ".join(liste_candidat)
        date=election.date
        mois = date.month
        annee=date.year
        date_temp=[str(mois),str(annee)]
        date_format="/".join(date_temp)
        request_content.append(vecteur_candidat)
        request_content.append("FR")
        request_content.append(date_format)
        my_data = import_trends(request_content)
        for daily_date in my_data.index:
            for candidate in candidats[:5]:
                total = 0
                candidate_name =  candidate.surname + " " + candidate.name
                if (isinstance(my_data.loc[daily_date, candidate_name.lower()], (int, float, long))):
                    candidate_weight = round(float(my_data.loc[daily_date, candidate_name.lower()]),2)
                total = total + candidate_weight
            for candidate in candidats[:5]:
                candidate_name =  candidate.surname + " " + candidate.name
                if (total !=0 and str(total) != "nan"):
                    _trend, created = Trend.objects.get_or_create(place_id = election.place.id, date = pandas.to_datetime(daily_date), election_id = election.id, candidate_id = candidate.id, score = round(candidate_weight/total,2), weight = candidate_weight, trend_source_id = _google_trends.id)
    return HttpResponse("Hello, we've done the Google Analysis")

