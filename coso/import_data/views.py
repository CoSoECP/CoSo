# -*- coding: UTF-8 -*-
from coso.settings import WIKIPEDIA_BASE_API_URL, API_KEYS
from polls.models import Candidate, Place, PoliticalFunction, Role, Trend, Election, Result, TrendSource
from libs.time import to_datetime
from libs import got

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseNotFound
from django.http import HttpResponse

import json
import logging
import requests
from datetime import time, datetime, timedelta
from repustate import Client
import os
import sys
import tweepy
from json import load


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
