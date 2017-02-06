from coso.settings import WIKIPEDIA_BASE_API_URL
from polls.models import Candidate, Place, PoliticalFunction, Role

from libs.time import to_datetime

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from coso.settings.py import API_KEYS
import datetime
import json
import logging

import requests
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

from coso.coso.settings import API_KEYS
from coso.polls.models import Candidate, Place, PoliticalFunction, Role
from libs.time import to_datetime

from datetime import time, datetime
from repustate import Client
import os
import tweepy


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

# -*- coding: UTF-8 -*-


currentdir = os.getwcd()
parentdir = os.path.dirname(currentdir)
coso = parentdir + '/coso'
os.path.insert(0, coso)
polls = parentdir + '/polls'
os.path.insert(0, polls)
from settings import API_KEYS
from models import Trend, Place, Election, Candidate, Result, TrendSource

non_usable_keys=[]
>>>>>>> trend à tester

non_usable_keys=[]

<<<<<<< 5c819ece19912946ecb2c717f7dcfe2d361d2852

def replace_api_key(not_working_api_key):
	if not_working_api_key != '':
		non_usable_keys.append(not_working_api_key)
	
def replace_api_key(not_working_api_key):
	if not_working_api_key != '':
		non_usable_keys.append(not_working_api_key)

	for key in API_KEYS:
		if key in non_usable_keys:
			pass
		else:
			return key

			return key


def objects_to_create():
    place, created = Place.objects.get_or_create(country="France")
    election, created = Election.objects.get_or_create(date=datetime.datetime(2016,12,22), place_id = place.id)
    valls, created = Candidate.objects.get_or_create(name="Valls", surname = "Manuel", birth_date=datetime.datetime(1968,12,05), birth_place_id= place.id, nationality_id= place.id)
    montebourg, created = Candidate.objects.get_or_create(name="Montebourg", surname = "Arnaud", birth_place_id= place.id, nationality_id= place.id)
    hamon, created = Candidate.objects.get_or_create(name="Hamon", surname = "Benoit", nationality_id= place.id)
    bennahmias, created = Candidate.objects.get_or_create(name="Bennahmias", surname = "Jean-Luc", nationality_id= place.id)
    de_rugy, created = Candidate.objects.get_or_create(name="De Rugy", surname = "François", nationality_id= place.id)
    pinel, created = Candidate.objects.get_or_create(name="Pinel", surname = "Sylvia", nationality_id= place.id)
    peillon, created = Candidate.objects.get_or_create(name="Peillon", surname = "Vincent", birth_date=datetime.datetime(1968,12,05), birth_place_id= place.id, nationality_id= place.id)
    result1, created = Result.objects.get_or_create(election_id = election.id, candidate_id = valls.id)
    result2, created = Result.objects.get_or_create(election_id = election.id, candidate_id = montebourg.id)
    twitter, created = TrendSource.objects.get_or_create(name = 'Twitter')
    candidates_created = [valls, montebourg, hamon, bennahmias, de_rugy, pinel, peillon]
    return (place, election, twitter, candidates_created)




def candidate_list():
    candidates =[
    ]


def get_tweets_by_day(day, tag):
    from json import load
    filename = os.path.dirname(os.getcwd()) + "/static/access.json"
    with open(filename) as file:
        token = load(file)

    auth = tweepy.OAuthHandler(token[0]["consumer_key"], token[0]["consumer_secret"])
    auth.set_access_token(token[0]["access_key"], token[0]["access_secret"])
    api = tweepy.API(auth, wait_on_rate_limit=True)

    date = datetime.datetime.strptime(day, '%Y-%m-%d')
    next_date = date + datetime.timedelta(days=1)
    next_day = next_date.strftime('%Y-%m-%d')

    return tweepy.Cursor(api.search, q=tag, since=day,
                         until=next_day).items(25)


def filter_tweets_by_day(tweets, day, list_of_candidate_names):
    api_key = replace_api_key('')
    filtered_list = []

    while True:
        try:
            tweet = tweets.next()
            text = tweet.text
            print(tweet.created_at)
            for candidate in list_of_candidate_names:
                if text.find(candidate) != -1:
                    filtered_tweet = {
                        'created_at': day,
                        'text': text,
                        'candidate': candidate,
                        'score': get_score(text, api_key)
                    }
                    filtered_list.append(filtered_tweet)
        except tweepy.TweepError:
            print('rate limit raised !')
            time.sleep(60 * 15)
            continue
        except StopIteration:
            break

    return filtered_list




def get_score(text, api_key):
    client = Client(api_key=api_key, version='v3')
    sentiment = client.sentiment(text, lang='fr')

    if sentiment['status'] == 'OK':
        return sentiment['score']
    else:
        get_score(text, replace_api_key(api_key))


def aggregate_by_day(filtered_list, day):
    result = {}
    final_result = []
    for tweet in filtered_list:
        add_value(result, tweet['candidate'], tweet['score'])

    (place, election, twitter, candidates_created) = objects_to_create()
    index = 0
    for candidate in result.keys():
        for can in candidates_created: # On parcourt la liste des candidats que l'on a crées à la main avec get_or_create
             if can.name == candidate:
                index = candidates_created.index(can)
        trend = Trend.objects.get_or_create(
            place = place.id,
            date = datetime.strptime(day, '%Y-%m-%d'),
            election = election.id,
            candidate = candidates_created[index].id,
            score = result[candidate]['score']/result[candidate]['weight'],
            weight = result[candidate]['weight'],
            trend_source = twitter.id

        )
        trend.save()
        # return trend # UNIQUEMENT POUR TESTER LA FONCTION, A ENLEVER 

    #     final_result.append(
    #         {
    #             'place': 'France',
    #             'date': datetime.datetime.strptime(day, '%Y-%m-%d'),
    #             'election': 'Primaire socialiste 2017',
    #             'candidate': candidate,
    #             'score': result[candidate]['score'] / result[candidate]['weight'],
    #             'weight': result[candidate]['weight'],
    #             'trend_source': 'Twitter'
    #         }
    #     )
    # #with open('data.json', 'w') as f:
    #  #   json.dump(final_result, f, ensure_ascii=False)
    # return final_result


def add_value(dict, candidate, score):
    if candidate not in dict:
        dict[candidate] = {
            'score': float(score),
            'weight': 1
        }
    else:
        dict[candidate]['score'] += float(score)
        dict[candidate]['weight'] += 1


def produce_json(day, tag):
    list_of_candidate_names = {"valls", "montebourg", "hamon"}

    tweets = get_tweets_by_day(day, tag)
    filtered_list = filter_tweets_by_day(tweets, day, list_of_candidate_names)
    # return aggregate_by_day(filtered_list, day)
    aggregate_by_day(filtered_list, day)
>>>>>>> trend à tester
