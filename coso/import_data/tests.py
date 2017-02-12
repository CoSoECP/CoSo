from django.test import TestCase
import datetime
from views import save_to_database, get_tweets_by_day, filter_tweets_by_day

def test_aggregate_by_day(filtered_list, day):
	# save_to_database('2017-01-15', 'PrimaireGauche', 0)
	filter_tweets_by_day(get_tweets_by_day(datetime.datetime.strptime('2017-02-08', '%Y-%m-%d'),'PrimaireGauche'),datetime.datetime.strptime('2017-02-08', '%Y-%m-%d'))
	# save_to_database('2017-01-15','PrimaireGauche',0,election)
	# print("Kasra fragile")