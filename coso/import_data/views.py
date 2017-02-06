# -*- coding: UTF-8 -*-
from django.shortcuts import render
from datetime import time, datetime
from repustate import Client
import os
import tweepy

currentdir = os.getwcd()
parentdir = os.path.dirname(currentdir)
coso = parentdir + '/coso'
os.path.insert(0, coso)
polls = parentdir + '/polls'
os.path.insert(0, polls)
from settings import API_KEYS
from models import Trend, Place, Election, Candidate, Result, TrendSource

non_usable_keys=[]


def replace_api_key(not_working_api_key):
	if not_working_api_key != '':
		non_usable_keys.append(not_working_api_key)

	for key in API_KEYS:
		if key in non_usable_keys:
			pass
		else:
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
