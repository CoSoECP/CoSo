from functions import aggregate_by_day

#get_tweets_by_day('2017-01-31', '')




#for tweet in cricTweet:
    #print(tweet.text)
    #print(tweet.created_at)
    #print(tweet.entities['user_mentions'])

list = [{
                    'created_at': '2017-01-13',
                    'text': 'Bonjour :)',
                    'candidate': 'valls',
                    'score': '0.7'
                },
    {
                    'created_at': '2017-01-13',
                    'text': 'Bonsoir :)',
                    'candidate': 'valls',
                    'score': '-0.3'
                },
    {
        'created_at': '2017-01-13',
        'text': 'Bonsoir :)',
        'candidate': 'montebourg',
        'score': '-0.3'
    }
]

print(aggregate_by_day(list, '2017-01-13'))
