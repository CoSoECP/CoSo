# -*- coding: UTF-8 -*-
from django.shortcuts import render
from datetime import time, datetime
from repustate import Client
import os
import sys
import tweepy
from json import load
from django.http import HttpResponseNotFound

# currentdir = os.getcwd()
# parentdir = os.path.dirname(currentdir)
# coso = parentdir + '/coso'
# sys.path.insert(0, coso)
# polls = parentdir + '/polls'
# sys.path.insert(0, polls)
from coso.settings import API_KEYS
from polls.models import Trend, Place, Election, Candidate, Result, TrendSource

non_usable_keys=[]


def get_twitter_trends(request):
	start_date = request.POST.get("start_date","")
	end_date = request.POST.get("start_end","")
	tag = request.POST.get("tag","")
	election_id = request.POST.get("election","")
	try:
		election = Election.objects.get(id=election_id)
	except Entry.DoesNotExist:
		return HttpResponseNotFound("Candidate not found")
	start = datetime.strptime(start_date, '%Y-%m-%d')
	end = datetime.strptime(end_date, '%Y-%m-%d')
	user_token = 0
	while start <= end:
		save_to_database(start, tag, user_token, election)
		start += datetime.deltatime(1)
		user_token += 1
		if user_token > 4:
			user_token = 0


def replace_api_key(not_working_api_key):
	if not_working_api_key != '':
		non_usable_keys.append(not_working_api_key)

	for key in API_KEYS:
		if key in non_usable_keys:
			pass
		else:
			return key


# def candidate_list():
#     candidates =[]


def get_tweets_by_day(day, tag, user_token):
    filename = os.path.dirname(os.getcwd()) + "/static/access.json"
    with open(filename) as file:
        token = load(file)

    auth = tweepy.OAuthHandler(token[user_token]["consumer_key"], token[user_token]["consumer_secret"])
    auth.set_access_token(token[user_token]["access_key"], token[user_token]["access_secret"])
    api = tweepy.API(auth, wait_on_rate_limit=True)

    date = datetime.strptime(day, '%Y-%m-%d')
    next_date = date + datetime.timedelta(days=1)
    next_day = next_date.strftime('%Y-%m-%d')

    return tweepy.Cursor(api.search, q=tag, since=day,
                         until=next_day).items(25)


def filter_tweets_by_day(tweets, day, election):
    api_key = replace_api_key('')
    filtered_list = []

    while True:
        try:
            tweet = tweets.next()
            text = tweet.text
            print(tweet.created_at)
            for candidate in election.candidates.all():
                if text.find(candidate.surname) != -1:
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


def aggregate_by_day(filtered_list, day, election):
    result = {}
    final_result = []
    for tweet in filtered_list:
        add_value(result, tweet['candidate'], tweet['score'])

    (place, election, twitter, candidates_created) = objects_to_create()
    index = 0
    for candidate in result:
        trend = Trend(
            place_id = place.id,
            date = datetime.strptime(day, '%Y-%m-%d'),
            election_id = election.id,
            candidate_id = candidate.id,
            weight = result[candidate]['weight'],
            trend_source_id = twitter.id

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


def add_value(dictionary, candidate, score):
    if candidate not in dictionary:
        dictionary[candidate] = {
            'score': float(score),
            'weight': 1
        }
    else:
        dictionary[candidate]['score'] += float(score)
        dictionary[candidate]['weight'] += 1


def save_to_database(day, tag, user_token, election):
    # list_of_candidate_names = {"valls", "montebourg", "hamon"}

    tweets = get_tweets_by_day(day, tag, user_token)
    filtered_list = filter_tweets_by_day(tweets, day, list_of_candidate_names)
    # return aggregate_by_day(filtered_list, day)
    aggregate_by_day(filtered_list, day, election)
