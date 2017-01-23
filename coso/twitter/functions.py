from datetime import time

import tweepy


def get_tweets_by_day(day, tag):
    import datetime
    from json import load
    filename = "C:/token/access.json"
    with open(filename) as file:
        token = load(file)

    auth = tweepy.OAuthHandler(token["consumer_key"], token["consumer_secret"])
    auth.set_access_token(token["access_key"], token["access_secret"])
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
    import datetime
    result = {}
    final_result = []
    for tweet in filtered_list:
        add_value(result, tweet['candidate'], tweet['score'])

    for candidate in result:
        final_result.append(
            {
                'place': 'France',
                'date': datetime.datetime.strptime(day, '%Y-%m-%d'),
                'election': 'Primaire socialiste 2017',
                'candidate': candidate,
                'score': result[candidate]['score'] / result[candidate]['weight'],
                'weight': result[candidate]['weight'],
                'trend_source': 'Twitter'
            }
        )
    #with open('data.json', 'w') as f:
     #   json.dump(final_result, f, ensure_ascii=False)
    return final_result


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