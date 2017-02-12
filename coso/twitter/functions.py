from datetime import time
import datetime
import tweepy
from polls/models.py import Trend, Place, Election, Candidate

def different_classes():   
    _place, created = Place.objects.get_or_create(country="France")
    _election, created = Election.objects.get_or_create(date=datetime.datetime(2016,12,22), place_id = _place.id)
    _valls, created = Candidate.objects.get_or_create(name="Valls", surname = "Manuel", birth_date=datetime.datetime(1968,12,05), birth_place_id= _place.id, nationality_id= _place.id)
    _montebourg, created = Candidate.objects.get_or_create(name="Montebourg", surname = "Arnaud", birth_place_id= _place.id, nationality_id= _place.id)
    _hamon, created = Candidate.objects.get_or_create(name="Hamon", surname = "Benoit", nationality_id= _place.id)
    _bennahmias, created = Candidate.objects.get_or_create(name="Bennahmias", surname = "Jean-Luc", nationality_id= _place.id)
    _de_rugy, created = Candidate.objects.get_or_create(name="De Rugy", surname = "François", nationality_id= _place.id)
    _pinel, created = Candidate.objects.get_or_create(name="Pinel", surname = "Sylvia", nationality_id= _place.id)
    _peillon, created = Candidate.objects.get_or_create(name="Peillon", surname = "Vincent", birth_date=datetime.datetime(1968,12,05), birth_place_id= _place.id, nationality_id= _place.id)
    _result1, created = Result.objects.get_or_create(election_id = _election.id, candidate_id = _candidate1.id)
    _result2, created = Result.objects.get_or_create(election_id = _election.id, candidate_id = _candidate2.id)
    _twitter, created = TrendSource.objects.get_or_create(name = 'Twitter')


def candidate_list():
    candidates =[
    ]


def get_tweets_by_day(day, tag):
    from json import load
    filename = "./static/access.json"
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
    from repustate import Client
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

    for candidate in result:
        trend = Trend.objects.get_or_create(
            place_id = place.id
            date = datetime.datetime.strptime(day, '%Y-%m-%d'),
            election = election.id
            candidate = candidate,
            score = result[candidate]['score'] / result[candidate]['weight'],
            weight = result[candidate]['weight'],
            trend_source = twitter.id

        )

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
    return aggregate_by_day(filtered_list, day)


def replace_api_key(api_key):
    return '6c8f03dbdd7fd059f44f365bf8eca282dd5f214c'